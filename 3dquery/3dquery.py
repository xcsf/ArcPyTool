#!usr/bin/python
# -*- coding: gbk -*-
import arcpy
import logging
# arcpy.CheckOutExtension("3D")
arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = "UNQUALIFIED"


# pipeLayer = {"url":"https://webgis.szmedi.com.cn/server/rest/services/pipe3d/FeatureServer/0/query?where=1%3D1&f=json&OutFields=*"}


x = '12718107.42'
y = '2582462.66'
z = '16.503'
h = '10'
r = '1'
SDEWorkSpace = r"C:\Users\Mr_Yin\AppData\Roaming\ESRI\Desktop10.6\ArcCatalog\szgis.sde"
LogPathName = r"\\172.18.230.81\arcgissharedata\3dquery.log"
PointsFilePath = r"\\172.18.230.81\arcgissharedata\pointinfo.txt"
PipeFeature = r"szgis_test.sde.pipe3d"

# x = arcpy.GetParameterAsText(0)
# y = arcpy.GetParameterAsText(1)
# z = arcpy.GetParameterAsText(2)
# h = arcpy.GetParameterAsText(3)
# r = arcpy.GetParameterAsText(4)
# SDEWorkSpace = arcpy.GetParameterAsText(5)
# LogPathName = arcpy.GetParameterAsText(6)
# PointsFilePath = arcpy.GetParameterAsText(7)
# PipeFeature = arcpy.GetParameterAsText(8)
# pipearr = {}
response = []

d = float(z)-float(h)
inputSR = r"PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]"
arcpy.arcpy.AcceptConnections(SDEWorkSpace, True)
arcpy.env.workspace = SDEWorkSpace
pipeLayer = SDEWorkSpace + "\\" + PipeFeature


# Define a Handler and set a format which output to file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
    datefmt='%Y-%m-%d %A %H:%M:%S',
    filename=LogPathName,
    filemode='w')
# Define a Handler and set a format which output to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')
console.setFormatter(formatter)
# Create an instance
logging.getLogger().addHandler(console)

try:
    logging.info('Create points file(*.txt)')
    f = open(PointsFilePath, 'w')
    f.write('id,x,y,z\n')
    f.write('1,' + x + ',' + y + ',' + z + '\n')
    f.write('1,' + x + ',' + y + ',' + str(d))
    f.close()
    logging.info('The points file(*.txt) has been created')
    pass
except Exception as e:
    logging.error(e)
    pass

try:
    logging.info('Execute MakeXYEventLayer')
    arcpy.MakeXYEventLayer_management(
        PointsFilePath, "x", "y", "templayer", spatial_reference=inputSR, in_z_field="z")
    logging.info('Execute FeatureClassToFeatureClass_conversion')
    arcpy.FeatureClassToFeatureClass_conversion(
        in_features="templayer", out_path="in_memory", out_name="tempPoint")
    logging.info('Execute PointsToLine_management')
    arcpy.PointsToLine_management(Input_Features="in_memory" + "\\" +
                                  "tempPoint", Output_Feature_Class="in_memory" + "\\" + "resultLine")
    logging.info('Execute Buffer3D_3d')
    arcpy.Buffer3D_3d("in_memory" + "\\" + "resultLine", "in_memory" +
                      "\\" + "queryrange", r + ' METERS', 'STRAIGHT', 30)
    logging.info('Query ranges has been created')
    logging.info('Execute SelectLayerByLocation')
    arcpy.MakeFeatureLayer_management(pipeLayer, "layer")
    queryresult = arcpy.SelectLayerByLocation_management(in_layer="layer", overlap_type="INTERSECT_3D", select_features="in_memory" + "\\" + "queryrange")
    logging.info('Query Completed')
    desc = arcpy.Describe(queryresult)
    cursor = arcpy.SearchCursor(queryresult)
    for row in cursor:
        response.append(row.getValue('id'))
    # print(','.join(response))
    # print(eval(str(response)))
    # print(eval(str(response[0])))
    arcpy.SetParameterAsText(9, ','.join(response))
    pass
except arcpy.ExecuteError:
    errorMsgs = arcpy.GetMessages(2)
    logging.info(str(errorMsgs))
    arcpy.AddError(str(errorMsgs))
    arcpy.AddMessage("Failed!")
    pass
