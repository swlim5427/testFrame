# coding=utf-8
import xlrd
import json
from action import *
import public_methods


class testFrameDistribute():
    #-----------------------
    def __init__(self,message):

        self.message = message
        self.tableName = r"./testcase/"+message["tableName"]
        self.caseId = message["caseId"]
        self.runTimes = message["times"]
        self.url = message["url"]
        self.haveNext = 0

        try:
            runId = message["id"]
            self.checkNextCase(runId)
        except:
            self.getTestCase()

    # ------------读取测试表格-----------
    def getTestCase(self):

        testTable = xlrd.open_workbook(self.tableName)
        self.testTableSheet = testTable.sheets()[0]

        self.rowNum = self.testTableSheet.nrows
        nextId,self.testCase,self.data = self.getCase()

        nextCaseId = self.getNextCaseId(nextId)

        sSql = "select id from testFrame ORDER BY id DESC limit 0,1"

        for testId in public_methods.sqliteConnect([sSql,0]):
            self.testId = testId

        nowCasId = self.caseId
        leftCaseId = nextCaseId

        #记录本次测试初始参数
        iSql = "insert into testFrame VALUES (\""+str(int(testId[0])+1)+"\",\""+str(self.caseId)+"\",\""+str(nextCaseId)+"\",\""+str(0)+"\",\""+str(self.runTimes)+"\",\""+str(nowCasId)+"\",\""+str(leftCaseId)+"\");"
        public_methods.sqliteConnect([iSql,0])

        self.testDistribute()
    #------------获取case-----------
    def getCase(self):

        for i in range(self.rowNum):
            if self.testTableSheet.cell(i,0).value == self.caseId:

                tValue = self.testTableSheet.cell(i,2).value
                testCase = json.loads(tValue)
                nextCaseId = self.testTableSheet.cell(i,5).value
                data = self.testTableSheet.cell(i,3).value

        return nextCaseId,testCase,data
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
    def testDistribute(self):

        caseType = self.analysisCaseId()

        # for i in range(self.runTimes):

        if caseType == "asr":
            # asrTest.asrTest(self.caseId,self.testCase,self.nextCaseId,self.runTimes,self.testId)
            uSql =  "update testFrame SET count = "+"\""+str(1)+"\" where id ="+str(int(self.testId[0])+1)+";"
            public_methods.sqliteConnect([uSql,1])
            asrTest.asrTest(self.message,self.testCase,str(int(self.testId[0])+1),self.data)

    #-----------测试类型------------
    def analysisCaseId(self):

        caseType = self.caseId.split('_')[0] #---caseID第一位
        caseType = self.caseId.split('_')[0] #---caseID第一位
        return caseType

    #-----------------------

    def checkNextCase(self,runId):

        sSql = "select nextId from testFrame where id ="+runId+";"
        # public_methods.sqliteConnect([sSql,0])
        for nextId in public_methods.sqliteConnect([sSql,0]):
            print nextId[0]
            nextCaseId = self.getNextCaseId(nextId[0])
            nowCaseId = nextCaseId[0]  #执行测试的业务逻辑
