

class asrTest():
    def __init__(self,caseId,testCase,nextCaseId,runTimes):
        self.caseId = caseId
        self.testCase = testCase
        self.nextCaseId = nextCaseId
        self.runTimes = runTimes

        self.checkTestCase()

    def checkTestCase(self):
        print self.caseId
        print self.testCase
        print self.nextCaseId
        print self.runTimes