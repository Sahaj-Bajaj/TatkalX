from fastapi import APIRouter, Query
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
@router.get("")
def analytics_dashboard():
    with get_db() as db:
        data = get_full_analytics(db)

    return {
        "success": True,
        "data": data,
    }

@router.get("/summary")
def analytics_summary():
    with get_db() as db:
        data = get_summary(db)

    return {
        "success": True,
        "data": data,
    }

@router.get("/popular")
def popular_routes(limit: int = Query(10, le=50)):
    with get_db() as db:
        data = get_popular_routes(db, limit=limit)

    return {
        "success": True,
        "data": data,
    }


@router.get("/trend")
def search_trend(days: int = Query(30, le=365)):
    with get_db() as db:
        data = get_search_volume_trend(db, days=days)

    return {
        "success": True,
        "data": data,
    }


@router.get("/peak-hours")
def peak_hours():
    with get_db() as db:
        data = get_peak_search_hours(db)

    return {
        "success": True,
        "data": data,
    }


@router.get("/risk")
def high_risk_routes(
    limit: int = Query(10, le=50),
    min_predictions: int = Query(2, ge=1),
):
    with get_db() as db:
        data = get_high_risk_routes(
            db,
            limit=limit,
            min_predictions=min_predictions,
        )

    return {
        "success": True,
        "data": data,
    }


@router.get("/weekdays")
def weekday_stats():
    with get_db() as db:
        data = get_weekday_stats(db)

    return {
        "success": True,
        "data": data,
    }


@router.get("/health")
def analytics_health(hours: int = Query(24, le=720)):
    with get_db() as db:
        performance = get_endpoint_performance(db, hours=hours)

    return {
        "success": True,
        "data": {
            "db_online": check_connection(),
            "window_hours": hours,
            "endpoints": performance,
        },
    }


@router.get("/stations")
def all_stations():
    with get_db() as db:
        data = get_all_stations(db)

    return {
        "success": True,
        "data": data,
    }


@router.get("/stations/search")
def station_search(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, le=20),
):
    with get_db() as db:
        data = search_stations(db, q, limit)

    return {
        "success": True,
        "data": data,
    }


@router.get("/stations/{code}")
def station_detail(code: str):
    with get_db() as db:
        station = get_station_by_code(db, code)

    if station is None:
        return {
            "success": False,
            "error": f"Station '{code.upper()}' not found."
        }

    return {
        "success": True,
        "data": station.to_dict(),
    }