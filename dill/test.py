#!usr/bin/python
# -*- coding: utf-8 -*-
import arcpy
import sys
import re
import arcpy
import xlrd
import xlwt
reload(sys)
sys.setdefaultencoding('gbk')
# arcpy.CheckOutExtension("3D")
arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = "UNQUALIFIED"

# inputPipeTable = r'E:/dill/a.xls'
# outputFile = r"E:\dill"
# PipeFeatureName = r"pipe.shp"
# PointFeatureName = r"point.shp"
# GDBworkspace = u"C:/Users/Mr_Yin/Documents/ArcGIS/Default.gdb"

inputPipeTable = arcpy.GetParameterAsText(0)
outputFile = arcpy.GetParameterAsText(1)
PipeFeatureName = arcpy.GetParameterAsText(2)
PointFeatureName = arcpy.GetParameterAsText(3)
GDBworkspace = arcpy.GetParameterAsText(4)

arcpy.env.workspace = GDBworkspace
sheet =  xlrd.open_workbook(inputPipeTable).sheet_by_index(0)
rows = sheet.get_rows()
tempExcel = xlwt.Workbook()
connectsheet = tempExcel.add_sheet('connect')
pointsheet = tempExcel.add_sheet('point')
pointsheet2 = tempExcel.add_sheet('point2')
allpointssheet = tempExcel.add_sheet('allpoints')
# 点集{'管线点预编号': 对应表格行}(埋深变为最低点)
points = {}
connectid = 1
flag = False

# 相关列的下标变量
# 预编号列与连接点号
name = 0
toname = 1
# 埋设方式
mode = 2
# 管线材料
material = 3
# 管径mm
diameter = 4
# 特征
prop = 5
# 附属物
attach = 6
# 平面坐标x y
x = 7
y = 8
# 地面高程
ground = 9
# 埋深
depth = 12
# 电缆数
elenum = 13
# 管孔排列
collocate = 14
# 电力电压
voltage = 15
# 备注
remark = 16
# 管线类型
pipetype = ""

# 添加一行 工作表、第n行、[内容数组]
def addRow(sheet,row,array):
    i = 0
    for item in array:
        sheet.write(row,i,item)
        i = i+1

# 检测埋深数据是否为空或者是否为float类型 计算返回改点高程 不合法点高程为0
def CheckElevation(arg):
    try:
        return float(arg[ground].value) - float(arg[depth].value)
    except Exception as e:
        print(e.message + u"\n不合法点高程为0")
        return 0

# 检测管径数据是否合法 不合法默认半径为0.1米 t = 0时为宽 t = 1时为高
def CheckDiameter(diameter, t):
    try:
        return float(diameter)/2000.0
    except Exception as e:
        try:
            return float(diameter.split('X')[t])/2000.0
        except Exception as e:
            print(e.message + u"\n未知数据默认半径0.1米")
            return 0.1

# 返回当前管点最大的埋深管线埋深 
def CheckDepth(nowdepth, rowdepth):
    try:
        t1 = float(nowdepth)
        t2 = float(rowdepth)
    except Exception as e:
        try:
            float(nowdepth)
        except Exception as e:
            try:
                float(rowdepth)
            except Exception as e:
                print(e.message + u"\n未知数据默认埋深为0")
                return 0
            else:
                return float(rowdepth)
        else:
            return float(nowdepth)
    else:
        return t2 if t1 < t2 else t1

# 管点对应管线ID row当前遍历的行
def AddConnectTable(endptA, endptB ,row):
    # 坐标信息
    startx = row[x].value
    starty = row[y].value
    lineID = endptA + '_' + endptB
    startz = CheckElevation(row)
    # 相关属性
    mod = row[mode].value
    mat = row[material].value
    wid = CheckDiameter(row[diameter].value, 0)
    hei = CheckDiameter(row[diameter].value, 1)
    ele = row[elenum].value
    col = row[collocate].value
    vol = row[voltage].value
    global connectid
    addRow(connectsheet,connectid,[lineID, startx, starty, startz, endptA, endptB, mod, mat, wid, hei, ele, col, vol, pipetype])
    connectid += 1

# 管点类型数组
Pointtype = [u"电信手孔", u"电信人孔", u"检查井" , u"未知井", u"阀门井", u"检修井", u"雨篦", u"路灯", u"排泥井", u"消防栓", u"消火栓"]
def AddPointsTable(points):
    pt = 1
    pointid = 1
    pointid2 = 1
    for key, value in points.items():
        ptnum = key
        ptx = value[x].value
        pty = value[y].value
        ptprop = value[prop].value
        ptattach = value[attach].value
        ptz = value[ground].value - value[depth].value
        gro = value[ground].value
        addRow(allpointssheet, pt, [ptnum, ptx, pty, ptz, ptattach, ptprop, gro, pipetype])
        pt += 1
        if value[attach].value in Pointtype:
            # 地面高程
            pth = value[ground].value
            # 最低点高程
            ptz = pth - value[depth].value - CheckDiameter(value[diameter].value, 0)
            addRow(pointsheet, pointid, [ptnum, ptx, pty, ptz, ptattach, ptprop, pipetype])
            addRow(pointsheet, pointid+1, [ptnum, ptx, pty, pth, ptattach, ptprop ,pipetype])
            pointid += 2
        else:
            ptz = value[ground].value - value[depth].value
            addRow(pointsheet2, pointid2, [ptnum, ptx, pty, ptz, ptattach, ptprop, pipetype])
            pointid2 += 1
            pass
# 添加表头
addRow(connectsheet,0,["id", "x", "y", "z", "startpt", "endpt", "mode", "material", "width", "heigh", "electric", "collocate", "voltage", "pipetype"])
addRow(pointsheet,0,["id", "x", "y", "z", "attach", "prop", "pipetype"])
addRow(pointsheet2,0,["id", "x", "y", "z", "attach", "prop", "pipetype"])
addRow(allpointssheet,0,["id", "x", "y", "z", "attach", "prop", "ground", "pipetype"])

for row in rows:
    start = row[0].value
    if u"管线类型" in start:
        pipetype = start[5:]
    end = row[1].value
    # 找管线点预编号一行
    if not flag:
        if start != u"管线点\n预编号":
            continue
        else:
            flag = True
            continue
    else:
        # 俩空白跳过
        if(start == u'' and end == u''):
            continue
        # 起始点存在
        if start != '':
            # 记录当前正在判断的起始点
            nowrow = row
            points[start] = row
            # print(nowrow[0].value)
            #终点已存在点集内
            if end in points:
                AddConnectTable(end, start, row)
                # print(u"%s与当前起始点%s相连" % (end,start))
            else:
                AddConnectTable(start, end, row)
                # print(u"跳过%s" % end)
            points[nowrow[0].value][depth].value = CheckDepth(nowrow[depth].value, row[depth].value)
        # 起始点位置为空 即判断终点是否在点集中
        else:
            # 将管井点最低高程管的埋深更新至点集中
            points[nowrow[0].value][depth].value = CheckDepth(nowrow[depth].value, row[depth].value)
            if end in points:
                AddConnectTable(end, nowrow[0].value, row)
                # print(u"%s与当前起始点%s相连" % (end,nowrow[0].value))
            else:
                AddConnectTable(nowrow[0].value, end, row)
                # print(u"跳过%s" % end)

AddPointsTable(points)
outTempTable = r"E:/dill/temp.xls"
tempExcel.save(outTempTable)
input_table = outTempTable + "/connect$"
point_table = outTempTable + "/point$"
point_table2 = outTempTable + "/point2$"
allpoint_table = outTempTable + "/allpoints$"
inputSR = r"PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]"
inmemory = "in_memory"


LineLayer = "E:/dill/resultLayer.lyr"

try:
    # 生成三维管线
    arcpy.MakeXYEventLayer_management(input_table, "x", "y", "templayer",spatial_reference = inputSR, in_z_field = "z")
    arcpy.FeatureClassToFeatureClass_conversion(in_features = "templayer",out_path = inmemory, out_name = "tempPoint")
    arcpy.PointsToLine_management(Input_Features = inmemory+ "\\" + "tempPoint", Output_Feature_Class = inmemory + "\\" + "resultLine", Line_Field = "id")
    arcpy.MakeFeatureLayer_management(inmemory + "\\" + "resultLine" , "layer")
    # arcpy.SaveToLayerFile_management("layer", LineLayer)
    # arcpy.AddJoin_management(LineLayer, "id", input_table, "id")
    arcpy.AddJoin_management("layer", "id", input_table, "id")
    # arcpy.FeatureClassToFeatureClass_conversion(LineLayer, out_path = inmemory, out_name = "tempLine")
    arcpy.FeatureClassToFeatureClass_conversion("layer", out_path = outputFile, out_name = PipeFeatureName)
    arcpy.Buffer3D_3d(outputFile + "\\" + PipeFeatureName, 'pipe3d', 'width', 'STRAIGHT', 30)
    arcpy.Delete_management(inmemory)

    # 生成三维管点
    arcpy.MakeXYEventLayer_management(point_table, "x", "y", "templayer",spatial_reference = inputSR, in_z_field = "z")
    arcpy.FeatureClassToFeatureClass_conversion(in_features = "templayer",out_path = inmemory, out_name = "tempPoint")
    arcpy.PointsToLine_management(Input_Features = inmemory+ "\\" + "tempPoint", Output_Feature_Class = inmemory + "\\" + "resultLine", Line_Field = "id")
    arcpy.Buffer3D_3d(inmemory + "\\" + "resultLine", 'point3d', '0.5 METERS', 'STRAIGHT', 30)
    arcpy.Delete_management(inmemory)
    
    # 其他管点
    arcpy.MakeXYEventLayer_management(point_table2, "x", "y", "templayer",spatial_reference = inputSR, in_z_field = "z")
    arcpy.FeatureClassToFeatureClass_conversion(in_features = "templayer",out_path = inmemory, out_name = "tempPoint")
    arcpy.Buffer3D_3d(inmemory + "\\" + "tempPoint", 'point23d', '0.5 METERS', 'STRAIGHT', 30)
    arcpy.Delete_management(inmemory)

    # 输出点集
    arcpy.MakeXYEventLayer_management(allpoint_table, "x", "y", "templayer",spatial_reference = inputSR, in_z_field = "z")
    arcpy.FeatureClassToFeatureClass_conversion(in_features = "templayer",out_path = outputFile, out_name = PointFeatureName)

except arcpy.ExecuteError:
    errorMsgs = arcpy.GetMessages(2)
    arcpy.AddError(str(errorMsgs))
    arcpy.AddMessage("Failed!")
    pass