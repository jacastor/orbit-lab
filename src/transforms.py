import numpy as np


def eci_to_lla(x: float, y: float, z: float, gst: float) -> dict:
    """
    Convert ECI coordinates to latitude, longitude, altitude.

    Args:
        x, y, z: ECI position in km
        gst: Greenwich Sidereal Time in radians

    Returns:
        dict with lat, lon, alt
    """
    R_EARTH = 6378.137
    e2 = 0.00669437999014

    lon = np.arctan2(y, x) - gst
    lon = (np.degrees(lon) + 360) % 360
    if lon > 180:
        lon -= 360

    r = np.sqrt(x**2 + y**2)
    lat = np.arctan2(z, r)

    for _ in range(5):
        sin_lat = np.sin(lat)
        N = R_EARTH / np.sqrt(1 - e2 * sin_lat**2)
        lat = np.arctan2(z + e2 * N * sin_lat, r)

    lat = np.degrees(lat)
    sin_lat = np.sin(np.radians(lat))
    N = R_EARTH / np.sqrt(1 - e2 * sin_lat**2)
    alt = r / np.cos(np.radians(lat)) - N

    return {'lat': lat, 'lon': lon, 'alt': alt}


def gst_from_jd(jd: float, fr: float) -> float:
    """
    Compute Greenwich Sidereal Time from Julian date.

    Args:
        jd: Julian date
        fr: fractional day

    Returns:
        GST in radians
    """
    T = ((jd + fr) - 2451545.0) / 36525.0
    gst = (67310.54841
           + (876600 * 3600 + 8640184.812866) * T
           + 0.093104 * T**2
           - 6.2e-6 * T**3)
    gst = np.radians(gst / 240.0 % 360.0)
    return gst
