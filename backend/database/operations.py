"""
database/operations.py
──────────────────────
Every database operation in one place.
Import these functions into your Flask/FastAPI routes —
never write raw SQL or raw SQLAlchemy outside this file.

Sections:
  1. Stations
  2. Search history logging + retrieval
  3. Prediction logging + retrieval
  4. Analytics aggregations
  5. API metrics
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import func, desc, asc, cast, Date, text
from sqlalchemy.orm import Session

from .models import Station, SearchHistory, Prediction, APIMetric

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
# 1. STATIONS
# ══════════════════════════════════════════════════════════════════════════════

def get_station_by_code(db: Session, code: str) -> Optional[Station]:
    """Return a single station by its code (case-insensitive)."""
    return (
        db.query(Station)
        .filter(Station.station_code == code.upper().strip())
        .first()
    )


def get_all_stations(db: Session) -> list[dict]:
    """Return all stations, major ones first."""
    stations = (
        db.query(Station)
        .order_by(desc(Station.is_major), asc(Station.station_name))
        .all()
    )
    return [s.to_dict() for s in stations]


def search_stations(db: Session, query: str, limit: int = 10) -> list[dict]:
    """
    Autocomplete search — matches station code, name, or city.
    Used by the frontend search box.
    """
    q = f"%{query.upper().strip()}%"
    stations = (
        db.query(Station)
        .filter(
            (Station.station_code.ilike(q))
            | (Station.station_name.ilike(q))
            | (Station.city.ilike(q))
        )
        .order_by(desc(Station.is_major))
        .limit(limit)
        .all()
    )
    return [s.to_dict() for s in stations]


def get_stations_by_state(db: Session, state: str) -> list[dict]:
    stations = (
        db.query(Station)
        .filter(Station.state.ilike(f"%{state}%"))
        .order_by(desc(Station.is_major), asc(Station.station_name))
        .all()
    )
    return [s.to_dict() for s in stations]


# ══════════════════════════════════════════════════════════════════════════════
# 2. SEARCH HISTORY
# ══════════════════════════════════════════════════════════════════════════════

def log_search(
    db: Session,
    source_code: str,
    destination_code: str,
    path: list,
    total_distance_km: Optional[float] = None,
    total_duration_minutes: Optional[int] = None,
    stops_count: Optional[int] = None,
    algorithm_used: str = "dijkstra",
    query_time_ms: Optional[float] = None,
) -> SearchHistory:
    """
    Call this every time a route search is performed.

    Example (in your Flask route):
        import time
        start = time.perf_counter()
        result = networkx_search(source, destination)
        elapsed = (time.perf_counter() - start) * 1000

        with get_db() as db:
            log_search(db, source, destination, result['path'],
                       result['distance'], result['duration'],
                       len(result['path']) - 1, 'dijkstra', elapsed)
    """
    record = SearchHistory(
        source_station_code=source_code.upper().strip(),
        destination_station_code=destination_code.upper().strip(),
        path=json.dumps(path) if path else None,
        path_found=bool(path),
        total_distance_km=total_distance_km,
        total_duration_minutes=total_duration_minutes,
        stops_count=stops_count,
        algorithm_used=algorithm_used,
        query_time_ms=query_time_ms,
    )
    db.add(record)
    db.flush()   # get the ID without committing (commit happens in context manager)
    logger.debug("Logged search: %s → %s", source_code, destination_code)
    return record


def get_recent_searches(db: Session, limit: int = 20) -> list[dict]:
    """Most recent N route searches."""
    rows = (
        db.query(SearchHistory)
        .order_by(desc(SearchHistory.created_at))
        .limit(limit)
        .all()
    )
    return [r.to_dict() for r in rows]


def get_searches_between(
    db: Session, start: datetime, end: datetime
) -> list[dict]:
    """All searches in a datetime range — useful for export/audit."""
    rows = (
        db.query(SearchHistory)
        .filter(SearchHistory.created_at >= start, SearchHistory.created_at <= end)
        .order_by(desc(SearchHistory.created_at))
        .all()
    )
    return [r.to_dict() for r in rows]


# ══════════════════════════════════════════════════════════════════════════════
# 3. PREDICTIONS
# ══════════════════════════════════════════════════════════════════════════════

def log_prediction(
    db: Session,
    source_code: Optional[str],
    destination_code: Optional[str],
    delay_probability: float,
    inputs: Optional[dict] = None,
    shap_values: Optional[dict] = None,
    delay_minutes_predicted: Optional[int] = None,
    model_version: str = "1.0.0",
    query_time_ms: Optional[float] = None,
) -> Prediction:
    """
    Call this every time an XGBoost prediction is served.

    inputs dict keys (all optional — pass whatever your model uses):
        train_number, departure_hour, day_of_week, month, distance_km

    shap_values dict example:
        {"departure_hour": 0.23, "distance_km": -0.12, "month": 0.07}
    """
    inp = inputs or {}
    record = Prediction(
        source_station_code=source_code.upper().strip() if source_code else None,
        destination_station_code=destination_code.upper().strip() if destination_code else None,
        train_number=inp.get("train_number"),
        departure_hour=inp.get("departure_hour"),
        day_of_week=inp.get("day_of_week"),
        month=inp.get("month"),
        distance_km=inp.get("distance_km"),
        delay_probability=round(float(delay_probability), 4),
        delay_minutes_predicted=delay_minutes_predicted,
        feature_importance=json.dumps(shap_values) if shap_values else None,
        model_version=model_version,
        query_time_ms=query_time_ms,
    )
    db.add(record)
    db.flush()
    logger.debug(
        "Logged prediction: %s → %s  %.1f%%",
        source_code, destination_code, delay_probability
    )
    return record


def get_recent_predictions(db: Session, limit: int = 20) -> list[dict]:
    rows = (
        db.query(Prediction)
        .order_by(desc(Prediction.created_at))
        .limit(limit)
        .all()
    )
    return [r.to_dict() for r in rows]


# ══════════════════════════════════════════════════════════════════════════════
# 4. ANALYTICS  (all the meaty aggregations)
# ══════════════════════════════════════════════════════════════════════════════

def get_summary(db: Session) -> dict:
    """
    Top-level KPI card data.
    Returns in a single DB round-trip.
    """
    total_searches = db.query(func.count(SearchHistory.id)).scalar() or 0
    successful     = db.query(func.count(SearchHistory.id)).filter(SearchHistory.path_found == True).scalar() or 0
    total_preds    = db.query(func.count(Prediction.id)).scalar() or 0
    avg_prob       = db.query(func.avg(Prediction.delay_probability)).scalar()
    avg_query_ms   = db.query(func.avg(SearchHistory.query_time_ms)).scalar()

    return {
        "total_searches":         total_searches,
        "successful_searches":    successful,
        "failed_searches":        total_searches - successful,
        "success_rate_pct":       round(successful / total_searches * 100, 1) if total_searches else 0,
        "total_predictions":      total_preds,
        "avg_delay_probability":  round(float(avg_prob), 2) if avg_prob is not None else 0,
        "avg_search_time_ms":     round(float(avg_query_ms), 2) if avg_query_ms is not None else 0,
    }


def get_popular_routes(db: Session, limit: int = 10) -> list[dict]:
    """
    Most searched origin → destination pairs.
    Only counts successful (path_found = True) searches.
    """
    rows = (
        db.query(
            SearchHistory.source_station_code.label("source"),
            SearchHistory.destination_station_code.label("destination"),
            func.count(SearchHistory.id).label("search_count"),
            func.max(SearchHistory.created_at).label("last_searched"),
            func.avg(SearchHistory.total_distance_km).label("avg_distance"),
        )
        .filter(SearchHistory.path_found == True)
        .group_by(
            SearchHistory.source_station_code,
            SearchHistory.destination_station_code,
        )
        .order_by(desc("search_count"))
        .limit(limit)
        .all()
    )
    return [
        {
            "source":        r.source,
            "destination":   r.destination,
            "search_count":  r.search_count,
            "last_searched": r.last_searched.isoformat() if r.last_searched else None,
            "avg_distance":  round(float(r.avg_distance), 1) if r.avg_distance else None,
        }
        for r in rows
    ]


def get_search_volume_trend(db: Session, days: int = 30) -> list[dict]:
    """
    Daily search volume for the last N days.
    Used for the line chart on the analytics dashboard.
    """
    since = datetime.utcnow() - timedelta(days=days)
    rows = (
        db.query(
            cast(SearchHistory.created_at, Date).label("date"),
            func.count(SearchHistory.id).label("total"),
            func.count(
                SearchHistory.id
            ).filter(SearchHistory.path_found == True).label("successful"),
        )
        .filter(SearchHistory.created_at >= since)
        .group_by(cast(SearchHistory.created_at, Date))
        .order_by(cast(SearchHistory.created_at, Date))
        .all()
    )
    return [
        {
            "date":       str(r.date),
            "total":      r.total,
            "successful": r.successful,
            "failed":     r.total - r.successful,
        }
        for r in rows
    ]


def get_peak_search_hours(db: Session) -> list[dict]:
    """
    Search volume by hour of day (0–23).
    Shows when users are most active — good for README / presentation.
    """
    rows = (
        db.query(
            func.extract("hour", SearchHistory.created_at).label("hour"),
            func.count(SearchHistory.id).label("count"),
        )
        .group_by(func.extract("hour", SearchHistory.created_at))
        .order_by(func.extract("hour", SearchHistory.created_at))
        .all()
    )
    # Fill in hours with zero count so the chart has all 24 points
    hour_map = {int(r.hour): r.count for r in rows}
    return [
        {"hour": h, "count": hour_map.get(h, 0)}
        for h in range(24)
    ]


def get_prediction_distribution(db: Session, buckets: int = 10) -> list[dict]:
    """
    Histogram of delay probabilities in equal-width buckets (0–100%).
    Used for the histogram chart on the analytics dashboard.
    """
    bucket_size = 100 / buckets
    all_probs = db.query(Prediction.delay_probability).all()
    if not all_probs:
        return []

    counts = [0] * buckets
    for (p,) in all_probs:
        idx = min(int(float(p) / bucket_size), buckets - 1)
        counts[idx] += 1

    return [
        {
            "range": f"{int(i * bucket_size)}–{int((i + 1) * bucket_size)}%",
            "count": counts[i],
        }
        for i in range(buckets)
    ]


def get_high_risk_routes(db: Session, limit: int = 10, min_predictions: int = 2) -> list[dict]:
    """
    Routes with the highest average predicted delay probability.
    Only includes routes with at least min_predictions data points.
    """
    rows = (
        db.query(
            Prediction.source_station_code.label("source"),
            Prediction.destination_station_code.label("destination"),
            func.count(Prediction.id).label("prediction_count"),
            func.avg(Prediction.delay_probability).label("avg_probability"),
            func.max(Prediction.delay_probability).label("max_probability"),
        )
        .filter(
            Prediction.source_station_code.isnot(None),
            Prediction.destination_station_code.isnot(None),
        )
        .group_by(
            Prediction.source_station_code,
            Prediction.destination_station_code,
        )
        .having(func.count(Prediction.id) >= min_predictions)
        .order_by(desc("avg_probability"))
        .limit(limit)
        .all()
    )
    return [
        {
            "source":           r.source,
            "destination":      r.destination,
            "prediction_count": r.prediction_count,
            "avg_probability":  round(float(r.avg_probability), 2),
            "max_probability":  round(float(r.max_probability), 2),
        }
        for r in rows
    ]


def get_prediction_trend(db: Session, days: int = 30) -> list[dict]:
    """
    Daily average delay probability for the last N days.
    Shows whether delay risk is trending up or down.
    """
    since = datetime.utcnow() - timedelta(days=days)
    rows = (
        db.query(
            cast(Prediction.created_at, Date).label("date"),
            func.count(Prediction.id).label("count"),
            func.avg(Prediction.delay_probability).label("avg_probability"),
        )
        .filter(Prediction.created_at >= since)
        .group_by(cast(Prediction.created_at, Date))
        .order_by(cast(Prediction.created_at, Date))
        .all()
    )
    return [
        {
            "date":            str(r.date),
            "count":           r.count,
            "avg_probability": round(float(r.avg_probability), 2),
        }
        for r in rows
    ]


def get_weekday_stats(db: Session) -> list[dict]:
    """
    Average delay probability by day of week.
    0 = Monday … 6 = Sunday.
    """
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    rows = (
        db.query(
            Prediction.day_of_week.label("dow"),
            func.count(Prediction.id).label("count"),
            func.avg(Prediction.delay_probability).label("avg_probability"),
        )
        .filter(Prediction.day_of_week.isnot(None))
        .group_by(Prediction.day_of_week)
        .order_by(Prediction.day_of_week)
        .all()
    )
    result = {r.dow: r for r in rows}
    return [
        {
            "day":             day_names[d],
            "day_number":      d,
            "count":           result[d].count if d in result else 0,
            "avg_probability": round(float(result[d].avg_probability), 2) if d in result else 0,
        }
        for d in range(7)
    ]


def get_full_analytics(db: Session) -> dict:
    """
    Single call that returns everything the analytics dashboard needs.
    Keeps the number of API round trips to one.
    """
    return {
        "summary":                get_summary(db),
        "popular_routes":         get_popular_routes(db, limit=10),
        "search_volume_30d":      get_search_volume_trend(db, days=30),
        "peak_hours":             get_peak_search_hours(db),
        "prediction_distribution":get_prediction_distribution(db),
        "high_risk_routes":       get_high_risk_routes(db, limit=10),
        "prediction_trend_30d":   get_prediction_trend(db, days=30),
        "weekday_stats":          get_weekday_stats(db),
        "recent_searches":        get_recent_searches(db, limit=5),
        "recent_predictions":     get_recent_predictions(db, limit=5),
    }


# ══════════════════════════════════════════════════════════════════════════════
# 5. API METRICS
# ══════════════════════════════════════════════════════════════════════════════

def log_api_metric(
    db: Session,
    endpoint: str,
    method: str,
    status_code: int,
    response_ms: float,
) -> APIMetric:
    """Log latency for any API call. Use the middleware in INTEGRATION_GUIDE.md."""
    record = APIMetric(
        endpoint=endpoint,
        method=method.upper(),
        status_code=status_code,
        response_ms=round(response_ms, 3),
    )
    db.add(record)
    db.flush()
    return record


def get_endpoint_performance(db: Session, hours: int = 24) -> list[dict]:
    """
    Average and p95 response time per endpoint for the last N hours.
    Shows on the 'System Health' panel of the dashboard.
    """
    since = datetime.utcnow() - timedelta(hours=hours)
    rows = (
        db.query(
            APIMetric.endpoint,
            APIMetric.method,
            func.count(APIMetric.id).label("call_count"),
            func.avg(APIMetric.response_ms).label("avg_ms"),
            func.min(APIMetric.response_ms).label("min_ms"),
            func.max(APIMetric.response_ms).label("max_ms"),
            func.avg(
                func.cast(APIMetric.status_code >= 400, Integer)
            ).label("error_rate"),
        )
        .filter(APIMetric.created_at >= since)
        .group_by(APIMetric.endpoint, APIMetric.method)
        .order_by(desc("call_count"))
        .all()
    )
    return [
        {
            "endpoint":   r.endpoint,
            "method":     r.method,
            "calls":      r.call_count,
            "avg_ms":     round(float(r.avg_ms), 2),
            "min_ms":     round(float(r.min_ms), 2),
            "max_ms":     round(float(r.max_ms), 2),
            "error_rate": round(float(r.error_rate) * 100, 1),
        }
        for r in rows
    ]
