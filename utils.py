"""
Created on Oct 24, 2015

@author: ionut
"""

import json


def gps_to_json(positions):
    """
    Transform GPS data to web format (time data to seconds since epoch)
    :param positions: position data received from bbgps
    :return: json data to return on request
    """
    data = []
    for position in positions:
        aux = position.copy()
        aux["time"] = int(aux["time"].strftime("%s"))
        data.append(aux)
    return json.dumps(data)


def convert_projection(lng, lat, src_proj="+init=EPSG:4326", dst_proj="+init=EPSG:31700"):
    """
    Convert coordinates from src_proj to dst_proj
    :param lng: longitude
    :param lat: latitude
    :param src_proj: source projection
    :param dst_proj: destination projection
    """
    lng = float(lng)
    lat = float(lat)
    import pyproj
    return pyproj.transform(pyproj.Proj(src_proj), pyproj.Proj(dst_proj), lng, lat)


def main():
    """
    Test coordinate transform function with sample data
    """
    longitude = 25.0
    latitude = 46.0
    longitude1, latitude1 = convert_projection(longitude, latitude)
    print("input [%.5f, %.5f], output [%.5f, %.5f]" % (longitude, latitude, longitude1, latitude1))


if __name__ == "__main__":
    main()
