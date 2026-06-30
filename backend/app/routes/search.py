from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.core.redis import redis_client
from app.services.graph_service import find_routes
from database.connection import get_db
from database.connection import get_db_dependency
from database.operations import log_search, get_all_stations

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)

STATIONS_CACHE_KEY = "stations:all"
STATIONS_CACHE_TTL = 86400  # 24 hours

ROUTES_CACHE_TTL = 3600  # 1 hour


@router.get("/routes")
def get_routes(
    source: str = Query(..., description="Station code e.g. NDLS"),
    destination: str = Query(..., description="Station code e.g. MMCT"),
    max_routes: int = Query(3, ge=1, le=5),
):
    cache_key = f"routes:{source}:{destination}:{max_routes}"

    # Try Redis first
    try:
        result = redis_client.get(cache_key)
    except Exception:
        result = None

    if result is None:
        # Cache miss → compute routes
        result = find_routes(source, destination, max_routes)

        # Cache only successful responses
        if "error" not in result:
            try:
                redis_client.set(
                    cache_key,
                    result,
                    ROUTES_CACHE_TTL
                )
            except Exception:
                pass

    # Always log the search for analytics
    if "routes" in result and result["routes"]:
        best_route = result["routes"][0]

        with get_db() as db:
            log_search(
                db=db,
                source_code=source,
                destination_code=destination,
                path=best_route["path"],
                total_distance_km=best_route["total_distance_km"],
                total_duration_minutes=int(best_route["total_duration_hrs"] * 60),
                stops_count=best_route["stops"],
                algorithm_used="yen_k_shortest_paths"
            )

    return result


# In backend/app/routes/search.py — replace the list_stations() function
# with this version. Only change: filter the DB result down to station
# codes that actually exist in the route graph, so the dropdown never
# offers a station that /search/routes can't reach.

from app.services.graph_service import graph as route_graph


@router.get("/stations")
def list_stations(db: Session = Depends(get_db_dependency)):
    # Try Redis first
    try:
        cached_stations = redis_client.get(STATIONS_CACHE_KEY)
    except Exception:
        cached_stations = None

    if cached_stations is not None:
        return cached_stations

    # Load from PostgreSQL
    stations = get_all_stations(db)

    # Only expose stations that exist in the route graph —
    # keeps the dropdown and /search/routes in sync.
    routable_codes = set(route_graph.nodes)

    response = {
        station["code"]: {
            "name": station["name"],
            "city": station["city"],
        }
        for station in stations
        if station["code"] in routable_codes
    }

    # Store in Redis (ignore cache failures)
    try:
        redis_client.set(
            STATIONS_CACHE_KEY,
            response,
            STATIONS_CACHE_TTL
        )
    except Exception:
        pass

    return response