import gdal_workaround
import fiona
from fiona.crs import from_epsg
import pyproj

SOURCE_EPSG = 29902
DEST_EPSG = 4326

SOURCE_PROJ = pyproj.Proj(from_epsg(SOURCE_EPSG))
DEST_PROJ = pyproj.Proj(from_epsg(DEST_EPSG))

SOURCE = "settlements/stgeom.shp"
NEW_SHP = ".cache/settlements_modified.shp"
NEW_JSON = ".cache/settlements_modified.json"


def transform_coordinates(coordinates):
    outgoing_geom = {}
    outgoing_geom["coordinates"] = []

    l1_out = []
    for l1 in item["geometry"]["coordinates"]:
        l2_out = []
        for l2 in l1:
            # for pair in l2:
            x, y = l2
            lon, lat = pyproj.transform(SOURCE_PROJ, DEST_PROJ, x, y)
            l1_out.append((lon, lat))
            # l1_out.append(l2_out)
        outgoing_geom["coordinates"].append(l1_out)

    return outgoing_geom


with fiona.open(SOURCE) as source:
    pop_densities = []
    sink_schema = {'properties': {
        'settlement': 'str:254', 'settl_name': 'str:254'}, 'geometry': source.schema["geometry"]}

    print("*" * 50)
    print("File Type is {}".format(source.driver))
    print("Number of features is {}".format(len(source)))
    print("SRS (EPSG) is {}".format(source.crs["init"].split(":")[1]))
    print("Schema is {}".format(source.schema))
    print("*" * 50)

    # {"type":"Feature","id":"ctygeom.C33","geometry":{"type":"MultiPolygon","coordinates":[]}"geometry_name":"geom",
    # "properties":{}}],"crs":{"type":"EPSG","properties":{"code":"4326"}}}
    geo_json = {"type": "FeatureCollection", "features": [], "crs": {"type": "EPSG", "properties": {"code": "29902"}}}
    geo_json_id = 0

    with fiona.open(
            NEW_SHP, 'w',
            # crs=from_epsg(29902),
            crs=source.crs,
            driver=source.driver,
            schema=sink_schema,
    ) as sink:
        for item in source:
            pop_densities.append(
                (item["properties"]["total2011"] / item["properties"]["area2011"], item["properties"]["settl_name"]))
            print("{} - {:5.2f}".format(pop_densities[-1][1], pop_densities[-1][0]))

            feature = {}
            feature["geometry"] = {}
            feature["geometry"]["type"] = item["geometry"]["type"]
            feature["geometry"]["coordinates"] = item["geometry"]["coordinates"]
            # feature["geometry"]["coordinates"] = transformCoordinates(item["geometry"]["coordinates"])
            feature["properties"] = {}

            for i in sink_schema["properties"].keys():
                feature["properties"][i] = item["properties"][i]
            sink.write(feature)

            # Add to geoJSON - i.e. make new feature
            geo_json_id += 1
            geo_json_feature = {"type": "Feature", "id": geo_json_id,
                                "geometry": {"type": "MultiPolygon", "coordinates": []},
                                "properties": {}}

            geo_json_feature["properties"] = feature["properties"]
            geo_json_feature["geometry"]["type"] = item["geometry"]["type"]
            geo_json_feature["geometry"]["coordinates"] = feature["geometry"]["coordinates"]

            geo_json["features"].append(geo_json_feature)

max_density = sorted(pop_densities, reverse=True)[0]
min_density = sorted(pop_densities, reverse=False)[0]

print("*" * 50)
print("Highest Pop Den: {} -- {:5.2f}".format(max_density[1], max_density[0]))
print("Lowest Pop Den: {} -- {:5.2f}".format(min_density[1], min_density[0]))
print("*" * 50)
