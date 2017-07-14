# coding=utf-8
import commonFunc


class asrTest():

    def __init__(self,message,testCase,testId,data):

        self.message = message
        self.caseId = message["caseId"]
        self.testCase = testCase
        self.data = data

        # self.nextCaseId = message["nextCaseId"]
        # self.runTimes = message["runTimes"]
        self.testId = testId

        if  self.checkTestCase() == 1:
            commonFunc.public_methods.callback(self.message,testId)
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
        print "do test"
        # public_methods.callback()