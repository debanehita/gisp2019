import gdal_workaround
import pyproj
from fiona.crs import from_epsg

lat = 53.0
lon = -8.5

WGS84  = pyproj.Proj(from_epsg(4326))
IRISH_GRID = pyproj.Proj(from_epsg(29902))

x,y = pyproj.transform(WGS84, IRISH_GRID, lon, lat)

print("Turned Lat: {}, Lon: {} into IG Easting: {}, Northing: {}".format(lat, lon, x, y))

