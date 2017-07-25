# coding=utf-8

import public_methods
import test_frame_distribute
import threading


def check_test(message, testId):

    sSql = "select * from testFrame where id ="+str(testId)+";"
    for r in public_methods.sqlite_connect([sSql, 0]):
        caseId = r[1]
        nextId = r[2]
        count = r[3]
        times = r[4]
        leftNextId = public_methods.get_nextCaseId(r[6])

    # 剩余caseId 为 0 时进入下个循环,count = times 并且 leftNextId 为空 时结束测试

    if count != times or leftNextId != [u'0']:

        if leftNextId != [u'0']:

            uNowCaseId = leftNextId[0]
            del leftNextId[0]

            if len(leftNextId) == 0:
                leftNextId = [0]

            uSql = "update testFrame SET nowCaseId ="+"\""+str(uNowCaseId)+"\",leftNextId ="+"\""+str(
                leftNextId)+"\" where id =" + str(testId) + ";"
            # print "test:", count, "========", times, "---nowCaseId", uNowCaseId

        else:

            uNowCaseId = caseId
            leftNextId = nextId
            uCount = int(count) + 1

            uSql = "update testFrame SET nowCaseId =" + "\""+str(uNowCaseId)+"\",leftNextId =" + "\"" + str(
                leftNextId) + "\",count =" + "\"" + str(uCount) + "\" where id ="+str(testId)+";"

        public_methods.sqlite_connect([uSql, 1])

        message.setdefault('id', testId)
        message.setdefault('count', uCount)
        message.update({'caseId': uNowCaseId})


        test_frame_distribute.TestFrameDistribute(message)
    else:

        print "test overs -----------", threading.current_thread().getName()
