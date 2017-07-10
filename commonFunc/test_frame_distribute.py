# coding=utf-8
import xlrd
import json
from action import *
import public_methods


class testFrameDistribute():
    #-----------------------
    def __init__(self,message):
        self.tableName = r"./testcase/"+message["tableName"]
        caseId = message["caseId"]
        self.runTimes = message["times"]
        self.url = message["url"]
        self.haveNext = 0

        if message["id"] == "":
            self.getTestCase()

        else:
            runId = message["id"]
            self.checkNextCase(runId)
    # ------------读取测试表格-----------
    def getTestCase(self):

        testTable = xlrd.open_workbook(self.tableName)
        self.testTableSheet = testTable.sheets()[0]

        self.rowNum = self.testTableSheet.nrows
        nextId,testCase = self.getCase()
        nextCaseId = self.getNextCaseId(nextId)

        sSql = "select id from testFrame ORDER BY id DESC limit 0,1"

        for testId in public_methods.sqliteConnect([sSql,0]):
            self.testId = testId

        iSql = "insert into testFrame VALUES (\""+str(int(testId)+1)+"\",\""+str(self.caseId)+"\",\""+str(nextCaseId)+"\",\""+str(self.runTimes)+"\");"

        public_methods.sqliteConnect([iSql,0])

        self.testDistribute(testCase)
    #------------获取case-----------
    def getCase(self):

        for i in range(self.rowNum):
            if self.testTableSheet.cell(i,0).value == self.caseId:

                tValue = self.testTableSheet.cell(i,2).value
                testCase = json.loads(tValue)
                nextCaseId = self.testTableSheet.cell(i,5).value

                return nextCaseId,testCase
    #------------获取nextid-----------
    def getNextCaseId(self,nextId):

        if nextId != 0:
            if nextId.replace('[', ''):
                nextId = nextId.replace('[', '')
                nextId = nextId.replace(']', '')

            nextId = nextId.replace('\'', '')
            nextCaseId = nextId.split(',')
            print nextCaseId[0]
            return nextCaseId

        else:
            return nextId
    #------------分配测试-----------
    def testDistribute(self,testCase):

        caseType = self.analysisCaseId()

        if caseType == "asr":
            asrTest.asrTest(self.caseId,testCase,self.nextCaseId,self.runTimes,self.testId)

    #-----------测试类型------------
    def analysisCaseId(self):

        caseType = self.caseId.split('_')[0] #---caseID第一位
        return caseType

    #-----------------------

    def checkNextCase(self,runId):
        sSql = "select nextId from testFrame where id ="+runId+";"
        # public_methods.sqliteConnect([sSql,0])
        for nextId in public_methods.sqliteConnect([sSql,0]):
            print nextId[0]
            nextCaseId = self.getNextCaseId(nextId[0])
            caseId = nextCaseId[0]  #执行测试的业务逻辑

    #-----------------------

    def initSqlite(self):
        import public_methods
        public_methods.checkSql()