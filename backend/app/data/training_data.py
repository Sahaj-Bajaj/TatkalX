import numpy as np
import pandas as pd


def generate_synthetic_data(n_samples: int = 10000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    days_before     = rng.integers(1, 61, n_samples)
    travel_class    = rng.integers(0, 4, n_samples)   # 0=SL, 1=3A, 2=2A, 3=1A
    day_of_week     = rng.integers(0, 7, n_samples)
    month           = rng.integers(1, 13, n_samples)
    route_popularity = rng.integers(1, 6, n_samples)  # 1=quiet, 5=very busy
    is_tatkal       = rng.integers(0, 2, n_samples)
    hour_of_booking = rng.integers(0, 24, n_samples)

    availability = np.ones(n_samples) * 0.75

    # Fewer days before → harder to get (exponential drop)
    availability -= 0.3 * np.exp(-days_before / 10)

    # Tatkal opens 1 day before; availability is much lower
    tatkal_penalty = is_tatkal * (0.35 - 0.04 * days_before.clip(1, 5))
    availability -= tatkal_penalty.clip(0, 0.35)

    # SL fills fastest; 1A usually has space
    class_effect = np.array([-0.2, -0.08, 0.05, 0.18])
    availability += class_effect[travel_class]

    # Fri/Sat/Sun are busier
    is_weekend = (day_of_week >= 4).astype(float)
    availability -= is_weekend * 0.1

    # Peak seasons: Oct–Jan (festivals + winter) and May–Jun (summer vacation)
    is_peak = (
        (month >= 10) | (month <= 1) |
        ((month >= 5) & (month <= 6))
    ).astype(float)
    availability -= is_peak * 0.1

    # Busier routes → lower availability
    availability -= (route_popularity - 1) * 0.06

    # Tatkal opens at 10 AM — first hour is most contested
    tatkal_rush = is_tatkal * (hour_of_booking == 10).astype(float) * 0.15
    availability -= tatkal_rush

    # Realistic noise
    availability += rng.normal(0, 0.05, n_samples)
    availability = availability.clip(0.0, 1.0)

    return pd.DataFrame({
        "days_before_journey": days_before,
        "travel_class":        travel_class,
        "day_of_week":         day_of_week,
        "month":               month,
        "route_popularity":    route_popularity,
        "is_tatkal":           is_tatkal,
        "hour_of_booking":     hour_of_booking,
        "availability_prob":   availability,
    })