#!usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
import os
import shutil
import openpyxl
import numpy

if os.path.exists("temp"):
    shutil.rmtree("temp")
os.mkdir("temp")
dictionary = {
    '中砂': 'MediumSand',
    '中风化混合花岗岩': 'WeatheringMixedGranite',
    '中风化花岗岩': 'ModeratelyWeatheredGranite',
    '中风化黑云母花岗岩': 'WeatheringOfBiotiteGranite',
    '中等风化炭质页岩夹砂岩': 'ModeratelyWeatheredSandstoneCarbonaceousShale',
    '中等风化碎裂岩': 'MediumWeatheringCataclasticRock',
    '中等风化泥岩与砂岩互层': 'ModeratelyWeatheredMudstoneAndSandstoneInterbed',
    '中等风化糜棱岩': 'MediumWeatheringMylonite',
    '中等风化角岩': 'MediumWeatheringHornfels',
    '中等风化混合岩': 'MediumWeatheringMigmatite',
    '中等风化混合花岗岩': 'MediumWeatheringMixedGranite',
    '中等风化花岗岩': 'ModeratelyWeatheredGranite',
    '中等风化黑云母花岗岩': 'MediumWeatheringBiotiteGranite',
    '中等风化含砾砂岩': 'MediumWeatheringConglomeraticSandstone',
    '中等风化断层角砾岩': 'MediumWeatheringFaultBreccia',
    '中粗砂': 'MidCoarseSand',
    '杂填土': 'MiscellaneousFill',
    '圆砾': 'RoundGravel',
    '淤泥质土': 'SiltSoil',
    '淤泥质黏性土': 'MuddyClay',
    '淤泥质黏土': 'MuddyClay',
    '淤泥质砾砂': 'MuddyGravelSand',
    '淤泥质粉质粘土': 'MuddySiltyClay',
    '淤泥质粉质黏土': 'MuddySiltyClay',
    '淤泥': 'Silt',
    '有机质土（炭质页岩）': 'SoilOrganicMatter',
    '有机质土': 'SoilOrganicMatter',
    '硬塑状砂质粘性土': 'HardPlasticSandClayeySoil',
    '硬塑状砾质粘性土': 'HardPlasticGravelClayeySoil',
    '硬塑状粉质粘土': 'HardPlasticSiltyClay',
    '硬塑砂质粘性土': 'HardPlasticSandClayeySoil',
    '硬塑砂质黏性土': 'HardPlasticSandClayeySoil',
    '硬塑砾质粘性土': 'HardPlasticGravelClayeySoil',
    '硬塑砾质黏性土': 'HardPlasticGravelClayeySoil',
    '硬塑粉质粘土': 'HardPlasticSiltyClay',
    '硬塑粉质黏土': 'HardPlasticSiltyClay',
    '细砂': 'FineSand',
    '微风化泥岩与砂岩互层': 'BreezeOfMudstoneAndSandstoneInterbed',
    '微风化角岩': 'BreezeTheHornfels',
    '微风化混合岩': 'BreezeMigmatite',
    '微风化混合母花岗岩': 'BreezeMotherMixedGranite',
    '微风化混合花岗岩': 'BreezeMixedGranite',
    '微风化花岗岩': 'BreezeGranite',
    '微风化黑云母母花岗岩': 'BreezeMotherBiotiteGranite',
    '微风化黑云母花岗岩': 'BreezeBiotiteGranite',
    '挖孔区': 'DigAHoleArea',
    '土状强风化碎裂岩': 'EarthyWeatheringCataclasticRock',
    '土状强风化角岩': 'EarthyWeatheringHornfels',
    '土状强风化混合岩': 'EarthyWeatheringMigmatite',
    '土状强风化混合花岗岩': 'EarthyStrongWeatheringMixedGranite',
    '土状强风化花岗岩': 'EarthyStronglyWeatheredGranite',
    '土状强风化黑云母花岗岩': 'EarthyWeatheringBiotiteGranite',
    '土状强风化含砾砂岩': 'EarthyWeatheringConglomeraticSandstone',
    '土状强风化变质粉砂岩': 'EarthyStronglyWeatheredMetamorphicSiltstone',
    '填碎石土': 'FillGravelSoil',
    '填碎石': 'FillInTheRubble',
    '填石层(碎石、块石)': 'RockFill',
    '填石层（碎石、块石）': 'RockFill',
    '填石层(碎石)': 'RockFill',
    '填石层（碎石）': 'RockFill',
    '填石层(块石)': 'RockFill',
    '填石层': 'RockFill',
    '填石(块石)': 'RockFill',
    '填石': 'RockFill',
    '填砂层（砂）': 'FillInTheSand',
    '填砂层(砂)': 'FillInTheSand',
    '填砂层': 'FillInTheSand',
    '填砂': 'FillInTheSand',
    '填块石': 'FillInTheStone',
    '炭质页岩(土状)': 'CarbonaceousShale',
    '炭质页岩(块状)': 'CarbonaceousShale',
    '炭质页岩': 'CarbonaceousShale',
    '碎屑灰岩': 'ClasticLimestone',
    '碎石土': 'GravelSoil',
    '碎裂岩': 'CataclasticRock',
    '素填土(碎石、块石)': 'GrainFilling',
    '素填土(碎石)': 'GrainFilling',
    '素填土(砂)': 'GrainFilling',
    '素填土': 'GrainFilling',
    '砂质粘性土': 'SandyClay',
    '砂质黏性土': 'SandyClay',
    '砂岩(土状)': 'Sandstone',
    '砂岩(块状)': 'Sandstone',
    '砂岩': 'Sandstone',
    '溶洞卵石': 'KarstCave,Pebble',
    '溶洞砾砂': 'KarstCave,SandGravel',
    '溶洞粉质黏土': 'KarstCave,SiltyClay',
    '溶洞': 'KarstCave',
    '全风化炭质页岩夹砂岩': 'WeatheredSandstoneCarbonaceousShale',
    '全风化碎裂岩': 'WeatheredBrokenRock',
    '全风化泥岩与砂岩互层': 'WeatheredMudstoneAndSandstoneInterbed',
    '全风化角岩': 'WeatheredHornfels',
    '全风化混合岩': 'WeatheredMigmatite',
    '全风化混合花岗岩': 'WeatheredMixedGranite',
    '全风化花岗岩': 'FullyWeatheredGranite',
    '全风化黑云母化花岗岩': 'WeatheredBiotiteGranite',
    '全风化黑云母花岗岩': 'WeatheredBiotiteGranite',
    '全风化含砾砂岩': 'WeatheredConglomeraticSandstones',
    '全风化断层角砾岩、断层泥': 'WeatheredFaultBrecciaAndFaultGouge',
    '全风化变质粉砂岩': 'WeatheredMetamorphicSiltstone',
    '全风黑云母化花岗岩': 'WindBiotiteGranite',
    '强风化炭质页岩夹砂岩（块状）': 'StrongWeatheringCarbonaceousShaleClipSandstone(Block)',
    '强风化炭质页岩夹砂岩': 'StrongWeatheredSandstoneCarbonaceousShale',
    '强风化炭质页岩': 'StrongWeatheringCarbonaceousShale',
    '强风化石英脉': 'StrongWindFossilsOfArteriesAndVeins',
    '强风化泥岩与砂岩互层(块状)': 'StronglyWeatheredMudstoneAndSandstoneInterbed(Block)',
    '强风化糜棱岩(土状)': 'StrongWeatheringMylonite(Soil)',
    '强风化混合花岗岩(土状)': 'StrongWeatheringMixGranite',
    '强风化混合花岗岩（土状）': 'StrongWeatheringMixGranite',
    '强风化混合花岗岩(块状)': 'StrongWeatheringMixGranite',
    '强风化混合花岗岩(半岩半土状)': 'StrongWeatheringMixGranite',
    '强风化混合花岗岩（半岩半土状）': 'StrongWeatheringMixGranite',
    '强风化花岗岩(土状)': 'StronglyWeatheredGranite',
    '强风化花岗岩(块状)': 'StronglyWeatheredGranite',
    '强风化花岗岩(半岩半土状)': 'StronglyWeatheredGranite',
    '强风化花岗岩': 'StronglyWeatheredGranite',
    '强风化黑云母花岗岩（土状）': 'StrongWeatheringBiotiteGranite',
    '强风化黑云母花岗岩(土状)': 'StrongWeatheringBiotiteGranite',
    '强风化黑云母花岗岩（碎块状）': 'StrongWeatheringBiotiteGranite',
    '强风化黑云母花岗岩(块状)': 'StrongWeatheringBiotiteGranite',
    '强风化黑云母花岗岩（块状）': 'StrongWeatheringBiotiteGranite',
    '强风化黑云母花岗岩（半岩半土状）': 'StrongWeatheringBiotiteGranite',
    '强风化黑云母花岗岩(半岩半土状)': 'StrongWeatheringBiotiteGranite',
    '强风化黑云母花岗岩': 'StrongWeatheringBiotiteGranite',
    '强风化断层角砾岩': 'StrongWeatheringFaultBreccia',
    '凝灰质石英岩(土状)': 'TuffaceousQuartzite',
    '凝灰质石英岩(块状)': 'TuffaceousQuartzite',
    '凝灰质石英岩': 'TuffaceousQuartzite',
    '黏性土': 'CohesiveSoils',
    '黏土': 'Clay',
    '泥质粉砂岩': 'ArgillaceousSiltstone',
    '泥炭质淤泥': 'PeatySilt',
    '泥炭质土': 'PeatSoil',
    '泥炭质黏性土': 'PeatyClayeySoils',
    '靡棱岩': 'PeddlerRidgeRock',
    '糜棱岩': 'Mylonite',
    '卵石': 'Pebble',
    '砾质黏性土': 'GravellyClayeySoils',
    '砾砂': 'GravelSand',
    '块状强风化碎裂岩': 'MassiveStrongWeatheringCataclasticRock',
    '块状强风化角岩': 'MassiveStrongWeatheringHornfels',
    '块状强风化混合岩': 'MassiveStrongWeatheringMigmatite',
    '块状强风化混合花岗岩': 'MassiveStrongWeatheringMixedGranite',
    '块状强风化花岗岩': 'MassiveStronglyWeatheredGranite',
    '块状强风化黑云母花岗岩': 'MassiveStrongWeatheringBiotiteGranite',
    '块状强风化含砾砂岩': 'MassiveStrongWeatheringConglomeraticSandstones',
    '块状强风化变质粉砂岩': 'MassiveStronglyWeatheredMetamorphicSiltstone',
    '可塑状砂质粘性土': 'PlasticSandClayeySoil',
    '可塑状砾质粘性土': 'PlasticGravelClayeySoil',
    '可塑状粉质粘土': 'PlasticSiltyClay',
    '可塑砂质黏性土': 'PlasticSandClayeySoil',
    '可塑砾质黏性土': 'PlasticGravelClayeySoil',
    '可塑粉质黏土': 'PlasticSiltyClay',
    '角岩': 'Hornfels',
    '灰岩': 'Limestone',
    '花岗岩(土状)': 'Granite',
    '花岗岩(块状)': 'Granite',
    '花岗岩': 'Granite',
    '含砾砂岩': 'ConglomeraticSandstone',
    '含砾黏性土': 'ConglomeraticClayeySoils',
    '孤石': 'Boulder',
    '粉质粘土': 'SiltyClay',
    '粉质黏土': 'SiltyClay',
    '粉细砂': 'SiltySand',
    '粉土': 'Floury Soil ',
    '粉砂': 'MealySand',
    '粗砂': 'CoarseSand',
    '变质石英砂岩': 'MetamorphicQuartzSandstone',
    '变质粉砂岩(土状)': 'MetamorphicSiltstone',
    '变质粉砂岩(块状)': 'MetamorphicSiltstone',
    '变质粉砂岩': 'MetamorphicSiltstone',
    '半岩半土状强风化混合花岗岩': 'RockAndSoilStrongWeatheringMixedGranite',
    '半岩半土状强风化黑云母花岗岩': 'RockAndSoilStrongWeatheringBiotiteGranite',
    '半岩半土状黑云母花岗岩': 'RockAndSoilBiotiteGranite',

}

filename = r'附表1-2：14号线(布石区间)-中国铁设地质钻孔数据模板'
filepath = r'E:\ArcPyscript\geobodyPY\sourcetable' + '\\' + filename + '.xlsx'
print(filepath)

workbook = openpyxl.load_workbook(filepath, read_only=True, data_only=True)

rows = workbook['钻孔数据信息'].rows
line = []
outputline = []

for row in rows:
    line.append([col.value for col in row])
indexX = line[0].index('坐标XN')
indexY = line[0].index('坐标YE')
# indexLevel = line[0].index('层号')
indexCharacter = line[0].index('岩土特征')
indexName = line[0].index('岩土名称')
indexDrill = line[0].index('孔号')
indexBottom = line[0].index('层底标高')
indexTop = line[0].index('层顶标高')
# indexId = line[0].index('OBJECTID')
# 岩土名称唯一值
namesUnique = {}
namesAndCharacterUnique = {}
# {岩土名称: count}
namesCount = {}
nameEnArray = []
dataLine = ''
for indexRow in range(1, len(line)):
    try:

        # 替换中文标点、回车、否则csv解析错误
        line[indexRow][indexCharacter] = str(line[indexRow][indexCharacter]).replace(r",", r"，").replace('\n', '')
        line[indexRow][indexName] = str(line[indexRow][indexName]).replace(r",", r"").replace('\n', '')
        curName = line[indexRow][indexName].replace('\n', '')
        curNameAndCharacter = curName + line[indexRow][indexCharacter]
        # 深圳独立XY与 ArcMap 中xy相反 这里交换
        if float(line[indexRow][indexY]) > float(line[indexRow][indexX]):
            line[indexRow][indexY], line[indexRow][indexX] = line[indexRow][indexX], line[indexRow][indexY]
    except Exception as e:
        print('continue')
        print(e)
        print(line[indexRow])
        continue

    # 构造岩土名称英文列表
    if curName not in namesUnique:
        namesCount[curName] = 1
        namesUnique[curName] = dictionary[curName]
        namesAndCharacterUnique[curNameAndCharacter] = dictionary[curName]
        nameEnArray.append(dictionary[curName])
        # print(curName + ' : ' + namesUnique[curName])
    else:
        if curNameAndCharacter not in namesAndCharacterUnique:
            namesAndCharacterUnique[curNameAndCharacter] = dictionary[curName] + str(namesCount[curName])
            nameEnArray.append(namesAndCharacterUnique[curNameAndCharacter])
            namesCount[curName] = namesCount[curName] + 1

elevationLine = 'Elevation '
for i, nameEn in enumerate(nameEnArray):
    elevationLine += "\"" + str(i + 1) + r"|" + nameEn + "\" "
    pass
count = 0
for indexRow in range(1, len(line)):
    try:
        curName = line[indexRow][indexName].replace('\n', '')
        curNameAndCharacter = curName + line[indexRow][indexCharacter]
        if line[indexRow][indexDrill] != drillNum:
            drillNum = line[indexRow][indexDrill]
            dataLine += str(line[indexRow][indexX]) + '	' + str(line[indexRow][indexY]) + '	' + str(line[indexRow][indexTop]) + '	' + str(nameEnArray.index(namesAndCharacterUnique[curNameAndCharacter]) + 1) + '	' + line[indexRow][indexDrill] + '\n'
            count += 1
        dataLine += str(line[indexRow][indexX]) + '	' + str(line[indexRow][indexY]) + '	' + str(line[indexRow][indexBottom]) + '	' + str(nameEnArray.index(namesAndCharacterUnique[curNameAndCharacter]) + 1) + '	' + line[indexRow][indexDrill] + '\n'
        count += 1
    except Exception as e:
        print('continue')
        print(e)
        print(line[indexRow])
        continue

headLine = 'X Y Z Geologic_Unit_Id Bore\n'
elevationLine += 'meters \n'
countLine = str(count) + ' 1' + '\n'
temppath = r'./temp/' + filename + '.pgf'
print("输出" + temppath)
with open(temppath, 'w') as fileobj:
    fileobj.write(headLine)
    fileobj.write(elevationLine.replace(u'\xa0', u' '))
    fileobj.write(countLine)
    fileobj.write(dataLine)

