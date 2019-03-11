import json, datetime
from geopy.geocoders import Nominatim
# from urllib.request import Request
geolocator = Nominatim()
import pyproj
from fiona.crs import from_epsg


def geocode_address(address=""):
    """
    Address geocoder using OSM Nominatim. Accepts 'address' string and returns a JSON response containing
    everything that the geocoder provides.

    :param address: Address to be geocoded
    :return: JSON response
    """
    body = {}

    try:
        if not address:
            raise Exception("No address supplied")

        loc = geolocator.geocode(address, addressdetails=True)

        if not loc:
            raise Exception("No result found for '{}'".format(address))

        body["message"] = "Called 'geocode_address'. OK! {}".format(datetime.datetime.now())
        body["input_address"] = address
        body["result"] = loc.raw

        response = {
            "body": body
        }
    except Exception as e:
        body["error"] = "{} - {}".format(e, datetime.datetime.now())
        response = {
            "body": body
        }

    return response


def geocode_location(location="", epsg=4326):
    """
    Address geocoder using OSM Nominatim. Accepts 'location' string in lat, lon format and returns a
    JSON response containing everything that the geocoder provides.

    :param location: string in lat, lon
    :param epsg: EPSG code of input coordinates, these will be converted to EPSG:4326
    :return: JSON response
    """
    body = {}

    # set the input projection of the original file.
    input_projection = pyproj.Proj(from_epsg(epsg))
    # set the projection for the output file.
    output_projection = pyproj.Proj(from_epsg(4326))

    try:
        if not location:
            raise Exception("No location supplied")

        if epsg != 4326:
            lon, lat = pyproj.transform(
                input_projection, output_projection, float(location.strip().split(",")[0]), float(location.strip().split(",")[1])
            )
        else:
            lon, lat = float(location.strip().split(",")[1]), float(location.strip().split(",")[0])

        loc = geolocator.reverse("{}, {}".format(lat, lon))

        if not loc:
            raise Exception("No result found for '{}'".format(location))

        body["message"] = "Called 'geocode_location'. OK! {}".format(datetime.datetime.now())
        body["input_location"] = location
        body["result"] = loc.raw

        response = {
            "body": body
        }
    except Exception as e:
        body["error"] = "{} - {}".format(e, datetime.datetime.now())
        response = {
            "body": body
        }

    return response

## Looks like this has been fixed in the latest version of geopy - MF, March 2019
# def get_geolocator():
#     """
#     Horrible hack to get around spurious geopy error (bugs #262 and #185):
#     "geocoders.base.Geocoder._call_geocoder() does not sent HTTP headers breaking Nominatim usage"
#
#     :return: corrected geolocator object
#     """
#
#     geolocator = Nominatim()
#
#     requester = geolocator.urlopen
#
#     def requester_hack(req, **kwargs):
#         req = Request(url=req, headers=geolocator.headers)
#         return requester(req, **kwargs)
#
#     geolocator.urlopen = requester_hack
#
#     return geolocator


def main():
    my_address = "Drumcondra, Dublin, Ireland"
    result = geocode_address(my_address)
    print(result)
    my_location = "53.33, -6.33"
    result = geocode_location(my_location)
    print(result)
    my_location = "255000.0, 333000"
    result = geocode_location(my_location, 29902)
    print(result)


if __name__ == "__main__":
    main()
