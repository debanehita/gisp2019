try:
    import pyproj
    from fiona.crs import from_epsg, from_string, to_string
except ImportError as e:
    print("ERROR: {}".format(e))
    quit(1)
except Exception as e:
    print("ERROR: {}".format(e))
    quit(2)


def transform_coordinates(souce_srs, target_srs, source_coord_pair):
    """
    Generic function to transform a coordinate pair from one CRS to any other.

    Mark Foley
    Feb 2019

    :param souce_srs: The srs that you want to convert FROM. This can be in proj4 format or can be an EPSG code.
    :param target_srs: The srs that you want to convert TO. This can be in proj4 format or can be an EPSG code. When
    using an epsg code pass in a sting in the format "epsg:nn" where nn is the code number, e.g "epsg:4326"
    :param source_coord_pair: a list or tuple containing the incoming coordinate pair in the format LON,LAT or X,Y
    :return: The coordinate pair transformed to the target SRS as a LON, LAT or X, Y tuple.
    """

    proj = []
    try:
        for srs in (souce_srs, target_srs):
            if type(srs) == str:
                srs_split = srs.split(":")
                if srs_split[0].lower() == "epsg":
                    proj.append(pyproj.Proj(init=srs))
                else:
                    proj.append(pyproj.Proj(srs))
            elif type(srs) == dict and "proj" in srs:
                srs = to_string(srs)
                proj.append(pyproj.Proj(srs))
            else:
                raise ValueError("SRS must be string or dictionary")

        return pyproj.transform(proj[0], proj[1], source_coord_pair[0], source_coord_pair[1])

    except ValueError as e:
        print("ERROR: {}".format(e))
        quit(3)
    except Exception as e:
        print("ERROR: {}".format(e))
        quit(4)


if __name__ == "__main__":
    # main() used for testing only.

    # src is EPSG 29903
    src_srs = {'proj': 'tmerc', 'lat_0': 53.5, 'lon_0': -8, 'k': 1.000035, 'x_0': 200000, 'y_0': 250000,
               'ellps': 'mod_airy', 'units': 'm', 'no_defs': True}
    trg_srs = "epsg:4326"
    src_coords = (300000, 250000)
    result = transform_coordinates(src_srs, trg_srs, src_coords)
    print("SOURCE SRS: {}\nTARGET SRS: {}\nSOURCE COORDINATES: {}\nTRANSFORMED COORDINATES: {}"
          .format(src_srs, trg_srs, src_coords, result))
