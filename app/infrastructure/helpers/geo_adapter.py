
from typing import Optional

try:
    from geoalchemy2.shape import from_shape
    from shapely.geometry import Point
    HAS_GEO = True
except ImportError:
    HAS_GEO = False


def to_postgis_point(latitude: float, longitude: float):

    if not HAS_GEO:
        return None

    try:

        point = Point(longitude, latitude)
        return from_shape(point, srid=4326)
    except:
        return None


def parse_location(location_dict: Optional[dict]):

    if not location_dict:
        return None

    try:
        lat = float(location_dict.get("latitude"))
        lon = float(location_dict.get("longitude"))
        return to_postgis_point(lat, lon)
    except:
        return None
