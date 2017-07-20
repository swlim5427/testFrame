# coding=utf-8
import commonFunc
import threading
import json
import time
import os

class asrTest():

    def __init__(self,message,testCase,testId,data,testTools):

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
        self.runTime = commonFunc.public_methods.getDateTime(1,0)

        self.testPath = self.data["config"].split("decoder.conf")[0]
        #
        # self.asrResult = self.testPath,self.caseId+"-",self.testId,"/result/",self.runTime
        # self.asrLog = self.testPath,"log/",self.runTime,".log"




        self.doTest()

        commonFunc.check_test.chenckTest(self.message,testId)


    def doTest(self):

        pwd = os.getcwd()
        testFoler = self.caseId+"-" + self.testId
        resultPath,logPath = commonFunc.public_methods.mkdir(self.testPath,testFoler)

        casePath = self.testPath + testFoler
        os.chdir(pwd)


        if self.url != "":

            commonFunc.public_methods.downLoad(self.url, casePath+"/"+self.testTools)

        os.chdir(casePath)

        os.system('chmod +x ' + self.testTools)
        sResult = str(resultPath)+"/"+str(self.runTime)

        print self.caseId, "do test----",self.testId, "-----", threading.current_thread().getName()

        doshell =  "./"+str(self.testTools)+" --config "+str(self.decoderConfig)+" --filelist "+str(self.caseList)+" --log "+str(sResult)+" --sleep 2"

        os.system(doshell)

        os.chdir(pwd) #切换回原始路径
        time.sleep(1)
