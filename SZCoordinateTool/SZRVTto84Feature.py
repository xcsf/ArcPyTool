#!usr/bin/python
import arcpy
import sys
import logging
import os
LogPathName = r'E:/ArcPyscript/SZCoordinateTool/log.txt'
# Define a Handler and set a format which output to file
logging.basicConfig(
    level=logging.DEBUG,  # 定义输出到文件的log级别，大于此级别的都被输出
    # 定义输出log的格式
    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
    datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
    filename=LogPathName,  # log文件名
    filemode='w')  # 写入模式“w”或“a”
# Define a Handler and set a format which output to console
console = logging.StreamHandler()  # 定义console handler
console.setLevel(logging.INFO)  # 定义该handler级别
formatter = logging.Formatter(
    '%(asctime)s  %(filename)s : %(levelname)s  %(message)s')  # 定义该handler格式
console.setFormatter(formatter)
# Create an instance
logging.getLogger().addHandler(console)  # 实例化添加handler
# 输出日志级别
# Print information
# logging.debug('logger debug message')
# logging.info('logger info message')
# logging.warning('logger warning message')
# logging.error('logger error message')
# logging.critical('logger critical message')

GDBworkspace = r'E:/ArcPyscript/SZCoordinateTool/test.gdb'
rvtPath = r'E:/ArcPyscript/SZCoordinateTool/SZ.rvt'
# inputLinkFeatures = GDBworkspace + "\\" + 'Link54114toSZ'
inputLinkFeatures = GDBworkspace + "\\" + 'LinkSZto54114'
outputFeatures = GDBworkspace + "\\" + 'result_54'
outputResult = GDBworkspace + "\\" + 'result_4326'
featureSets = []
Web_Mercator = r"PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]"
arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = "UNQUALIFIED"
arcpy.env.workspace = rvtPath

try:
    datasets = arcpy.ListDatasets()
    for ds in datasets:
        for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
            if fc == 'LocationPoints':
                continue
            path = os.path.join(arcpy.env.workspace, ds, fc)
            # print(path)
            arcpy.MakeFeatureLayer_management (path, fc+'_lyr')
            arcpy.Layer3DToFeatureClass_3d(fc+'_lyr', "in_memory"+ "\\" + fc+'_fea')
    arcpy.env.workspace = "in_memory"
    for fc in arcpy.ListFeatureClasses():
        path = os.path.join(arcpy.env.workspace, fc)
        featureSets.append(path)
    arcpy.Merge_management(featureSets,outputFeatures)
    arcpy.Delete_management("in_memory")
    arcpy.TransformFeatures_edit(outputFeatures, inputLinkFeatures, "AFFINE")
    arcpy.Project_management(outputFeatures, outputResult, Web_Mercator, '54to84')
except arcpy.ExecuteError:
    errorMsgs = arcpy.GetMessages(2)
    logging.error(str(errorMsgs))
    arcpy.AddError(str(errorMsgs))
    arcpy.AddMessage("Failed!")
    pass
