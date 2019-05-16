#!usr/bin/python
# -*- coding: gbk -*-
# import logging
# import arcpy
# arcpy.env.overwriteOutput = True
# arcpy.env.workspace = r"E:\dill"
# try:
#     arcpy.ExcelToTable_conversion(Input_Excel_File = "temp.xls", Output_Table = "test.gdb/connect", Sheet = "connect")
# except arcpy.ExecuteError:
#     errorMsgs = arcpy.GetMessages(2)
#     arcpy.AddError(str(errorMsgs))
#     arcpy.AddMessage("Failed!")
#     pass

import os
import xlrd
import arcpy
def importallsheets(in_excel, out_gdb):
    workbook = xlrd.open_workbook(in_excel)
    sheets = [sheet.name for sheet in workbook.sheets()]
    print(sheets)
    print('{} sheets found: {}'.format(len(sheets), ','.join(sheets)))
    for sheet in sheets:
        # The out_table is based on the input excel file name
        # a underscore (_) separator followed by the sheet name
        out_table = os.path.join(
            out_gdb,
            arcpy.ValidateTableName(
                "{0}_{1}".format(os.path.basename(in_excel), sheet),
                out_gdb))
        print('Converting {} to {}'.format(sheet, out_table))
        # Perform the conversion
        arcpy.ExcelToTable_conversion(in_excel, out_table, sheet)
if __name__ == '__main__':
    importallsheets('e:/dill/a.xls',
                    'e:/dill/test.gdb')