# coding=utf-8
import xlrd
import json
from action import *
import public_methods
import logging


class TestFrameDistribute():

    def __init__(self, message):

        self.message = message
        tpSql = "select path from testPath;"

        for testPath in public_methods.sqlite_connect([tpSql, 0]):
            tablePath = testPath[0]
            print tablePath

        self.tableName = tablePath+"/testcase/"+message["tableName"]
        self.caseId = message["caseId"]
        self.runTimes = message["times"]
        # self.version = message["version"]
        # self.url = message["url"]

        self.haveNext = 0

        self.get_testcase()

    def get_testcase(self):

        testTable = xlrd.open_workbook(self.tableName)
        self.testTableSheet = testTable.sheets()[0]

        self.rowNum = self.testTableSheet.nrows

        for i in range(self.rowNum):
            if self.testTableSheet.cell(i, 0).value == self.caseId:

                tValue = self.testTableSheet.cell(i, 2).value
                self.testCase = json.loads(tValue)

                dValue = self.testTableSheet.cell(i, 3).value
                self.data = json.loads(dValue)
                self.testTools = self.testTableSheet.cell(i, 4).value
                nextId = self.testTableSheet.cell(i, 5).value

        nextCaseId = public_methods.get_nextCaseId(nextId)

        try:
            self.runId = self.message["id"]

        except:

            sSql = "select id from testFrame ORDER BY id DESC limit 0,1"

            for testId in public_methods.sqlite_connect([sSql, 0]):
                self.testId = testId

            nowCasId = self.caseId
            leftCaseId = nextCaseId

            # 记录本次测试初始参数.
            iSql = "insert into testFrame VALUES (" \
                   "\""+str(int(testId[0])+1)+"\",\""+str(self.caseId)+"\",\""+str(nextCaseId)+"\",\""+str(0)+"\",\""+str(self.runTimes)+"\",\""+str(nowCasId)+"\",\""+str(leftCaseId)+"\");"
            public_methods.sqlite_connect([iSql, 0])

        self.test_distribute()

    def test_distribute(self):

        caseType = self.caseId.split('_')[0]

        if caseType == "asr":

            try:
                runId = self.message["id"]
                logging.info(runId, "distribute test")

            except:
                runId = int(self.testId[0])+1

                uSql = "update testFrame SET count = "+"\""+str(1)+"\" where id ="+str(runId)+";"
                public_methods.sqlite_connect([uSql, 1])

            asrtest.AsrTest(self.message, self.testCase, str(runId), self.data, self.testTools)
    def a(self):
        print "1"