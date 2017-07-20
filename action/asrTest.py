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
        self.data = data

        self.testId = testId

        if message["url"] != "":
            # folder = str(self.caseId)+str(message["version"])+str(testId)+str(commonFunc.public_methods.getDateTime)
            self.toolPath  = self.data["config"].split("decoder.conf")[0]
            commonFunc.public_methods.downLoad(message["url"],str(self.toolPath)+"HawkDecoder")

        if  self.checkTestCase() == 1:
            commonFunc.check_test.chenckTest(self.message,testId)
        else:
            return

    def checkTestCase(self):

        self.caseList = self.testCase["caselist"]
        self.answerList = self.testCase["answer"]
        self.decoderConfig = self.data["config"]
        self.asrResult = self.toolPath + "ar/" + commonFunc.public_methods.getDateTime(1,0)
        self.asrLog = self.toolPath + "ar/" + commonFunc.public_methods.getDateTime(1,0) + ".log"

        try:
            self.doTest()

        except Exception as e:
            print e
            return 0
        return 1

    def doTest(self):

        tools = "HawkDecoder"
        pwd = os.getcwd()
        os.chdir(self.toolPath)

        os.system('chmod +x ' + tools)

        print self.caseId, "do test", "-----------", threading.current_thread().getName()

        os.system('./'+tools+' --config '+self.decoderConfig+
                  " --filelist "+self.caseList+" --log "+self.asrResult+" --sleep 2 >>"+self.asrLog)


        os.chdir(pwd) #切换回原始路径