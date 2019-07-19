#!usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
import os
import shutil
import arcpy
import openpyxl
import numpy

arcpy.env.workspace = r'E:\ArcPyscript\geobodyPY\sourcetable'
arcpy.env.overwriteOutput = True
filepath = r'E:\ArcPyscript\geobodyPY\sourcetable\附表1：13号线路-中铁二院地质钻孔数据汇总.xlsx'
outputResult = r'E:\ArcPyscript\geobodyPY\result.gdb\MergeGeobody0'
print(filepath)

workbook = openpyxl.load_workbook(filepath, read_only=True, data_only=True)

rows = workbook['钻孔数据信息'].rows
line = []
# {'层号'："改层对应的所有行[[],[],[]]"}
levelTable = {}
for row in rows:
    line.append([col.value for col in row])
indexX = line[0].index('坐标XN')
indexY = line[0].index('坐标YE')
indexLevel = line[0].index('层号')
indexCharacter = line[0].index('岩土特征')
indexName = line[0].index('岩土名称')
indexDrill = line[0].index('孔号')
indexId = line[0].index('OBJECTID')

for indexRow in range(1, len(line)):
    try:
        curLevel = line[indexRow][indexLevel].lstrip('<').rstrip('>').replace('-', '_')
        # print(line[index][indexId])
        # 替换中文标点、回车、否则csv解析错误
        line[indexRow][indexCharacter] = str(line[indexRow][indexCharacter]).replace(r",", r"，").replace('\n', '')
        line[indexRow][indexName] = str(line[indexRow][indexName]).replace(r",", r"").replace('\n', '')
        # 深圳独立XY与 ArcMap 中xy相反 这里交换
        if float(line[indexRow][indexY]) > float(line[indexRow][indexX]):
            line[indexRow][indexY], line[indexRow][indexX] = line[indexRow][indexX], line[indexRow][indexY]
    except:
        print('continue')
        print(line[indexRow])
        continue

    # 表格按照层号分层
    if curLevel in levelTable:
        # 如果重复则不添加改行
        flag = 0
        for row in levelTable[curLevel][1:]:
            if row[indexDrill] == line[indexRow][indexDrill]:
                flag = 1
        if flag == 0:
            levelTable[curLevel].append(line[indexRow])
    else:
        levelTable[curLevel] = [line[0], line[indexRow]]
if os.path.exists("temp"):
    shutil.rmtree("temp")
os.mkdir("temp")
# 输出csv表格
for key, value in levelTable.items():
    # 点数少不显示
    if len(value) > 3:
        temppath = r'./temp/' + key + '.csv'
        print("输出" + temppath)
        numpy.savetxt(temppath, value, fmt='%s', delimiter=',')

Beijing_1954_114 = r"PROJCS['Beijing_1954_3_Degree_GK_CM_114E',GEOGCS['GCS_Beijing_1954',DATUM['D_Beijing_1954',SPHEROID['Krasovsky_1940',6378245.0,298.3]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',114.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"
arcpy.env.workspace = r'E:\ArcPyscript\geobodyPY\temp'
arcpy.Delete_management('E:\ArcPyscript\geobodyPY\data.gdb')
arcpy.CreateFileGDB_management('E:\ArcPyscript\geobodyPY', 'data.gdb')

for table in (arcpy.ListTables()):
    levelNum = table.split('.')[0]

    inputTable = os.path.join(arcpy.env.workspace, table)
    arcpy.AddMessage("Start!" + table)
    arcpy.MakeXYEventLayer_management(table=inputTable, in_x_field='坐标XN', in_y_field='坐标YE',
                                      out_layer=r'in_memory\temppoint', spatial_reference=Beijing_1954_114)
    arcpy.AddMessage("MakeXYEventLayer_management have done")

    newXYPara = r"in_memory\temppoint 层顶标高 Mass_Points <None>"
    outputTopTin = r"E:\ArcPyscript\geobodyPY\temp\outputTopTin"
    arcpy.CreateTin_3d(out_tin=outputTopTin, spatial_reference=Beijing_1954_114, in_features=newXYPara,
                       constrained_delaunay="DELAUNAY")
    arcpy.AddMessage("First CreateTin_3d have done")

    newXYPara = r"in_memory\temppoint 层底标高 Mass_Points <None>"
    outputBottomTin = r"E:\ArcPyscript\geobodyPY\temp\outputBottomTin"
    arcpy.CreateTin_3d(out_tin=outputBottomTin, spatial_reference=Beijing_1954_114, in_features=newXYPara,
                       constrained_delaunay="DELAUNAY")
    arcpy.AddMessage("Second CreateTin_3d have done")

    outputTinDomain = "in_memory" + "\\" + "tinDomain1"
    arcpy.TinDomain_3d(outputTopTin, outputTinDomain, "POLYGON")
    arcpy.AddMessage("TinDomain_3d have done")

    outputFeatures = r"E:\ArcPyscript\geobodyPY\data.gdb\geobody" + levelNum
    arcpy.AddMessage('ExtrudeBetween_3d ' + outputFeatures)
    arcpy.ExtrudeBetween_3d(in_tin1=outputTopTin, in_tin2=outputBottomTin, in_feature_class=outputTinDomain,
                            out_feature_class=outputFeatures)
    arcpy.AddMessage("ExtrudeBetween_3d have done")

    for field in line[0]:
        if field != 'OBJECTID':
            arcpy.AddField_management(outputFeatures, field_name=field, field_type='TEXT')
    arcpy.AddMessage("AddField_management have done")
    print([f.name for f in arcpy.ListFields(outputFeatures)])
    with arcpy.da.UpdateCursor(outputFeatures, '*') as cursor:
        for row in cursor:
            print(row[2:])
            print(levelTable[levelNum])
            row[2:] = levelTable[levelNum][2][1:]
            cursor.updateRow(row)
    arcpy.AddMessage("updateRow have done")
    arcpy.Delete_management('in_memory')
    print(table + 'Over!')

arcpy.env.workspace = r'E:\ArcPyscript\geobodyPY\data.gdb'
for index, FeatureClass in enumerate(arcpy.ListFeatureClasses()):
    if index == 0:
        arcpy.Copy_management(FeatureClass, outputResult)
    else:
        arcpy.Append_management(FeatureClass, outputResult, "NO_TEST")
        arcpy.AddMessage("Append_management " + FeatureClass + " have done")
print('Success!!!' + outputResult)
