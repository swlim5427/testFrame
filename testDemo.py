# coding=utf-8

import requests
import json
import sys
import io
from io import StringIO
import sqlite3
import urllib
import time
import datetime

def getDateTime():
    dateTime = datetime.datetime.now()
    t = str(dateTime.year)+str(dateTime.month)+str(dateTime.day)+str(dateTime.hour)+str(dateTime.minute)+str(dateTime.second)
    # return t

def downLoad():

    def aa(a,b,c):
        per = 100.0 * a * b / c
        if per >100:
            per = 100
        # print '%.2f%%' % per
        elif per == 100:
            print "over"

    url = "http://172.22.144.204:8080/view/TSP/job/TSPDecoder/572/artifact/package/linux/libEngine.a"
    urllib.urlretrieve(url,"22",aa)

    # r = requests.get('http://172.22.144.204:8080/view/TSP/job/TSPDecoder/572/artifact/package/linux/libEngine.a',stream = True)


def listTest():
    list = ['asr_5', ' asr_6', ' asr_7', ' asr_8']
    print list

def httpGet():

    print "dddddddddddddddddd"

    ip = "192.168.170.128:9989/"
    # ip = "192.168.128.54:9989/"
    url = "http://" + ip
    s = requests.session()
    headers = {"Content-type": "application/x-protobuf;charset=utf-8", "Connection": "Keep-Alive"}
    # s.headers.update(headers)
    mainPostMessage = {"caseId": "asr_1", "version": "2.4.0", "times": 5, "tableName": "testCase.xlsx",
                       "url": "http://172.22.144.204:8080/view/TSP/job/TSPDecoder/572/artifact/package/linux/HawkDecoder"}
    # mainPostMessage = {"caseId":"asr_1","times":2,"tableName":"","url":"","id":""}
    message = {"param": json.dumps(mainPostMessage)}
    print message

    postMessage = s.post(url, data=message)
    print postMessage


def sqliteTest():

    strId = "1000002"
    strCaseId = "asr_1"
    list = ["asr_2","asr_3","asr_4"]
    count = "10"


    cSql = "create table testFrame (id text,caseId text,nextId text,count text);"
    sqliteConnect([cSql, 0])
    # ctr = sqliteConnect([cSql, 0])
    #
    # if  ctr == False:
    #     print "1"
        # dSql = "drop table testFrame;"
        # sqliteConnect([dSql, 0])
        # cSql = "create table testFrame (id text,caseId text,nextId text,count text);"
        # sqliteConnect([cSql, 0])

    # iSql = "insert into testFrame VALUES (\""+str(strId)+"\",\""+str(strCaseId)+"\",\""+str(list)+"\",\""+str(count)+"\");"
    #     iSql = "insert into testFrame VALUES (\"100000\",\"\",\"\",\"\");"
    #     sqliteConnect([iSql, 0])

    iSql2 = "insert into testFrame VALUES (\"1000001\",\"\",\"\",\"\");"
    sSql = "select id from testFrame where id ="+strId+";"
    # sSql = "select name from sqlite_master where type = 'table';"
    # sSql = "select id from testFrame ORDER BY id DESC limit 0,1"
    countSql = "select count(*) from testFrame;"
    # sqliteConnect([iSql2, 0])
    dSql = "drop table testFrame;"
    # a = sqliteConnect([sSql,0])


    try:

        for ida in sqliteConnect([countSql,0]):
            lineCount = ida[0]

        if lineCount == 0:
            sqliteConnect([iSql2, 0])
        else:
            dSql = "drop table testFrame;"
            sqliteConnect([dSql, 0])

        # getNextCaseId(ida[0])

    except Exception as e:

        print e


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
            return False


def getNextCaseId(nextId):

    if nextId  != 0:
        if nextId.replace('[', ''):

            nextId = nextId.replace('[', '')
            nextId = nextId.replace(']', '')

        nextId = nextId.replace('\'','')
        nextCaseId = nextId.split(',')
        print "------",nextCaseId[0]
        return nextCaseId
    else:
        return nextId

def openExcel():
    import xlrd
    testTable = xlrd.open_workbook("testcase/testCase.xlsx")
    testTableSheet = testTable.sheets()[0]

    rowNum = testTableSheet.nrows

    for i in range(rowNum):
        if testTableSheet.cell(i, 0).value == "asr_1":
            tValue = testTableSheet.cell(i, 2).value
            testCase = json.loads(tValue)
            nextId = testTableSheet.cell(i, 5).value
            data = testTableSheet.cell(i, 3).value

    print  tValue
    print testCase
    print nextId
    print data



def doShell():
    import os
    s = os.system('cd /home/pachiratest/testCase/path1')
    print s

doShell()

# t = getDateTime()
# downLoad()
# sqliteTest()
# listTest()
# httpGet()
# openExcel()
