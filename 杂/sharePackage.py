summary = 'none'
tags = 'none'
path = r"G:\Job\Data\地质\测试" + '\\'
for folder in os.listdir(path):
    if folder[-4:] == 'slpk':
        folderPath = path + folder
        print(folderPath)
        arcpy.SharePackage_management(folderPath, 'arcgis', 'esri123', summary, tags, public='EVERYBODY')