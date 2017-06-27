import xlrd
import json

def testFrameDistribute(message):

    # tableName = message["tableName"]
    tableName = r"/testcase/"+message["tableName"]
    # tableName = message["/testcase/testCase.xlsx"]
    caseId = message["caseId"]

    testTable = xlrd.open_workbook(tableName)
    testTableSheet = testTable.sheets()[0]

    rowNum = testTableSheet.nrows
    getCase(testTableSheet,rowNum,caseId)

def getCase(tableName,rowNum,caseId):
    for i in range(rowNum):
        if tableName.row_value(i) == caseId:
            tValue = tableName.cell(i,2).value
            s = json.loads(tValue)
            print s
            print s["key1"]