import sys
import xlrd
import os
from xlrd import open_workbook

def main(argv):

    wbName = argv[0]

    wb = open_workbook(wbName)
    sheets = wb.sheets()
    colNames = getColNames(sheet)

    return 0
