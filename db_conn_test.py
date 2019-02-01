"""
This program implements functions to get a data source from either a PostgreSQL database or a geoserver instance (GeoJSON)
"""

def get_data_from_postgres(conn, qry):
    """

    Gets a list of 'DictRows' from a PostgreSQL database. A DictRow can be indexed numerically or by column name, In other
    words it behaves like a list OR a dictionary object.

    :param conn: The database connection string
    :param qry: The SQL query which gets the data
    :return: The result set.
    """
    import psycopg2
    import psycopg2.extras
    try:
        my_conn = psycopg2.connect(conn)
        cur = my_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            cur.execute(qry)
            c = cur.fetchall()
            cur.close()
            # self.result = c
            return c
        except psycopg2.Error as e:
            print(e)
            return False

    except psycopg2.OperationalError as e:
        print(e)
        return False

def get_data_from_geoserver(geo_host, resource):
    """
    Gets a GeoJSON representation of any ressource published by any Geoserver

    :param geo_host: The name of the host geoserver including the port number if necessary
    :param resource: The name of the required resource in the format <workspace>:<resource name> e.g. cso:counties
    :return: The resource in GeoJSON formay
    """
    import httplib2
    import json

    url = "http://{}/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName={}&outputFormat=json" \
          "&srsName=epsg:4326"\
        .format(geo_host, resource)

    try:
        h = httplib2.Http(".cache")
        response_headers, response = h.request(url)
        return json.loads(response.decode())

    except httplib2.HttpLib2Error as e:
        print(e)
        return False
    except Exception as e:
        print(e)
        return False


def main():
    # CONN_STRING = "dbname=geonames user=stduser password=stduser host=mf2.dit.ie port=5432"
    # SQL_QUERY = "SELECT * FROM geonames_populated"
    # SQL_QUERY = "SELECT * FROM geonames_pop_5000"

    GEOSERVER_HOST = "mf2.dit.ie:8080"
    GEOSERVER_RESOURCE = "dit:dublin_museums"

    CONN_STRING = "dbname=osm user=stduser password=stduser host=mf2.dit.ie port=5436"
    SQL_QUERY = "SELECT * FROM dublin_museums"

    geo_result = get_data_from_geoserver(GEOSERVER_HOST, GEOSERVER_RESOURCE)
    pg_result = get_data_from_postgres(CONN_STRING, SQL_QUERY)

    print("Got {} GeoJSON features".format(len(geo_result["features"])))
    print("Got {} rows from database".format(len(pg_result)))

if __name__ == "__main__":
    main()