import os


class asrTest():

    def __init__(self,caseId,testCase,nextCaseId,runTimes,callback):

        self.caseId = caseId
        self.testCase = testCase
        self.nextCaseId = nextCaseId
        self.runTimes = runTimes
        self.callback = callback
        self.checkTestCase()

    def checkTestCase(self):

        try:
            print self.caseId
            print self.testCase
            print self.nextCaseId
            print self.runTimes
            # os.system("testDemo.py")
            # execfile("testDemo.py")

        except Exception as e:
            print e