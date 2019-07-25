import os
datafolderpath = r'G:\Job\Data\12Line\14'
mapIndex = 0
tempGDB = datafolderpath + "\\" +  r'temp.gdb'
resultGDB = datafolderpath + "\\" +  r'result.gdb'
arcpy.Delete_management(tempGDB)
arcpy.CreateFileGDB_management(datafolderpath, 'temp.gdb')
Beijing_1954_114 = r"PROJCS['Beijing_1954_3_Degree_GK_CM_114E',GEOGCS['GCS_Beijing_1954',DATUM['D_Beijing_1954',SPHEROID['Krasovsky_1940',6378245.0,298.3]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',114.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"
curproject = arcpy.mp.ArcGISProject("CURRENT")
curMapList = curproject.listMaps()
curMap = curMapList[mapIndex]
outputName = ''
arcpy.env.workspace = datafolderpath
for data in arcpy.ListFiles():
    featureSets = []
    if data != 'result.gdb' and data != 'temp.gdb':
        outputName = data[:-4]
        outputFeatures = resultGDB + "\\" + outputName
        outputSLPK = resultGDB + "\\" + outputName
        path = os.path.join(datafolderpath, data)
        print(path)
        curMap.addDataFromPath(path)
        for lyr in curMap.listLayers():
            if lyr.isFeatureLayer and lyr.name != 'LocationPoints':
                arcpy.Layer3DToFeatureClass_3d(lyr, tempGDB + "\\" + lyr.name+'_fean')
        arcpy.env.workspace = tempGDB
        for fc in arcpy.ListFeatureClasses():
            path = os.path.join(tempGDB, fc)
            featureSets.append(path)
        arcpy.Merge_management(featureSets,outputFeatures)
        arcpy.DefineProjection_management(outputFeatures, Beijing_1954_114)
        arcpy.Delete_management(tempGDB)
        arcpy.CreateFileGDB_management(datafolderpath, 'temp.gdb')
        try:
            for layer in curMap.listLayers():
                print('remove',layer)
                if layer.name != ' ':
                    curMap.removeLayer(layer)
                print('remove success',layer)
        except:
            print('continue')
            continue