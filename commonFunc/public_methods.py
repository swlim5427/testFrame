# coding=utf-8

import threading
import sqlite3
import test_frame_distribute
import datetime


def sqliteConnect(sql):
    conn = sqlite3.connect('testFrame.db')
    if sql[1] == 2:
        conn.close()
    else:
        try:
            cur = conn.execute(sql[0]);
            conn.commit()
            if sql[1] == 1:
                conn.close()
                return cur
            else:
                return cur
        except Exception as e:
            print e
            return False
# --------------------------------------------------------------------------
def initTable():

    cSql = "create table testFrame (" \
           "id text,caseId text,nextId text,count text,times text,nowCaseId text,leftNextId text);"
    # id:执行id
    # caseId:启动测试的用例id
    # nextid:本次除caseId外所需要执行的caseId
    # count:当前执行到第几次
    # times:总计要执行多少次
    # nowCaseId:当前执行的caseId
    # leftNextId:剩余要执行的caseId
    sqliteConnect([cSql, 0])

    countSql = "select count(*) from testFrame;"
    iSql = "insert into testFrame VALUES (" \
           "\"1000001\",\"\",\"\",\"\",\"\",\"\",\"\");"

    try:
        for ida in sqliteConnect([countSql,0]):
            lineCount = ida[0]
        if lineCount == 0:

            sqliteConnect([iSql, 0])
        # else:
        #     dSql = "drop table testFrame;"
        #     sqliteConnect([dSql, 0])

        # getNextCaseId(ida[0])

    except Exception as e:
        print e
# --------------------------------------------------------------------------
def createThreading(param):

    p = []
    p.append(param)
    print "new threading"
    nThreading = threading.Thread(target=test_frame_distribute.testFrameDistribute,args=(p))

    return nThreading


# --------------------------------------------------------------------------
def getNextCaseId(nextId):

    if nextId != 0:
        if nextId.replace('[', ''):
            nextId = nextId.replace('[', '')
            nextId = nextId.replace(']', '')
        nextId = nextId.replace('u\'', '')
        nextId = nextId.replace('\'', '')
        nextId = nextId.replace(' ', '')
        nextCaseId = nextId.split(',')
        return nextCaseId

    else:
       return nextId

# --------------------------------------------------------------------------

def downLoad(url,path):

    import urllib

    def reporthook(a,b,c):
        per = 100.0 * a * b / c
        if per >100:
            per = 100
            r = per
        # print '%.2f%%' % per
        elif per == 100:
            r = per

    urllib.urlretrieve(url,path,reporthook)

# --------------------------------------------------------------------------

def getDateTime(fileName,NowTime):

    dateTime = datetime.datetime.now()

    if fileName == 1 and NowTime == 0:
        fileName = str(dateTime.year)+str(dateTime.month)+str(dateTime.day)+str(dateTime.hour)+str(dateTime.minute)+str(dateTime.second)
        return fileName
    else:
        return NowTime