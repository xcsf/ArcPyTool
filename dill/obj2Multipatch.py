#!usr/bin/python
# -*- coding: gbk -*-
import arcpy

arcpy.env.overwriteOutput = True
GDBworkspace = r"E:/data"
arcpy.env.workspace = GDBworkspace
try:
    OpenFlightList = arcpy.ListFiles("*.obj")
    print(OpenFlightList)
    arcpy.Import3DFiles_3d(GDBworkspace + "\\" + OpenFlightList[0], "C:/Users/Mr_Yin/Documents/ArcGIS/Default.gdb/asdasd")
    pass
except arcpy.ExecuteError:
    errorMsgs = arcpy.GetMessages(2)
    arcpy.AddError(str(errorMsgs))
    arcpy.AddMessage("Failed!")
    pass