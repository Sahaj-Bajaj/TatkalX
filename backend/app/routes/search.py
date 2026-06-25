from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.services.graph_service import find_routes
from database.connection import get_db
from database.connection import get_db_dependency
from database.operations import log_search, get_all_stations

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get("/routes")
def get_routes(
    source: str = Query(..., description="Station code e.g. NDLS"),
    destination: str = Query(..., description="Station code e.g. BCT"),
    max_routes: int = Query(3, ge=1, le=5),
):
    result = find_routes(source, destination, max_routes)

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


@router.get("/stations")
def list_stations(db: Session = Depends(get_db_dependency)):
    stations = get_all_stations(db)

    return {
        station["code"]: {
            "name": station["name"],
            "city": station["city"],
        }
        for station in stations
    }