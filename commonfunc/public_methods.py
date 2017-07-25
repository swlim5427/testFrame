# coding=utf-8

import threading
import sqlite3
import test_frame_distribute
import datetime
import os
import time


def sqlite_connect(sql):
    conn = sqlite3.connect('/tmp/testFrame.db')
    if sql[1] == 2:
        conn.close()
    else:
        try:
            cur = conn.execute(sql[0])
            conn.commit()
            if sql[1] == 1:
                conn.close()
                return cur
            else:
                return cur
        except Exception as e:
            print e
            return False


def init_table():

    path = os.getcwd()

    ctfSql = "create table testFrame (" \
             "id text,caseId text,nextId text,count text,times text,nowCaseId text,leftNextId text);"

    cpSql = "create table testPath (path text);"

    '''
    id:执行id
    caseId:启动测试的用例id
    nextid:本次除caseId外所需要执行的caseId
    count:当前执行到第几次
    times:总计要执行多少次
    nowCaseId:当前执行的caseId
    leftNextId:剩余要执行的caseId
    '''

    sqlite_connect([ctfSql, 0])
    sqlite_connect([cpSql, 0])

    countSql = "select count(*) from testFrame;"
    itfSql = "insert into testFrame VALUES (""" \
             "\"1000001\",\"\",\"\",\"\",\"\",\"\",\"\");"

    ipSql = "insert into testPath VALUES ("+"\""+path+"\")"

    try:
        for ida in sqlite_connect([countSql, 0]):
            lineCount = ida[0]

        if lineCount == 0:

            sqlite_connect([itfSql, 0])
            sqlite_connect([ipSql, 0])
        # else:
        #     dSql = "drop table testFrame;"
        #     sqliteConnect([dSql, 0])

        # getNextCaseId(ida[0])

    except Exception as e:
        print e


def create_threading(param):

    p = []
    p.append(param)
    print "new threading"
    nThreading = threading.Thread(target=test_frame_distribute.TestFrameDistribute, args=(p))

    return nThreading


def get_nextCaseId(nextId):

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


def download(url, path):

    import urllib

    def reporthook(a, b, c):
        per = 100.0 * a * b / c

        if per > 100:
            per = 100
            print '%.2f%%' % per
        elif per == 100:
            print '%.2f%%' % per
        # print '%.2f%%' % per
        # else:
        #     print '%.2f%%' % per1
    urllib.urlretrieve(url, path, reporthook)


def get_dateTime(fileName, NowTime):

    dateTime = datetime.datetime.now()

    if fileName == 1 and NowTime == 0:

        inputYear = dateTime.year
        inputMonth = dateTime.month
        inputDay = dateTime.day
        inputHour = dateTime.hour
        inputMinute = dateTime.minute
        inputSecond = dateTime.second

        mTime = dateTime.microsecond
        imputDateTime = datetime.datetime(year=int(inputYear), month=int(inputMonth), day=int(inputDay),
                                          hour=int(inputHour), minute=int(inputMinute), second=int(inputSecond))
        formatTime = long(round(time.mktime(imputDateTime.timetuple())))

        nowTime = long(str(formatTime) + str(mTime/1000))

        return nowTime

    else:
        return dateTime


def mkdir(testPath, testFolder):

    os.chdir(testPath)
    try:
        os.makedirs(testFolder)
        os.chdir(testFolder)
        os.makedirs("result")
        os.makedirs("log")

    except IOError as e:
        print e

    result = str(testPath) + str(testFolder) + "/" + "result"
    log = str(testPath) + str(testFolder) + "/" + "log"
    return result, log
