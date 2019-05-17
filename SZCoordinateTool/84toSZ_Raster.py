#!usr/bin/python
import arcpy
import sys
import logging

# staticGDB = r'./static.gdb'
# saveToGDB = r'./data.gdb'
# inputFeatures = staticGDB + "\\" + 'SZbasemap84'
# inputLinkFeatures = staticGDB + "\\" + 'Link54114toSZ'
# outputFeatures = saveToGDB + "\\" + 'SZbasemap54114'
inputFeatures = arcpy.GetParameterAsText(0)
outputFeatures = arcpy.GetParameterAsText(1)
Web_Mercator = r"PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]"
Beijing_1954_114 = r"PROJCS['Beijing_1954_3_Degree_GK_CM_114E',GEOGCS['GCS_Beijing_1954',DATUM['D_Beijing_1954',SPHEROID['Krasovsky_1940',6378245.0,298.3]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',114.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"

arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = "UNQUALIFIED"

try:
    arcpy.AddMessage("Start!")
    arcpy.ProjectRaster_management(inputFeatures, "in_memory"+ "\\" + 'temp', Beijing_1954_114,geographic_transform="84to54")
    arcpy.AddMessage("ProjectRaster_management!")
    arcpy.WarpFromFile_management( "in_memory"+ "\\" + 'temp',outputFeatures,'./54114tonewsz.txt','POLYORDER1')
    arcpy.AddMessage("WarpFromFile_management!")
except arcpy.ExecuteError:
    errorMsgs = arcpy.GetMessages(2)
    arcpy.AddError(str(errorMsgs))
    arcpy.AddMessage("Failed!")
    pass
