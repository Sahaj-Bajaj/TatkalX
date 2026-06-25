"""
database/models.py
──────────────────
ORM models — four tables, all with proper indexes and constraints.

Tables:
  stations        — 100 seeded Indian railway stations
  search_history  — every route search logged
  predictions     — every delay prediction logged with SHAP values
  api_metrics     — latency and status per endpoint (for dashboard)
"""

import json
from datetime import datetime

from sqlalchemy import (
    Boolean, CheckConstraint, Column, DateTime, Float,
    Index, Integer, String, Text, func,
)
from sqlalchemy.orm import relationship, validates

from .connection import Base


# ── Station ───────────────────────────────────────────────────────────────────
class Station(Base):
    __tablename__ = "stations"

    id           = Column(Integer, primary_key=True, index=True)
    station_code = Column(String(10), unique=True, nullable=False)
    station_name = Column(String(150), nullable=False)
    city         = Column(String(100))
    state        = Column(String(100))
    zone         = Column(String(20))           # NR, WR, SR, ER, etc.
    latitude     = Column(Float)
    longitude    = Column(Float)
    is_major     = Column(Boolean, default=False)
    created_at   = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("idx_station_code", "station_code"),
        Index("idx_station_city", "city"),
        Index("idx_station_state", "state"),
    )

    def to_dict(self):
        return {
            "id":           self.id,
            "code":         self.station_code,
            "name":         self.station_name,
            "city":         self.city,
            "state":        self.state,
            "zone":         self.zone,
            "latitude":     self.latitude,
            "longitude":    self.longitude,
            "is_major":     self.is_major,
        }

    def __repr__(self):
        return f"<Station {self.station_code} — {self.station_name}>"


# ── SearchHistory ─────────────────────────────────────────────────────────────
class SearchHistory(Base):
    __tablename__ = "search_history"

    id                      = Column(Integer, primary_key=True, index=True)
    source_station_code     = Column(String(10), nullable=False)
    destination_station_code= Column(String(10), nullable=False)
    path                    = Column(Text)          # JSON array of station codes
    path_found              = Column(Boolean, default=True)
    total_distance_km       = Column(Float)
    total_duration_minutes  = Column(Integer)
    stops_count             = Column(Integer)
    algorithm_used          = Column(String(20), default="dijkstra")
    query_time_ms           = Column(Float)
    created_at              = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("idx_sh_source",      "source_station_code"),
        Index("idx_sh_destination", "destination_station_code"),
        Index("idx_sh_created",     "created_at"),
        # Composite — used by popular routes query
        Index("idx_sh_route",       "source_station_code", "destination_station_code"),
    )

    def get_path_list(self):
        """Return path as a Python list."""
        if self.path:
            return json.loads(self.path)
        return []

    def to_dict(self):
        return {
            "id":          self.id,
            "source":      self.source_station_code,
            "destination": self.destination_station_code,
            "path":        self.get_path_list(),
            "path_found":  self.path_found,
            "distance_km": self.total_distance_km,
            "duration_min":self.total_duration_minutes,
            "stops":       self.stops_count,
            "algorithm":   self.algorithm_used,
            "time_ms":     self.query_time_ms,
            "searched_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return (
            f"<Search {self.source_station_code}→{self.destination_station_code} "
            f"({'found' if self.path_found else 'not found'})>"
        )


# ── Prediction ────────────────────────────────────────────────────────────────
class Prediction(Base):
    __tablename__ = "predictions"

    id                       = Column(Integer, primary_key=True, index=True)
    source_station_code      = Column(String(10))
    destination_station_code = Column(String(10))
    train_number             = Column(String(20))
    departure_hour           = Column(Integer)
    day_of_week              = Column(Integer)   # 0=Monday, 6=Sunday
    month                    = Column(Integer)
    distance_km              = Column(Float)
    delay_probability        = Column(Float, nullable=False)    # 0.0 – 100.0
    delay_minutes_predicted  = Column(Integer)
    feature_importance       = Column(Text)      # JSON of SHAP values
    model_version            = Column(String(20), default="1.0.0")
    query_time_ms            = Column(Float)
    created_at               = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("delay_probability >= 0 AND delay_probability <= 100",
                        name="ck_probability_range"),
        CheckConstraint("departure_hour >= 0 AND departure_hour <= 23",
                        name="ck_hour_range"),
        CheckConstraint("day_of_week >= 0 AND day_of_week <= 6",
                        name="ck_dow_range"),
        CheckConstraint("month >= 1 AND month <= 12",
                        name="ck_month_range"),
        Index("idx_pred_source",      "source_station_code"),
        Index("idx_pred_destination", "destination_station_code"),
        Index("idx_pred_created",     "created_at"),
        Index("idx_pred_probability", "delay_probability"),
    )

    def get_shap_values(self):
        """Return SHAP feature importance as a Python dict."""
        if self.feature_importance:
            return json.loads(self.feature_importance)
        return {}

    @validates("delay_probability")
    def validate_probability(self, key, value):
        if not (0.0 <= float(value) <= 100.0):
            raise ValueError(f"delay_probability must be 0–100, got {value}")
        return value

    def to_dict(self):
        return {
            "id":              self.id,
            "source":          self.source_station_code,
            "destination":     self.destination_station_code,
            "train_number":    self.train_number,
            "departure_hour":  self.departure_hour,
            "day_of_week":     self.day_of_week,
            "month":           self.month,
            "distance_km":     self.distance_km,
            "delay_probability": round(self.delay_probability, 2),
            "delay_minutes":   self.delay_minutes_predicted,
            "shap_values":     self.get_shap_values(),
            "model_version":   self.model_version,
            "time_ms":         self.query_time_ms,
            "predicted_at":    self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return (
            f"<Prediction {self.source_station_code}→{self.destination_station_code} "
            f"{self.delay_probability:.1f}%>"
        )


# ── APIMetric ─────────────────────────────────────────────────────────────────
class APIMetric(Base):
    """
    Tracks response time and status for every API endpoint.
    Powers the 'System Performance' panel in the analytics dashboard.
    """
    __tablename__ = "api_metrics"

    id            = Column(Integer, primary_key=True, index=True)
    endpoint      = Column(String(100), nullable=False)   # e.g. "/api/route/search"
    method        = Column(String(10), default="GET")
    status_code   = Column(Integer, nullable=False)
    response_ms   = Column(Float, nullable=False)
    created_at    = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index("idx_metric_endpoint", "endpoint"),
        Index("idx_metric_created",  "created_at"),
        Index("idx_metric_status",   "status_code"),
    )

    def to_dict(self):
        return {
            "id":          self.id,
            "endpoint":    self.endpoint,
            "method":      self.method,
            "status_code": self.status_code,
            "response_ms": self.response_ms,
            "recorded_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<APIMetric {self.method} {self.endpoint} {self.status_code} {self.response_ms:.1f}ms>"
