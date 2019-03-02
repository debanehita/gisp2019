"""
OrderedDict is just a dictionary that preserves the order in which the keys were created. You can use any of the
standard dictionary methods in the usual way.

MF
March 2019
"""

from collections import OrderedDict

file_extensions = OrderedDict({
    'AeronavFAA': None,
    'ARCGEN': None,
    'BNA': None,
    'DXF': 'dxf',
    'CSV': 'csv',
    'OpenFileGDB': None,
    'ESRI Shapefile': 'shp',
    'GeoJSON': 'json',
    'GPKG': 'gpkg',
    'GML': 'gml',
    'GPX': 'gpx',
    'GPSTrackMaker': None,
    'Idrisi': None,
    'MapInfo File': 'tab',
    'DGN': None,
    'S57': None,
    'SEGY': None,
    'SUA': None
})
