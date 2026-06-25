import time

from starlette.middleware.base import BaseHTTPMiddleware

from database.connection import SessionLocal
from database.operations import log_api_metric


class APIMetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.perf_counter()

        response = await call_next(request)

        response_ms = (time.perf_counter() - start_time) * 1000

        db = SessionLocal()

        try:
            log_api_metric(
                db=db,
                endpoint=request.url.path,
                method=request.method,
                status_code=response.status_code,
                response_ms=response_ms,
            )
            db.commit()
        except Exception:
            db.rollback()
        finally:
            db.close()

        return response