from fastapi import APIRouter, Query
from app.services.graph_service import find_routes

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
    return find_routes(source, destination, max_routes)


@router.get("/stations")
def list_stations():
    from app.services.graph_service import graph

    return {
        code: data
        for code, data in graph.nodes(data=True)
    }