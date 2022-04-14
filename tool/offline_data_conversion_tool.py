#########################################################################
# Geodatabase Conversion for Offline Collector Data
# Author: Aaron Taveras
# Date Created: 6/27/2019
# Debugging only works with Python 2.7, ArcGIS 10x Desktop, and Spatial Analyst installed 
#########################################################################

import sys #include system specific parameters and functions
import os #include os library

import arcpy, string #include ArcGIS Python library
from arcpy import env #include ArcGIS Python Environment module
from arcpy.sa import* #include ArcGIS Spatial Analyst module

#########################################################################
# Create folder for intermediate processing files
#########################################################################

MainFolder=r"C:/Temp" #follow this path to locate the primary Temp folder
if not os.path.exists(MainFolder):
    os.makedirs(mainFolder)

InterFolder=r"C:/Temp/Collector_Offline_Tool" #follow this path to locate processing files
if not os.path.exists(InterFolder):
    os.makedirs(InterFolder)

#########################################################################
# Mini function to send the print messages to the right output
# Input: Message-string to be printed
#########################################################################
def MyPrint(Message):
    if (RunningInArcMap): arcpy.AddMessage(Message)
    else: print(Message)

#########################################################################
# Determine if we are running within ArcMap (as a tool) or not
#########################################################################

RunningInArcMap=False #assume we are not running as a tool in ArcMap

if (len(sys.argv))>1: #if parameters are present, run in ArcMap as a tool
    RunningInArcMap=True 
    
#########################################################################
# Determine if Spatial Analyst is available
# Enable Spatial Analyst extension
#########################################################################
    
if arcpy.CheckExtension("Spatial")=="Available":
    arcpy.AddMessage("Checking out Spatial")
    arcpy.CheckOutExtension("Spatial")
else:
    arcpy.AddError("Unable to get Spatial Analyst extension")
    arcpy.AddMessage(arcpy.GetMessages(0))
    sys.exit(0)

#########################################################################
# Setup default parameters and then get the parameters from the argument
# List if we are running as a tool in ArcMap.
#########################################################################

MyPrint("""############################################### 
Input and output File paths
###############################################""")

#########################################################################
# All input paths
#########################################################################

CollInput="C:/Temp/Input.geodatabase" #input path for geodatabase file (from Collector)

#########################################################################
# All output paths
#########################################################################

CollGdbOuput="C:/Temp/Collector_Offline_Tool" #default output path for the final geodatabase file (placed in created GDB)
CollGdbName="CollOuput.gdb" #name for empty geodatabase
CollXmlOutput="C:/Temp/Collector_Offline_Tool/Output.xml" #default output path for XML file (converted geodatabase file)

#########################################################################
# If running in a tool, get the parameters from the Arc Tool GUI
#########################################################################

if (RunningInArcMap): #if running in a tool, get the parameters from the Arc Tool GUI
    CollGdbName=arcpy.GetParameterAsText(0) #sets parameter for setting output GDB name
    CollInput=arcpy.GetParameterAsText(1) #sets parameter for setting input filepath
    
#########################################################################
# Prints all parameters for debugging
#########################################################################

MyPrint("CollGdbOuput: "+CollGdbOuput)
MyPrint("CollGdbName: "+CollGdbName)
MyPrint("CollInput: "+CollInput)
MyPrint("CollXmlOutput: "+CollXmlOutput)

#########################################################################
# Run the script repeatedly without deleting the intermediate files
#########################################################################

arcpy.env.overwriteOutput=True

#########################################################################
# Main code (All processing scripts)
#########################################################################

MyPrint("#-----Beginning processing-----#") #prints message to ArcMap dialog that processing has begun

MyPrint("""############################################### 
Creating empty geodatabase
###############################################""")

try:
    arcpy.CreateFileGDB_management(CollGdbOuput, CollGdbName) #
    
    MyPrint(arcpy.GetMessages()) #prints ArcMap dialog processing messages
    MyPrint("#-----Completed successfully-----#") #prints message to ArcMap dialog    
except:
    MyPrint(arcpy.GetMessages()) #prints ArcMap dialog processing messages
    MyPrint("#-----Failed to create new Geodatabase-----#") #prints message to ArcMap dialog
    
MyPrint("""############################################### 
Creating XML input file
###############################################""")

try:
    export_option = "DATA"
    storage_type = "BINARY"
    export_metadata = "METADATA"
    
    arcpy.ExportXMLWorkspaceDocument_management(CollInput, CollXmlOutput, export_option, storage_type, export_metadata) #
    
    MyPrint(arcpy.GetMessages()) #prints ArcMap dialog processing messages
    MyPrint("#-----Completed successfully-----#") #prints message to ArcMap dialog     
except:
    MyPrint(arcpy.GetMessages()) #prints ArcMap dialog processing messages
    MyPrint("#-----Failed to export to XML file-----#") #prints message to ArcMap dialog
    
MyPrint("""############################################### 
Creating the final output geodatabase
###############################################""")

try:
    env.workspace = "C:/Temp/Collector_Offline_Tool"
    
    import_type = "DATA"
    config_keyword = "DEFAULTS"
    
    arcpy.ImportXMLWorkspaceDocument_management(CollGdbName, CollXmlOutput, import_type, config_keyword) #
    
    MyPrint(arcpy.GetMessages()) #prints ArcMap dialog processing messages
    MyPrint("#-----Completed successfully-----#") #prints message to ArcMap dialog     
except:
    MyPrint(arcpy.GetMessages()) #prints ArcMap dialog processing messages
    MyPrint("#-----Failed to import XML file into new geodatabase-----#") #prints message to ArcMap dialog