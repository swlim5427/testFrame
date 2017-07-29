# coding=utf-8

import public_methods
import test_frame_distribute
import threading


def check_test(message, test_id):

    global count
    global times
    global left_next_id
    global case_id
    global next_id
    global update_count

    select_sql = "select * from testFrame where id ="+str(test_id)+";"
    for r in public_methods.sqlite_connect([select_sql, 0]):

        case_id = r[1]
        next_id = r[2]
        count = r[3]
        times = r[4]

        left_next_id = public_methods.get_next_caseid(r[6])

    # 剩余caseId 为 0 时进入下个循环,count = times 并且 leftNextId 为空 时结束测试

    if count != times or left_next_id != [u'0']:
        global update_case_id

        if left_next_id != [u'0']:

            now_case_id = left_next_id[0]
            del left_next_id[0]

            if len(left_next_id) == 0:
                left_next_id = [0]

            update_sql = "update testFrame SET nowCaseId ="+"\""+str(now_case_id)+"\",leftNextId ="+"\""+str(
                left_next_id)+"\" where id =" + str(test_id) + ";"
            # print "test:", count, "========", times, "---nowCaseId", uNowCaseId

        else:
            global update_count
            update_case_id = case_id
            left_next_id = next_id
            update_count = int(count) + 1

            update_sql = "update testFrame SET nowCaseId =" + "\""+str(update_case_id)+"\",leftNextId =" + "\"" + str(
                left_next_id) + "\",count =" + "\"" + str(update_count) + "\" where id ="+str(test_id)+";"

        public_methods.sqlite_connect([update_sql, 1])

        try:
            message.update({'count': update_count})
        except Exception as e:
            print e
            message.setdefault('count', 1)

        message.setdefault('id', test_id)
        message.update({'caseId': update_case_id})

        test_frame_distribute.TestFrameDistribute(message)
    else:

        print "test overs -----------", threading.current_thread().getName()
