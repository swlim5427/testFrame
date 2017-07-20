# coding=utf-8
import xlrd
import json
from action import *
import public_methods
import logging


class testFrameDistribute():
    #-----------------------
    def __init__(self,message):

        self.message = message
        self.tableName = r"./testcase/"+message["tableName"]
        self.caseId = message["caseId"]
        self.runTimes = message["times"]
        # self.version = message["version"]
        # self.url = message["url"]

        self.haveNext = 0

        self.getTestCase()

    # ------------读取测试表格-----------
    def getTestCase(self):

        testTable = xlrd.open_workbook(self.tableName)
        self.testTableSheet = testTable.sheets()[0]

        self.rowNum = self.testTableSheet.nrows

        for i in range(self.rowNum):
            if self.testTableSheet.cell(i,0).value == self.caseId:

                tValue = self.testTableSheet.cell(i,2).value
                self.testCase = json.loads(tValue)

                dValue = self.testTableSheet.cell(i,3).value
                self.data = json.loads(dValue)
                self.testTools = self.testTableSheet.cell(i, 4).value
                nextId = self.testTableSheet.cell(i, 5).value

        nextCaseId = public_methods.getNextCaseId(nextId)

        try:
            self.runId = self.message["id"]

        except:

            sSql = "select id from testFrame ORDER BY id DESC limit 0,1"

            for testId in public_methods.sqliteConnect([sSql,0]):
                self.testId = testId

            nowCasId = self.caseId
            leftCaseId = nextCaseId

            #记录本次测试初始参数
            iSql = "insert into testFrame VALUES (" \
                   "\""+str(int(testId[0])+1)+"\",\""+str(self.caseId)+"\",\""+str(nextCaseId)+"\",\""+str(0)+"\",\""+str(self.runTimes)+"\",\""+str(nowCasId)+"\",\""+str(leftCaseId)+"\");"
            public_methods.sqliteConnect([iSql,0])

        self.testDistribute()

    #------------分配测试-----------
    def testDistribute(self):

        caseType = self.caseId.split('_')[0]

        if caseType == "asr":

            try:
                runId = self.message["id"]
                logging.info(runId, "distribute test")
            except:
                runId = int(self.testId[0])+1

                uSql =  "update testFrame SET count = "+"\""+str(1)+"\" where id ="+str(runId)+";"
                public_methods.sqliteConnect([uSql,1])

            asrTest.asrTest(self.message,self.testCase,str(runId),self.data,self.testTools)

