#!usr/bin/python
# -*- coding: gbk -*-
import arcpy
import sys
reload(sys)
sys.setdefaultencoding('gbk')
#arcpy.CheckOutExtension("3D")
arcpy.env.overwriteOutput = True


try:
    arcpy.env.workspace = "in_memory"
    arcpy.env.overwriteOutput = True
    featureCount = 0
    for fc in arcpy.ListFeatureClasses():
        arcpy.AddMessage(str(fc))
        featureCount += 1
        arcpy.AddMessage(str(featureCount))
        arcpy.Delete_management(fc)
        arcpy.AddMessage("Succeed in deleting "+str(fc))
    if featureCount == 0:
        arcpy.AddMessage("There are no featureclasses in the workspace: {0}".format(str(arcpy.env.workspace)))


    inputTable = arcpy.GetParameterAsText(0)
    outputWorkspace = arcpy.GetParameterAsText(1)
    outputFC = arcpy.GetParameterAsText(2)

    arcpy.AddMessage("Start to Convert...")
    inputSR2 = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision"
    inputSR1 = r"PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]"
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = outputWorkspace
    arcpy.AddMessage(str(inputTable))
    arcpy.AddMessage(str(outputWorkspace))
    X_Field = r"xn"#"坐标xn"
    Y_Field = r"ye"#"坐标ye"
    outputNewxy =inputTable
    TinDomain = "Tindomain"
    Z_Field1 = r"cdnbg"  #层顶标高
    Z_Field = r"cdbg" #层底标高


    newXYPara = outputNewxy+r"  cdnbg Mass_Points <None>".replace("cdnbg",Z_Field1) #层顶标高
    outputTin1 = outputWorkspace+"\\"+"outputTin1"
    arcpy.CreateTin_3d(out_tin=outputTin1,spatial_reference=inputSR2,in_features=newXYPara,constrained_delaunay="DELAUNAY")
    arcpy.AddMessage("First CreateTin_3d done...")

    outputTin2 = outputWorkspace+"\\"+"outputTin2"
    newXYPara = outputNewxy + r"  cdbg Mass_Points <None>".replace("cdbg", Z_Field)  #层底标高
    arcpy.CreateTin_3d(out_tin=outputTin2,spatial_reference=inputSR2, in_features=newXYPara, constrained_delaunay="DELAUNAY")
    arcpy.AddMessage("Second CreateTin_3d done...")

    outputTinDomain = "in_memory"+"\\"+"tinDomain1"
    arcpy.TinDomain_3d(outputTin1,outputTinDomain,"POLYGON")
    arcpy.AddMessage("TinDomain_3d done...")

    outputFeatures = "in_memory"+"\\"+"TinExtrude"
    arcpy.ExtrudeBetween_3d(in_tin1=outputTin1,in_tin2=outputTin2,in_feature_class=outputTinDomain,out_feature_class=outputFeatures)
    arcpy.AddMessage("ExtrudeBetween_3d done...")


    arcpy.DefineProjection_management(in_dataset=outputFeatures,
                                     coor_system= r"PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]")
    arcpy.AddMessage("DefineProjection_management done...")

    schemaType = "NO_TEST"
    arcpy.Append_management(outputFeatures, outputFC, schemaType)
    arcpy.AddMessage("Append_management done...")

    arcpy.AddMessage("Succeed!")
    pass
except arcpy.ExecuteError:
    errorMsgs = arcpy.GetMessages(2)
    arcpy.AddError(str(errorMsgs))
    arcpy.AddMessage("Failed!")
    pass
finally:
    arcpy.env.workspace = "in_memory"
    arcpy.env.overwriteOutput = True
    featureCount = 0
    for fc in arcpy.ListFeatureClasses():
        arcpy.AddMessage(str(fc))
        featureCount += 1
        arcpy.AddMessage(str(featureCount))
        arcpy.Delete_management(fc)
    if featureCount == 0:
        arcpy.AddMessage("There are no featureclasses in the workspace: {0}".format(str(arcpy.env.workspace)))
    arcpy.AddMessage("Finished!")
    pass


