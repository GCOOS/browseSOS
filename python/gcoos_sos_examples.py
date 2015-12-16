#!/usr/bin/env python
"""
DOCSTRING
"""

from geojson import FeatureCollection
from gcoos_sos_utils import gcoos_get_all_stations, gcoos_describe_sensor
def get_all_stations():
    """
    DOCSTRING
    """
    #Show all stations in catalog
    print "Getting all stations..."
    for station in gcoos_get_all_stations():
        print station
    print "--------------------------------"

def get_single_sensor():
    """
    DOCSTRING
    """
    #Get single station description as GeoJSON
    #simple text output
    print "Getting single station..."
    print gcoos_describe_sensor('urn:ioos:station:nerrs:apaebwq')
    print "--------------------------------"

def get_station_total():
    """
    DOCSTRING
    """
    #Total stations in catalog
    print "Total stations: %d" % len(gcoos_get_all_stations())
    print "--------------------------------"

def get_all_sensors():
    """
    DOCSTRING
    """
    #Get all sensor descriptions as GeoJSON features
    #simple text output
    for station in gcoos_get_all_stations():
        print "Fetching data for %s..." % station
        print gcoos_describe_sensor(station)
    print "--------------------------------"

def get_all_sensors_fc():
    """
    DOCSTRING
    """
    #Get all sensor descriptions as GeoJSON features
    #and make into GeoJSON feature collection that can
    #be dropped into Leaflet map
    the_collection = []
    for station in gcoos_get_all_stations():
        print "Fetching data for %s..." % station
        the_collection.append(gcoos_describe_sensor(station))
    the_fc = FeatureCollection(the_collection)
    print the_fc

#Uncomment the example you wish to execute
#get_all_stations()
#get_single_sensor()
#get_all_sensors_fc()
