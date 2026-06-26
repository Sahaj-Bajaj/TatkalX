from fastapi import APIRouter, Query

from app.services.prediction_service import predict_availability
from database.connection import get_db
from database.operations import log_prediction

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.get("/availability")
def get_availability(
    source: str = Query(..., description="Station code e.g. NDLS"),
    destination: str = Query(..., description="Station code e.g. BCT"),
    days_before: int = Query(..., ge=1, le=120, description="Days before journey date"),
    travel_class: str = Query("SL", description="SL, 3A, 2A, or 1A"),
    day_of_week: int = Query(..., ge=0, le=6, description="0=Mon, 6=Sun"),
    month: int = Query(..., ge=1, le=12),
    is_tatkal: bool = Query(False),
    hour_of_booking: int = Query(
        10,
        ge=0,
        le=23,
        description="Hour you plan to book (24hr)",
    ),
):
    result = predict_availability(
        source=source,
        destination=destination,
        days_before=days_before,
        travel_class=travel_class,
        day_of_week=day_of_week,
        month=month,
        is_tatkal=is_tatkal,
        hour_of_booking=hour_of_booking,
    )

    with get_db() as db:
        log_prediction(
            db=db,
            source_code=source,
            destination_code=destination,
            availability_probability =result["availability_probability"],
            inputs={
                "departure_hour": hour_of_booking,
                "day_of_week": day_of_week,
                "month": month,
            },
            shap_values=result["feature_importance"],
            model_version="1.0.0",
        )

    return result