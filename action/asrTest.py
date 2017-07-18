# coding=utf-8
import commonFunc
import threading
import json
import os

class asrTest():

    def __init__(self,message,testCase,testId,data):

        self.message = message
        self.caseId = message["caseId"]
        self.testCase = testCase
        self.data = json.loads(data)

        self.testId = testId

        if message["url"] != "":
            # folder = str(self.caseId)+str(message["version"])+str(testId)+str(commonFunc.public_methods.getDateTime)
            toolPath  = self.data["config"].split("config")[0]
            commonFunc.public_methods.downLoad(message["url"],str(toolPath)+"HawkDecoder")

        if  self.checkTestCase() == 1:
            commonFunc.check_test.chenckTest(self.message,testId)
        else:
            return

    def checkTestCase(self):

        try:
            self.doTest()

        except Exception as e:
            print e
            return 0
        return 1

    def doTest(self):

        tools = "HawkDecoder"
        pwd = os.getcwd()
        os.chdir('/home/pachiratest/testCase/path1')
        # print os.system('ls')
        os.system('chmod +x ' + tools)
        os.system('./' + tools)

        print self.caseId,"do test","-----------",threading.current_thread().getName()
        os.chdir(pwd)