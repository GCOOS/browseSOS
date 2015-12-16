#!/usr/bin/env python
"""
Name:       GCOOS Python SOS Utils
Author:     bob.currier@gcoos.org
Created:    2015-12-15
Modified:   2015-12-16
Inputs:     SOS service endpoint
Outputs:    GeoJSON formatted feature collection, Python list
Notes:      GCOOS Python Browse SOS. The example methods are intended
            to demonstrate Pythonic ways of accessing and utilizing
            data provided by standards-based SOS services such as
            http://data.gcoos.org/52N_SOS.php.  We use BeautifulSoup4
            to parse the XML as good soup is a wonderous thing.
"""
import sys
import urllib2
from bs4 import BeautifulSoup as soup
from geojson import Feature, Point, FeatureCollection
def gcoos_get_capabilities():
    """
    Notes:
    We use a hard-wired url. Ideally, we would use ConfigParser
    and retrieve the URL for each RA from a config file.
    """
    url = 'http://data.gcoos.org:8080/52nSOS/sos?REQUEST=GetCapabilities\
&SERVICE=SOS&ACCEPTVERSIONS=1.0.0'
    the_file = urllib2.urlopen(url)
    the_data = the_file.read()
    the_file.close()
    return soup(the_data, 'html.parser')

def gcoos_get_observed_properties():
    """
    Notes:
    BeautifulSoup parses the entire tree and returns
    all observed properties.
    """
    observed_props = []
    the_soup = gcoos_get_capabilities()
    properties = the_soup.find_all('sos:observedproperty')
    for the_property in properties:
        observed_props.append(the_property)
    return set(observed_props)

def gcoos_get_all_stations():
    """
    Notes:
    Gets a list of all stations and returns the uri
    for use in gcoos_describe_sensor and gcoos_get_observation
    """
    the_stations = []
    the_soup = gcoos_get_capabilities()
    the_soup = (the_soup.find_all('gml:name'))
    for station in the_soup:
        the_stations.append(station.contents[0])
    return the_stations

def gcoos_describe_sensor(urn):
    """
    Notes:
    Hardwired url for this demo -- very ugly but we ran out
    of time. Will work on making this much more pythonic.
    Hard to embed parameters with all the quotable chars...
    """
    url = 'http://data.gcoos.org:8080/52nSOS/sos/kvp?service=SOS&'
    url = url + 'version=1.0.0&request=DescribeSensor&procedure='
    url = url + urn + '&outputFormat=text%2Fxml%3B%20subtype%3D%22'
    url = url + 'sensorML%2F1.0.1%2Fprofiles%2Fioos_sos%2F1.0%22'

    the_file = urllib2.urlopen(url)
    the_data = the_file.read()
    the_file.close()
    the_soup = soup(the_data, 'html.parser')
    #get position
    the_pos = the_soup.find('gml:pos').contents[0]
    latitude = float(the_pos.split(' ')[0])
    longitude = float(the_pos.split(' ')[1])
    the_org = the_soup.find('sml:organizationname').contents[0]
    the_description = the_soup.find('gml:description').contents[0]
    sensor_list = []
    for sensor in set(the_soup.find_all('sml:output')):
        sensor_list.append(sensor['name'])
    my_feature = Feature(geometry=Point(([longitude, latitude])))
    my_feature.header = {'Organization' : the_org,
                         'Station' : urn,
                         'Description' : the_description,
                         'Sensors' : sensor_list}
    return my_feature

def gcoos_get_observation(station):
    """
    Notes:
    """
    print station

def gcoos_get_org_stations(org):
    """
    Notes:
    """
    print org

