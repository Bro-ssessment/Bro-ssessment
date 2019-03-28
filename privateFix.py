import sys
import os
from excelParser import fixPrivate

def main(argv):

    path = os.path.join('spreadsheets')
    classid = 0

    for root, dirs, files in os.walk(path):
        for filename in files:
            print("Now parsing "+ filename)
            filePath = os.path.join('spreadsheets', filename)
            fixPrivate(filePath)
            print("Finished")
    return

if __name__ == '__main__':
    main(sys.argv[1:])
