import sys
import xlrd
import os
from xlrd import open_workbook
from bs4 import BeautifulSoup
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

def parseSheet(filePath, classid):

    #create class for this workbook
    query = Class.select().where(Class.class_id == classid)
    if not query.exists():
        course = Class.create(class_id=classid, average_sentiment_score=0)
    # print(course)

    wb = open_workbook(filePath)
    sheet = wb.sheet_by_index(2)
    labels = getSheetLabels(sheet)

    userSet = set()
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

        userSet.add(labelToCell["PersonID"])

        if labelToCell["BuildsOn"] == 0:
            labelToCell["BuildsOn"] == None
        content = labelToCell["NoteContents"]
        if content is None:
            labelToCell["NoteContents"] = ""
        labelToCellList.append(labelToCell)

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
            content = stripHTML(labelToCell["NoteContents"])
            topic_id = labelToCell["TopicID"]

            # private can equal 0 or 1, the excel sheets have 0, 1, and 2 for some reason
            private = labelToCell["Private"]
            if private == 2:
                private = 1

            shared = labelToCell["Shared"]
            if shared == 2:
                shared = 1

            #print(post_id)

            query = Post.insert(post_id=post_id, class_id=class_id, user_id=user_id, title=title, content=content, topic_id=topic_id)
            query.execute()

    with postgres_db.atomic():
        for labelToCell in labelToCellList:
            builds_on = labelToCell["BuildsOn"]
            if builds_on is not None and builds_on != 0:
                post_id = labelToCell["NoteID"]
                print
                query = Post.update(builds_on=builds_on).where(Post.post_id==post_id)
                query.execute()




        # Get post values
        # post_id = labelToCell["NoteID"]
        # class_id = classid
        # user_id = labelToCell["PersonID"]
        # build_on = labelToCell["BuildsOn"]
        # title = labelToCell["Title"]
        # content = stripHTML(noteContent)
        # topic_id = labelToCell["TopicID"]
        #
        # print(post_id)
        # post = Post.create(post_id=post_id, class_id=class_id, user_id=user_id, build_on=build_on, title=title, content=content, topic_id=topic_id)

    return


def main():
    rowList = []
    path = os.path.join('spreadsheets')
    classid = 0
    for root, dirs, files in os.walk(path):
        for filename in files:
            classid += 1
            filePath = os.path.join('spreadsheets', filename)
            print("Now parsing "+ filename)
            row = parseSheet(filePath, classid)
            print("Finished")
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
    main()
