"""
Geocode an address list and save it as shapefile

Source document is a csv with names & addresses but NOT co-ordinates

Steps
1. Read csv
2. For each address use 'geopy' to geocode the address. This is the process of finding a co-ordinate pair to
match an address.
3. Write a new csv with the lat/lon included as two fields
4. Read the NEW csv and write a new shapefile with each lat/lon pair as Point geometry.
"""
import fiona
import geopy_corrected as gp
import json
import csv
from geopy.geocoders import Nominatim
from fiona.crs import from_epsg

geolocator = Nominatim()

INPUT_CSV = "geoname_pop5000.csv"
OUTPUT_CSV = ".cache/geoname_pop5000_geocoded.csv"
OUTPUT_SHP = ".cache/geoname_pop5000_geocoded.shp"


def geocode_csv():
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as out_csv:
        with open(INPUT_CSV, 'r', encoding='utf-8') as in_csv:
            reader = csv.DictReader(in_csv)
            output_fieldnames = reader.fieldnames + ["derived_latitude", "derived_longitude", "derived_address"]
            writer = csv.DictWriter(out_csv, fieldnames=output_fieldnames, delimiter='\t')
            writer.writeheader()
            for row in reader:
                try:
                    # Get coordinates from address (asciiname)
                    geocode_answer = gp.geocode_address(row["asciiname"])
                    # result = json.loads(result["body"])
                    location_coords = geocode_answer["body"]["result"]
                    row["derived_latitude"] = location_coords["lat"]
                    row["derived_longitude"] = location_coords["lon"]
                    geocode_answer = gp.geocode_location("{}, {}".format(row["latitude"], row["longitude"]))
                    # result = json.loads(result["body"])
                    location_reverse = geocode_answer["body"]["result"]
                    row["derived_address"] = location_reverse["display_name"]
                except:
                    row["derived_latitude"] = row["derived_longitude"] = row["derived_address"] = ""
                writer.writerow(row)


def make_shp_from_csv():
    with open(OUTPUT_CSV, 'r', encoding='utf-8') as out_csv:
        reader = csv.DictReader(out_csv, delimiter='\t')
        my_schema = {"geometry": "Point", "properties": {}}
        for item in reader.fieldnames:
            my_schema["properties"][item] = "str"

        with fiona.open(OUTPUT_SHP, "w", crs=from_epsg(4326), schema=my_schema, driver="ESRI Shapefile", encoding='utf-8') as target:
            for row in reader:
                try:
                    target_feature = {}
                    target_feature["geometry"] = \
                        {
                            "type": "Point",
                            "coordinates": [float(row["derived_longitude"]), float(row["derived_latitude"])]
                        }
                    target_feature["properties"] = {}
                    for k, v in row.items():
                        target_feature["properties"][k] = row[k]
                    target.write(target_feature)
                except:
                    pass


def main():
    geocode_csv()
    make_shp_from_csv()


if __name__ == "__main__":
    main()
