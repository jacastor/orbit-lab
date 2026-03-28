import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from datetime import datetime, timezone, timedelta
from sgp4.api import jday
import sys
sys.path.insert(0, 'src')
from tle_parser import parse_tle
from propagator import propagate
from transforms import eci_to_lla, gst_from_jd


RAW_TLE = """ISS (ZARYA)
1 25544U 98067A   24001.50000000  .00002182  00000-0  40768-4 0  9990
2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.50377579404740"""


def get_ground_track(raw_tle: str, minutes: int = 92) -> list[dict]:
    tle = parse_tle(raw_tle)
    start = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    times = [start + timedelta(seconds=60*i) for i in range(minutes)]
    results = propagate(tle, times)

    track = []
    for r in results:
        t = r['time']
        jd, fr = jday(t.year, t.month, t.day, t.hour, t.minute, t.second)
        gst = gst_from_jd(jd, fr)
        lla = eci_to_lla(r['x'], r['y'], r['z'], gst)
        track.append(lla)

    return track


def plot_ground_track(track: list[dict]) -> None:
    lats = [p['lat'] for p in track]
    lons = [p['lon'] for p in track]

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_facecolor('#0d1b2a')
    fig.patch.set_facecolor('#0d1b2a')

    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.set_xlabel('Longitude', color='white')
    ax.set_ylabel('Latitude', color='white')
    ax.tick_params(colors='white')
    ax.set_title('ISS Ground Track — One Orbit', color='white', fontsize=14)

    ax.plot(lons, lats, color='#00d4ff', linewidth=1.5, label='Ground Track')
    ax.plot(lons[0], lats[0], 'o', color='#00ff88', markersize=8, label='Start')
    ax.plot(lons[-1], lats[-1], 'o', color='#ff4444', markersize=8, label='End')

    ax.gridlines = ax.grid(color='white', alpha=0.1)
    ax.legend(facecolor='#0d1b2a', labelcolor='white')

    plt.tight_layout()
    plt.savefig('ground_track.png', dpi=150, bbox_inches='tight')
    plt.show()
    print('Saved to ground_track.png')


if __name__ == '__main__':
    track = get_ground_track(RAW_TLE)
    plot_ground_track(track)
