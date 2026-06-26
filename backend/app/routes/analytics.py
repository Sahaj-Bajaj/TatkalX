from fastapi import APIRouter, Query


from app.core.redis import redis_client
from database.connection import get_db, check_connection
from database.operations import (
    get_full_analytics,
    get_summary,
    get_popular_routes,
    get_search_volume_trend,
    get_peak_search_hours,
    get_high_risk_routes,
    get_weekday_stats,
    get_endpoint_performance,
    get_all_stations,
    get_station_by_code,
    search_stations,
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)

ANALYTICS_CACHE_TTL = 300  # 5 minutes


@router.get("")
def analytics_dashboard():
    cache_key = "analytics:dashboard"

    cached = redis_client.get(cache_key)
    if cached is not None:
        return cached

    with get_db() as db:
        data = get_full_analytics(db)

    response = {
        "success": True,
        "data": data,
    }

    redis_client.set(cache_key, response, ANALYTICS_CACHE_TTL)
    return response


@router.get("/summary")
def analytics_summary():
    cache_key = "analytics:summary"

    cached = redis_client.get(cache_key)
    if cached is not None:
        return cached

    with get_db() as db:
        data = get_summary(db)

    response = {
        "success": True,
        "data": data,
    }

    redis_client.set(cache_key, response, ANALYTICS_CACHE_TTL)
    return response


@router.get("/popular")
def popular_routes(limit: int = Query(10, le=50)):
    cache_key = f"analytics:popular:{limit}"

    cached = redis_client.get(cache_key)
    if cached is not None:
        return cached

    with get_db() as db:
        data = get_popular_routes(db, limit=limit)

    response = {
        "success": True,
        "data": data,
    }

    redis_client.set(cache_key, response, ANALYTICS_CACHE_TTL)
    return response


@router.get("/trend")
def search_trend(days: int = Query(30, le=365)):
    cache_key = f"analytics:trend:{days}"

    cached = redis_client.get(cache_key)
    if cached is not None:
        return cached

    with get_db() as db:
        data = get_search_volume_trend(db, days=days)

    response = {
        "success": True,
        "data": data,
    }

    redis_client.set(cache_key, response, ANALYTICS_CACHE_TTL)
    return response


@router.get("/peak-hours")
def peak_hours():
    cache_key = "analytics:peak-hours"

    cached = redis_client.get(cache_key)
    if cached is not None:
        return cached

    with get_db() as db:
        data = get_peak_search_hours(db)

    response = {
        "success": True,
        "data": data,
    }

    redis_client.set(cache_key, response, ANALYTICS_CACHE_TTL)
    return response


@router.get("/risk")
def high_risk_routes(
    limit: int = Query(10, le=50),
    min_predictions: int = Query(2, ge=1),
):
    cache_key = f"analytics:risk:{limit}:{min_predictions}"

    cached = redis_client.get(cache_key)
    if cached is not None:
        return cached

    with get_db() as db:
        data = get_high_risk_routes(
            db,
            limit=limit,
            min_predictions=min_predictions,
        )

    response = {
        "success": True,
        "data": data,
    }

    redis_client.set(cache_key, response, ANALYTICS_CACHE_TTL)
    return response


@router.get("/weekdays")
def weekday_stats():
    cache_key = "analytics:weekdays"

    cached = redis_client.get(cache_key)
    if cached is not None:
        return cached

    with get_db() as db:
        data = get_weekday_stats(db)

    response = {
        "success": True,
        "data": data,
    }

    redis_client.set(cache_key, response, ANALYTICS_CACHE_TTL)
    return response


@router.get("/health")
def analytics_health(hours: int = Query(24, le=720)):
    cache_key = f"analytics:health:{hours}"

    cached = redis_client.get(cache_key)
    if cached is not None:
        return cached

    with get_db() as db:
        performance = get_endpoint_performance(db, hours=hours)

    response = {
        "success": True,
        "data": {
            "db_online": check_connection(),
            "window_hours": hours,
            "endpoints": performance,
        },
    }

    redis_client.set(cache_key, response, ANALYTICS_CACHE_TTL)
    return response


@router.get("/stations")
def all_stations():
    cache_key = "analytics:stations"

    cached = redis_client.get(cache_key)
    if cached is not None:
        return cached

    with get_db() as db:
        data = get_all_stations(db)

    response = {
        "success": True,
        "data": data,
    }

    redis_client.set(cache_key, response, ANALYTICS_CACHE_TTL)
    return response


@router.get("/stations/search")
def station_search(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, le=20),
):
    cache_key = f"analytics:station-search:{q.lower()}:{limit}"

    cached = redis_client.get(cache_key)
    if cached is not None:
        return cached

    with get_db() as db:
        data = search_stations(db, q, limit)

    response = {
        "success": True,
        "data": data,
    }

    redis_client.set(cache_key, response, ANALYTICS_CACHE_TTL)
    return response


@router.get("/stations/{code}")
def station_detail(code: str):
    cache_key = f"analytics:station:{code.upper()}"

    cached = redis_client.get(cache_key)
    if cached is not None:
        return cached

    with get_db() as db:
        station = get_station_by_code(db, code)

    if station is None:
        return {
            "success": False,
            "error": f"Station '{code.upper()}' not found."
        }

    response = {
        "success": True,
        "data": station.to_dict(),
    }

    redis_client.set(cache_key, response, ANALYTICS_CACHE_TTL)
    return response


@router.get("/cache")
def cache_metrics():
    return {
        "success": True,
        "data": redis_client.get_metrics(),
    }