import sys
import xlrd
import os
from datetime import datetime
from xlrd import open_workbook
from bs4 import BeautifulSoup
from symspellpy.symspellpy import SymSpell
from brossessment.models import *

# Funtion to get the column lables
# Takes a xlrd sheet object as a parameter
# returns a list of strings
def getSheetLabels(sheet):
    labelCells = sheet.row(0)
    labels = []
    for labelCell in labelCells:
        if labelCell.value != "":
            labels.append(labelCell.value)

    return labels

# Function to strip the HTML data out of strings
# Takes a string
# Returns a string
def stripHTML(HTMLstring):
    soup = BeautifulSoup(HTMLstring, features="html.parser")
    strippedString = soup.get_text()
    return strippedString

def initializeSymSpell(maxEditDistance):
    # this variable can be between 5-7, the hgiher the faster the aglorithim runs but the more memory consumption
    prefixLength = 7
    # create object
    symSpell = SymSpell(maxEditDistance, prefixLength)
    # load dictionary
    dictionaryPath = os.path.join(os.path.dirname(__file__),
                                   "frequency_dictionary_en_82_765.txt")
    termIndex = 0  # column of the term in the dictionary text file
    countIndex = 1  # column of the term frequency in the dictionary text file
    if not symSpell.load_dictionary(dictionaryPath, termIndex, countIndex):
        print("Dictionary file not found")
        return
    return symSpell

def spellCheck(symSpell, maxEditDistance, string):
    suggestions = symSpell.lookup_compound(string, maxEditDistance)
    #print(suggestions[0].term)
    return suggestions[0].term

def getRowList(wb, symSpell, maxEditDistance):
    sheet = wb.sheet_by_index(2)
    labels = getSheetLabels(sheet)

    labelToCellList = []
    for row in range(1,sheet.nrows):
        # Get a list of cell values for the row
        rowList = []
        for col in range(0,sheet.ncols):
            rowList.append(sheet.cell_value(row, col))

        # Make a dictionary of column labels to row values
        labelToCell = {}
        for i in range(len(rowList)):
            label = labels[i]
            cell = rowList[i]
            if type(cell) is str:
                if cell.lower() == 'null':
                    cell = None
            labelToCell[label] = cell

        if labelToCell["BuildsOn"] == 0:
            labelToCell["BuildsOn"] == None

        # private can equal 0 or 1, the excel sheets have 0, 1, and 2 for some reason
        if labelToCell["Private"] != 1 or 0:
            labelToCell["Private"] = 1

        if labelToCell["SharedFlag"] != 1 or 0:
            labelToCell["SharedFlag"] = 1

        if labelToCell["WordCount"] == "":
            labelToCell["WordCount"] = 0

        content = labelToCell["NoteContents"]
        if content is None:
            content == ""
            labelToCell["NoteContents"] = ""

        content = stripHTML(content)
        if symSpell is not None:
            content = spellCheck(symSpell, maxEditDistance, content)

        labelToCell["NoteContents"] = content
        labelToCellList.append(labelToCell)

    return labelToCellList

def getUserSet(rowList):
    userSet = set()
    for row in rowList:
        userSet.add(row["PersonID"])

    return userSet

def parseSheet(filePath, classid, symSpell, maxEditDistance):

    #create class for this workbook
    query = Class.select().where(Class.class_id == classid)
    if not query.exists():
        course = Class.create(class_id=classid, average_sentiment_score=0)
    # print(course)

    wb = open_workbook(filePath)
    labelToCellList = getRowList(wb, symSpell, maxEditDistance)
    #print(labelToCellList)
    userSet = getUserSet(labelToCellList)

    # Make users
    with postgres_db.atomic():
        for user_id in userSet:
            query = User.select().where(User.user_id == user_id)
            if not query.exists():
                User.insert(user_id=user_id).execute()

    with postgres_db.atomic():
        for labelToCell in labelToCellList:
            #if user DNE create user

            user_id = labelToCell["PersonID"]
            # Get post values
            post_id = labelToCell["NoteID"]
            class_id = classid
            #build_on = labelToCell["BuildsOn"]
            title = labelToCell["Title"]
            content = labelToCell["NoteContents"]
            topic_id = labelToCell["TopicID"]
            private = labelToCell["Private"]
            shared = labelToCell["SharedFlag"]
            wordcount = labelToCell["WordCount"]

            #print(post_id)

            query = Post.insert(post_id=post_id, class_id=class_id, user_id=user_id, title=title, content=content, topic_id=topic_id, private=private, shared=shared, wordcount=wordcount)
            query.execute()

    with postgres_db.atomic():
        for labelToCell in labelToCellList:
            builds_on = labelToCell["BuildsOn"]
            if builds_on is not None and builds_on != 0:
                post_id = labelToCell["NoteID"]
                query = Post.update(builds_on=builds_on).where(Post.post_id==post_id)
                query.execute()

    return

def main(argv):

    if len(argv) > 1:
        print("correct usage is python excelParser.py *maxEditDistanceInterger*")
        return -1
    elif len(argv) == 1:
        maxEditDistance = int(argv[0])
        symSpell = initializeSymSpell(maxEditDistance)

    else:
        maxEditDistance=0
        symSpell=None

    rowList = []
    path = os.path.join('spreadsheets')
    classid = 0

    for root, dirs, files in os.walk(path):
        for filename in files:
            tstart = datetime.now()
            classid += 1
            filePath = os.path.join('spreadsheets', filename)
            print("Now parsing "+ filename)
            row = parseSheet(filePath, classid, symSpell, maxEditDistance)
            tend = datetime.now()
            time = tend - tstart
            print("Finished")
            print("It took " + str(time.seconds) + " seconds.")
            print()
            # rowList.append(row)

    # for i in range(1, len(rowList)):
    #     if not (rowList[0] == rowList[i]):
    #         print('Error')

    # wb = open_workbook(wbName)
    # sheets = wb.sheets()
    # colNames = getColNames(sheet)

    return 0

if __name__ == '__main__':
    main(sys.argv[1:])
