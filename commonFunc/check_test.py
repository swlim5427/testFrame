# coding=utf-8

import public_methods
import test_frame_distribute


def chenckTest(message,testId):


    sSql = "select * from testFrame where id ="+str(testId)+";"
    for r in public_methods.sqliteConnect([sSql,0]):
        caseId = r[1]
        nextId = r[2]
        count = r[3]
        times = r[4]
        leftNextId = public_methods.getNextCaseId(r[6])

    # 剩余caseId 为 0 时进入下个循环,count = times 时结束测试

    if count != times:

        if leftNextId != [u'']:

            uNowCaseId = leftNextId[0]
            del leftNextId[0]

            uSql = "update testFrame SET nowCaseId ="+"\""+str(uNowCaseId)+"\",leftNextId ="+"\""+str(
                leftNextId)+"\" where id =" + str(testId) + ";"

            print "test:", count, "========", times, "---nowCaseId", uNowCaseId
                # sqliteConnect([uSql,1])
                #
                # message.setdefault('id',testId)
                # message.update({'caseId':uNowCaseId})
        else:

            uNowCaseId = caseId
            leftNextId = nextId
            print "test:", count, "========", times, "---nowCaseId", uNowCaseId
            uCount = int(count) + 1

            uSql = "update testFrame SET nowCaseId =" + "\""+str(uNowCaseId)+"\",leftNextId =" + "\"" + str(
                leftNextId) + "\",count =" + "\"" + str(uCount) + "\" where id ="+str(testId)+";"

        public_methods.sqliteConnect([uSql, 1])

        message.setdefault('id', testId)
        message.update({'caseId': uNowCaseId})

        print "test:", count, "========", times,"---nowCaseId",uNowCaseId
        test_frame_distribute.testFrameDistribute(message)
    else:
        print "test all overs"