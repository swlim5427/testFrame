import xlrd
import json
from action import *


class testFrameDistribute():
#-----------------------
    def __init__(self,message):
        self.tableName = r"./testcase/"+message["tableName"]
        self.caseId = message["caseId"]
        self.runTimes = message["times"]
        self.url = message["url"]
        self.getMessage()

    def getMessage(self):

        testTable = xlrd.open_workbook(self.tableName)
        self.testTableSheet = testTable.sheets()[0]

        self.rowNum = self.testTableSheet.nrows
        nextId,testCase = self.getCase()
        self.nextCaseId = self.getNextCaseId(nextId)

        self.testDistribute(testCase)
#-----------------------
    def getCase(self):

        for i in range(self.rowNum):

            if self.testTableSheet.cell(i,0).value == self.caseId:

                tValue = self.testTableSheet.cell(i,2).value
                testCase = json.loads(tValue)
                nextCaseId = self.testTableSheet.cell(i,5).value

                return nextCaseId,testCase
#-----------------------
    def getNextCaseId(self,nextId):

        if nextId  != 0:
            nextCaseId = nextId.split(',')
            return  nextCaseId
        else:
            return nextId
#-----------------------
    def testDistribute(self,testCase):

        caseType = self.analysisCaseId()

        if caseType == "asr":
            asrTest.asrTest(self.caseId,testCase,self.nextCaseId,self.runTimes)
#-----------------------
    def analysisCaseId(self):

        caseType = self.caseId.split('_')[0]
        return caseType

