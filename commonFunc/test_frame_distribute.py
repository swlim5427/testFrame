import xlrd
import json
from action import *

class testFrameDistribute():

    def getMessage(self,message):

        # tableName = message["tableName"]
        tableName = r"./testcase/"+message["tableName"]
        # tableName = message["/testcase/testCase.xlsx"]
        caseId = message["caseId"]

        testTable = xlrd.open_workbook(tableName)
        testTableSheet = testTable.sheets()[0]

        rowNum = testTableSheet.nrows
        nextCaseId,testCase = self.getCase(testTableSheet,rowNum,caseId)

        print nextCaseId
        print testCase


    def getCase(self,tableName,rowNum,caseId):
        for i in range(rowNum):
            if tableName.cell(i,0).value == caseId:
                tValue = tableName.cell(i,2).value
                testCase = json.loads(tValue)
                nextCaseId = tableName.cell(i,5).value
                return nextCaseId,testCase

