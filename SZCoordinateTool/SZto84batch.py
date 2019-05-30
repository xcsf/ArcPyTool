#!usr/bin/python
import arcpy
import sys
import os

staticGDB = r'./static.gdb'
inputLinkFeatures = staticGDB + "\\" + 'LinkSZto54114'

#cad文件转为shp存入的文件夹
#直接运算存在超出坐标范围的错误  所以导出shp后定义坐标系再转为gdb进行转换
#直接使用shp格式进行转换效率极低、速度极慢
dataGDB = r'./cad'
saveToGDB = r'./res.gdb'

# inputFeatures = saveToGDB + "\\" + 'test8_3'
# outputBJ54 = saveToGDB + "\\" + 'test8_354'
# outputWGS84 = saveToGDB + "\\" + 'test8_384'

# inputFeatures = arcpy.GetParameterAsText(0)
# outputBJ54 = arcpy.GetParameterAsText(1)
# outputWGS84 = arcpy.GetParameterAsText(2)

Web_Mercator = r"PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]"
Beijing_1954_114 = r"PROJCS['Beijing_1954_3_Degree_GK_CM_114E',GEOGCS['GCS_Beijing_1954',DATUM['D_Beijing_1954',SPHEROID['Krasovsky_1940',6378245.0,298.3]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',114.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"
arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = "UNQUALIFIED"
arcpy.env.workspace = dataGDB
dsc = arcpy.Describe(inputLinkFeatures)
coord_sys = dsc.spatialReference
try:
    FeatureClasses = arcpy.ListFeatureClasses()
    for FeatureClass in FeatureClasses:
        inputFeatures = os.path.join(arcpy.env.workspace, FeatureClass)
        arcpy.AddMessage("Start!" + FeatureClass)
        arcpy.DefineProjection_management(inputFeatures, coord_sys)
        arcpy.AddMessage("DefineProjection!" + FeatureClass)
    arcpy.FeatureClassToGeodatabase_conversion(FeatureClasses,saveToGDB)
    arcpy.env.workspace = saveToGDB
    FeatureClasses = arcpy.ListFeatureClasses()
    for FeatureClass in FeatureClasses:
        inputFeatures = os.path.join(arcpy.env.workspace, FeatureClass)
        outputWGS84 = os.path.join(arcpy.env.workspace, FeatureClass+'_84')
        outputBJ54 = os.path.join(arcpy.env.workspace, FeatureClass+'_54')
        arcpy.AddMessage("start! Copy_management "+ inputFeatures)
        arcpy.Copy_management(inputFeatures, outputBJ54)
        arcpy.TransformFeatures_edit(outputBJ54, inputLinkFeatures, "AFFINE")
        arcpy.AddMessage("Success TransformFeatures 54 " + outputBJ54)
        arcpy.Project_management(outputBJ54, outputWGS84, Web_Mercator, '54to84')
        arcpy.AddMessage("Success Project 84 " + outputWGS84)
except arcpy.ExecuteError:
    errorMsgs = arcpy.GetMessages(2)
    arcpy.AddError(str(errorMsgs))
    arcpy.AddMessage("Failed!")
    pass
