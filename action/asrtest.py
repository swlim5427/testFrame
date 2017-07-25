# coding=utf-8
import commonfunc
import time
import os
import codecs

class AsrTest(object):

    def __init__(self, message, testCase, testId, data, testTools):

        self.message = message
        self.caseId = message["caseId"]
        self.url = message["url"]
        self.version = message["version"]

        try:
            self.count = self.message["count"]
        except KeyError:
            self.count = 1

        self.testCase = testCase
        self.data = data
        self.testId = testId
        self.testTools = testTools

        self.caseList = self.testCase["caselist"]
        self.answerList = self.testCase["answer"]
        self.decoderConfig = self.data["config"]

        self.runTime = commonfunc.public_methods.get_dateTime(1, 0)

        #
        # self.asrResult = self.testPath+self.caseId+"-"+self.testId+"/result/",self.runTime
        # self.asrLog = self.testPath+"log/"+self.runTime+".log"

        self.do_Test()

        commonfunc.check_test.check_test(self.message, testId)

    def do_Test(self):

        pwd = os.getcwd()
        testFolder = self.version+"-" + self.caseId+"-" + self.testId
        testPath = self.data["config"].split("decoder.conf")[0]
        answerPath = self.testCase["answer"].split("answer.list")[0]

        resultPath, logPath = commonfunc.public_methods.mkdir(testPath, testFolder)

        casePath = testPath + testFolder
        os.chdir(pwd)

        if self.url != "":
            commonfunc.public_methods.download(self.url, casePath + "/" + self.testTools)

        os.chdir(casePath)

        os.system('chmod +x '+self.testTools)
        lResult = str(resultPath) + "/" + str(self.count) + ".log"
        sResult = str(resultPath) + "/" + str(self.count)

        # print self.caseId, "do test----",self.testId, "-----", threading.current_thread().getName()
        os.system("./"+str(self.testTools)+" --config "+str(self.decoderConfig)+" --filelist "+str(self.caseList)+" --log "+str(self.count)+" --sleep 2 >>"+lResult)
        os.chdir(answerPath)

        os.system("python pasr_calc_recrate.py -s sclite -m answer.list -r "+str(sResult)+" -o "+str(self.count)+"rate")

        rlResult = codecs.open(lResult,'r','utf-8')
        rt = ",rt:"
        for line in reversed(rlResult.readlines()):
            if rt in line:
                rLine = line.split(rt)[1]
                rt = "rt:"+rLine
                rlResult.close()

        testResult = codecs.open(str(sResult)+"rate", 'r+', 'utf-8')
        rTestResult = testResult.read()
        testResult.seek(0)
        testResult.write(rt+'\n')
        testResult.write(rTestResult)
        testResult.close()

        os.chdir(pwd)
        time.sleep(1)
