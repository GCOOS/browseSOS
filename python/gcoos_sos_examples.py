#!/usr/bin/env python
"""
DOCSTRING
"""
from geojson import FeatureCollection
from gcoos_sos_utils import (gcoos_get_all_stations, gcoos_describe_sensor,
                             gcoos_get_capabilities, gcoos_get_observation)
def get_capabilities(r_a):
    """
    DOCSTRING
    """
    print gcoos_get_capabilities(r_a)

def get_all_stations(r_a):
    """
    DOCSTRING
    """
    #Show all stations in catalog
    for station in gcoos_get_all_stations(r_a):
        print station

def get_single_sensor(r_a, urn):
    """
    DOCSTRING
    """
    #Get single station description as GeoJSON
    #simple text output
    print gcoos_describe_sensor(r_a, urn)

def get_station_total(r_a):
    """
    DOCSTRING
    """
    #Total stations in catalog
    print "Total stations: %d" % len(gcoos_get_all_stations(r_a))

def get_all_sensors(r_a):
    """
    DOCSTRING
    """
    #Get all sensor descriptions as GeoJSON features
    #simple text output
    for station in gcoos_get_all_stations(r_a):
        print "Fetching data for %s..." % station
        print gcoos_describe_sensor(r_a, station)

def get_all_sensors_fc(r_a):
    """
    DOCSTRING
    """
    #Get all sensor descriptions as GeoJSON features
    #and make into GeoJSON feature collection that can
    #be dropped into Leaflet map
    the_collection = []
    for station in gcoos_get_all_stations(r_a):
        the_collection.append(gcoos_describe_sensor(r_a, station))
    the_fc = FeatureCollection(the_collection)
    print the_fc

if __name__ == '__main__':
    #get_all_stations('gcoos')
    #get_station_total('gcoos')
    #get_single_sensor('gcoos', 'urn:ioos:station:nerrs:apaebwq')
    #get_all_sensors('gcoos')
    print gcoos_get_observation('gcoos', 'air_temperature', 'urn:ioos:station:disl:bsca1')

