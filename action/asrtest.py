# coding=utf-8
import commonfunc
import time
import os


class AsrTest(object):

    def __init__(self, message, testCase, testId, data, testTools):

        self.message = message
        self.caseId = message["caseId"]
        self.url = message["url"]
        self.testCase = testCase
        self.data = data
        self.testId = testId
        self.testTools = testTools

        self.caseList = self.testCase["caselist"]
        self.answerList = self.testCase["answer"]
        self.decoderConfig = self.data["config"]
        self.runTime = commonfunc.public_methods.get_dateTime(1, 0)

        self.testPath = self.data["config"].split("decoder.conf")[0]
        #
        # self.asrResult = self.testPath,self.caseId+"-",self.testId,"/result/",self.runTime
        # self.asrLog = self.testPath,"log/",self.runTime,".log"

        self.do_Test()

        commonfunc.check_test.check_test(self.message, testId)

    def do_Test(self):

        pwd = os.getcwd()
        testFoler = self.caseId+"-" + self.testId
        resultPath, logPath = commonfunc.public_methods.mkdir(self.testPath, testFoler)

        casePath = self.testPath + testFoler
        os.chdir(pwd)

        if self.url != "":
            commonfunc.public_methods.download(self.url, casePath + "/" + self.testTools)

        os.chdir(casePath)

        os.system('chmod +x '+self.testTools)
        sResult = str(resultPath)+"/"+str(self.runTime)

        # print self.caseId, "do test----",self.testId, "-----", threading.current_thread().getName()
        os.system("./"+str(self.testTools)+" --config "+str(self.decoderConfig)+" --filelist "+str(self.caseList)+" --log "+str(sResult)+" --sleep 2")

        os.chdir(pwd)
        time.sleep(1)
