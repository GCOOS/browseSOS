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
import xml.etree.ElementTree as et
import ConfigParser
import urllib2
from bs4 import BeautifulSoup as soup
from geojson import Feature, Point

def gcoos_get_capabilities(r_a):
    """
    Notes:
    We use a hard-wired url. Ideally, we would use ConfigParser
    and retrieve the URL for each RA from a config file.
    """
    the_server = CONFIG.get('ra_servers', r_a)
    base_url = CONFIG.get('base_urls', 'get_capabilities')
    the_url = the_server + base_url
    if DEBUG:
        print "gcoos_get_capabilities('%s')" % r_a

    the_file = urllib2.urlopen(the_url)
    the_data = the_file.read()
    the_file.close()
    return soup(the_data, 'html.parser')

def gcoos_get_observed_properties(r_a):
    """
    Notes:
    BeautifulSoup parses the entire tree and returns
    all observed properties.
    """
    if DEBUG:
        print "gcoos_get_observed_properties('%s')" % r_a

    observed_props = []
    the_soup = gcoos_get_capabilities(r_a)
    properties = the_soup.find_all('sos:observedproperty')
    for the_property in properties:
        observed_props.append(the_property)
    return set(observed_props)

def gcoos_get_all_stations(r_a):
    """
    Notes:
    Gets a list of all stations and returns the uri
    for use in gcoos_describe_sensor and gcoos_get_observation
    """
    if DEBUG:
        print "gcoos_get_all_stations('%s')" % r_a
    the_stations = []
    the_soup = gcoos_get_capabilities(r_a)
    the_soup = (the_soup.find_all('gml:name'))
    for station in the_soup:
        the_stations.append(station.contents[0])
    #Drop the network:gcoos:all entry. Probably a way not to fetch
    #but for now this works.
    the_stations.remove('urn:ioos:network:gcoos:all')
    return the_stations

def gcoos_describe_sensor(r_a, urn):
    """
    Notes:
    We get all settings from the .cfg file and build
    the_url. Different RAs are running different versions
    of SOS so the XML parsing might need some tweaking. This
    code is known to work with the GCOOS-RA SOS server.
    """
    the_url = CONFIG.get('ra_servers', r_a)
    the_url = the_url + CONFIG.get('base_urls', 'describe_sensor')
    the_url = the_url.replace('[anyURI]', urn)
    if DEBUG:
        print "gcoos_describe_sensor(%s, %s)..." % (r_a, urn)

    the_soup = soup(urllib2.urlopen(the_url).read(), 'html.parser')
    #get position
    the_pos = the_soup.find('gml:pos').contents[0]
    latitude = float(the_pos.split(' ')[0])
    longitude = float(the_pos.split(' ')[1])
    #slurp up the rest of the tasty bits...
    the_org = the_soup.find('sml:organizationname').contents[0]
    the_description = the_soup.find('gml:description').contents[0]
    sensor_list = []
    for sensor in set(the_soup.find_all('sml:output')):
        sensor_list.append(sensor['name'])
    #Get GeoJSON with it...
    my_feature = Feature(geometry=Point(([longitude, latitude])))
    my_feature.header = {'Organization' : the_org,
                         'Station' : urn,
                         'Description' : the_description,
                         'Sensors' : sensor_list}
    return my_feature

def gcoos_get_observation(r_a, sensor, urn):
    """
    Notes:
    We're migrating to lxml so not using BeautifulSoup
    in this function.
    """
    if DEBUG:
        print "gcoos_get_observation(%s, %s, %s)" % (r_a, sensor, urn)
    the_url = CONFIG.get('ra_servers', r_a)
    the_url = the_url + CONFIG.get('base_urls', 'get_observation')
    the_url = the_url.replace('[anyURI]', urn)
    the_url = the_url.replace('[anySensor]', sensor)
    the_url = the_url.replace('[anyRA]', r_a)

    #We need to move the tag definitions to the config file...
    #And we can probably do the parse all in one find but for now
    #we'll drop down one level at a time.
    root = et.fromstring((urllib2.urlopen(the_url).read()))
    da_tag = '{http://www.opengis.net/swe/2.0}DataArray'
    oc_def = """http://mmisw.org/ont/ioos/swe_element_type/"""
    oc_def = oc_def + """sensorObservationCollection"""
    values_tag = '{http://www.opengis.net/swe/2.0}values'
    for elem in root.iter(tag=da_tag):
        if elem.attrib['definition'] == oc_def:
            for child in elem.iter(tag=values_tag):
                data_record = child.text
    return data_record

def gcoos_get_org_stations(org):
    """
    Notes:
    """
    print org
CONFIG = ConfigParser.ConfigParser()
CONFIG_FILE = './gcoos_sos_utils.cfg'
CONFIG.readfp(open(CONFIG_FILE))
DEBUG = CONFIG.getboolean('settings', 'debug')

