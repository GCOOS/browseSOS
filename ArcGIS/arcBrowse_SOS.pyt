# coding: utf-8
"""
Tool Name:  Get Stations Location
Source Name: arcBrowse_SOS
Version: ArcGIS 10.3
Author: Shin Kobara
Create: 2015-12-16
Edit:	2015-12-17

This tool performs 
"""
import os as OS
import sys as SYS
import netCDF4
import numpy as np
import datetime as dt
from pyoos.collectors.ioos.swe_sos import IoosSweSos
import arcpy
from arcpy import da
arcpy.env.overwriteOutput = True

try:
    import pyproj
    pyproj_enabled = True
except ImportError:
    pyproj_enabled = False

#Set variables
arcpy.env.workspace = "C:\\Temp\\"
outFolder = arcpy.env.workspace
pointFC = "GCOOS_SOS.shp" 
coordSys = "C:\\Program Files\\ArcGIS\\Desktop10.0\\Coordinate Systems\\Geographic Coordinate Systems\\World\\WGS 1984.prj"
        
class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "arcBrowse_SOS"
        self.alias = "arcBrowse_SOS"
        # List of tool classes associated with this toolbox
        self.tools = [arcBrowse_SOS]


class arcBrowse_SOS(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "arcBrowse_SOS"
        self.description = "Access data ocean observation data via SOS and return a layer"
        self.canRunInBackground = False
        self.url = None
        self.dataset = None
        # Set local variables
        arcpy.CreateFeatureclass_management(outFolder, pointFC, "POINT", "", "", "", coordSys)
        arcpy.AddField_management(pointFC, "name", "TEXT","","", 50)
        
        # Connect to GCOOS
        url_gcoos = 'http://data.gcoos.org:8080/52nSOS/sos/kvp'
        collector_gcoos = IoosSweSos(url_gcoos)
        offerings_gcoos = collector_gcoos.server.offerings
        #of0 = offerings_gcoos[0]
        #of0.id, of0.name, of0.begin_position, of0.end_position, of0.observed_properties, of0.procedures, of0.description, of0.response_formats, of0.response_modes, of0.result_model
        
        cursor = arcpy.InsertCursor(pointFC)
        for x in range(1, len(offerings_gcoos)):
            vertex = arcpy.CreateObject("Point")
            vertex.X = float(offerings_gcoos[x].bbox[0])
            vertex.Y = float(offerings_gcoos[x].bbox[1])
            feature = cursor.newRow()
            feature.shape = vertex
            feature.name = offerings_gcoos[x].name
            cursor.insertRow(feature)
            
        del cursor