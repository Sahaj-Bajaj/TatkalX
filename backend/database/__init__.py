"""
database/__init__.py
────────────────────
Clean public API for the database package.
Your routes only need one import line:

    from database import get_db, log_search, log_prediction, get_full_analytics
"""

from .connection import get_db, get_db_dependency, check_connection, engine, Base
from .models import Station, SearchHistory, Prediction, APIMetric
from .operations import (
    # Stations
    get_station_by_code,
    get_all_stations,
    search_stations,
    get_stations_by_state,
    # Search history
    log_search,
    get_recent_searches,
    get_searches_between,
    # Predictions
    log_prediction,
    get_recent_predictions,
    # Analytics
    get_summary,
    get_popular_routes,
    get_search_volume_trend,
    get_peak_search_hours,
    get_prediction_distribution,
    get_high_risk_routes,
    get_prediction_trend,
    get_weekday_stats,
    get_full_analytics,
    # API metrics
    log_api_metric,
    get_endpoint_performance,
)

__all__ = [
    "get_db", "get_db_dependency", "check_connection", "engine", "Base",
    "Station", "SearchHistory", "Prediction", "APIMetric",
    "get_station_by_code", "get_all_stations", "search_stations", "get_stations_by_state",
    "log_search", "get_recent_searches", "get_searches_between",
    "log_prediction", "get_recent_predictions",
    "get_summary", "get_popular_routes", "get_search_volume_trend",
    "get_peak_search_hours", "get_prediction_distribution",
    "get_high_risk_routes", "get_prediction_trend", "get_weekday_stats",
    "get_full_analytics",
    "log_api_metric", "get_endpoint_performance",
]
