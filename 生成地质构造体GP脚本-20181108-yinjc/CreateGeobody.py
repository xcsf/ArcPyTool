#!usr/bin/python
# -*- coding: gbk -*-
import arcpy
import sys
reload(sys)
sys.setdefaultencoding('gbk')
#arcpy.CheckOutExtension("3D")
arcpy.env.overwriteOutput = True


try:
#    arcpy.env.workspace = "in_memory"
#    arcpy.env.overwriteOutput = True
#    featureCount = 0
#    for fc in arcpy.ListFeatureClasses():
#        arcpy.AddMessage(str(fc))
#        featureCount += 1
#        arcpy.AddMessage(str(featureCount))
#        arcpy.Delete_management(fc)
#        arcpy.AddMessage("Succeed in deleting "+str(fc))
#    if featureCount == 0:
#        arcpy.AddMessage("There are no featureclasses in the workspace: {0}".format(str(arcpy.env.workspace)))


    inputTable = arcpy.GetParameterAsText(0)
    outputWorkspace = arcpy.GetParameterAsText(1)
    outputFC = arcpy.GetParameterAsText(2)
    inputTag = arcpy.GetParameterAsText(3)
    fieldName = arcpy.GetParameterAsText(4)
    fieldValue = arcpy.GetParameterAsText(5)

    arcpy.AddMessage("Start to Convert...")
#    inputSR2 = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision"
#    inputSR1 = r"PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]"
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = outputWorkspace
    arcpy.AddMessage(str(inputTable))
    arcpy.AddMessage(str(outputWorkspace))
    outputNewxy =inputTable
    TinDomain = "Tindomain"
    Z_Field1 = r"cdnbg"  #层顶标高
    Z_Field = r"cdbg" #层底标高


    newXYPara = outputNewxy+r"  cdnbg Mass_Points <None>".replace("cdnbg",Z_Field1) #层顶标高
    outputTin1 = outputWorkspace+"\\"+"outputTin1"
    arcpy.CreateTin_3d(out_tin=outputTin1,in_features=newXYPara,constrained_delaunay="DELAUNAY")
    arcpy.AddMessage("First CreateTin_3d done...")

    outputTin2 = outputWorkspace+"\\"+"outputTin2"
    newXYPara = outputNewxy + r"  cdbg Mass_Points <None>".replace("cdbg", Z_Field)  #层底标高
    arcpy.CreateTin_3d(out_tin=outputTin2, in_features=newXYPara, constrained_delaunay="DELAUNAY")
    arcpy.AddMessage("Second CreateTin_3d done...")

    outputTinDomain = "in_memory"+"\\"+"tinDomain1"
    arcpy.TinDomain_3d(outputTin1,outputTinDomain,"POLYGON")
    arcpy.AddMessage("TinDomain_3d done...")
	
    fc_exist=0
    fc_index=-1
			
    if inputTag=="init":
	fc_array=arcpy.ListFeatureClasses(feature_type='Multipatch')
	for fc in fc_array:	    
	    fc_index+=1;
	    if(str(fc)==outputFC):
	        fc_exist=1
                arcpy.AddMessage(str(fc))
		break;
	if fc_exist==1:
            arcpy.AddMessage("Succeed in deleting "+str(fc_array[fc_index]))
	    arcpy.Delete_management(fc_array[fc_index])	    

	outputFeatures = outputWorkspace+"\\"+outputFC
	arcpy.ExtrudeBetween_3d(in_tin1=outputTin1,in_tin2=outputTin2,in_feature_class=outputTinDomain,out_feature_class=outputFeatures)
	arcpy.AddMessage("ExtrudeBetween_3d done...")

	arcpy.DefineProjection_management(in_dataset=outputFeatures,
						    coor_system= r"PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]")
	arcpy.AddMessage("DefineProjection_management done...")
	arcpy.AddMessage("Create_management done...")
			
	outputFeatures = "in_memory"+"\\"+"TinExtrude"
	arcpy.ExtrudeBetween_3d(in_tin1=outputTin1,in_tin2=outputTin2,in_feature_class=outputTinDomain,out_feature_class=outputFeatures)
	arcpy.AddMessage("ExtrudeBetween_3d done...")\

        arcpy.AddMessage("Start Add Field...")
	outputFeatures = outputWorkspace+"\\"+outputFC
        arcpy.AddField_management(outputFeatures, fieldName, "TEXT")
        count = arcpy.GetCount_management(outputFeatures)
        arcpy.AddMessage("count:"+str(count))
	cursor = arcpy.UpdateCursor(outputFeatures)
	step=0
	for row in cursor:
            step+=1
            if(str(count) == str(step)):
                arcpy.AddMessage("step:"+str(step))
		row.setValue(fieldName, fieldValue)
		cursor.updateRow(row)
	        break;
        arcpy.AddMessage("Add Field done...")
        fc_exist=0
    else:
        fc_exist=1

    if fc_exist==1:
        outputFeatures = "in_memory"+"\\"+"TinExtrude"
	arcpy.ExtrudeBetween_3d(in_tin1=outputTin1,in_tin2=outputTin2,in_feature_class=outputTinDomain,out_feature_class=outputFeatures)
	arcpy.AddMessage("ExtrudeBetween_3d done...")


	arcpy.DefineProjection_management(in_dataset=outputFeatures,
					coor_system= r"PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]")
	arcpy.AddMessage("DefineProjection_management done...")

	schemaType = "NO_TEST"
	arcpy.Append_management(outputFeatures, outputFC, schemaType)
	arcpy.AddMessage("Append_management done...")

	arcpy.AddMessage("Start Add Field...")
	outputFeatures = outputWorkspace+"\\"+outputFC
        count = arcpy.GetCount_management(outputFeatures)
        arcpy.AddMessage("count:"+str(count))
	cursor = arcpy.UpdateCursor(outputFeatures)
	step=0
	for row in cursor:
            step+=1
            if(str(count) == str(step)):
                arcpy.AddMessage("step:"+str(step))
		row.setValue(fieldName, fieldValue)
		cursor.updateRow(row)
	        break;
        arcpy.AddMessage("Add Field done...")	

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


