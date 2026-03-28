from sgp4.api import Satrec, WGS72, jday
from datetime import datetime, timezone
import numpy as np

from tle_parser import TLE


def build_satellite(tle: TLE) -> Satrec:
    return Satrec.twoline2rv(tle.line1, tle.line2)


def propagate(tle: TLE, times: list[datetime]) -> list[dict]:
    satellite = build_satellite(tle)
    results = []

    for t in times:
        jd, fr = jday(t.year, t.month, t.day, t.hour, t.minute, t.second)
        error, position, velocity = satellite.sgp4(jd, fr)

        if error != 0:
            print(f'SGP4 error code {error} at {t}')
            continue

        results.append({
            'time': t,
            'x': position[0],
            'y': position[1],
            'z': position[2],
            'vx': velocity[0],
            'vy': velocity[1],
            'vz': velocity[2],
        })

    return results
