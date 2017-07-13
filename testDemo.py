# -*- coding: utf-8 -*-

# from twisted.internet import defer, reactor
# from twisted.internet.threads import deferToThread
#
# import functools
# import time
#
#
# # 耗时操作 这是一个同步阻塞函数
# def mySleep(timeout):
#     for i  in range(timeout):
#
#
#     # 返回值相当于加进了callback里
#         print i
#         time.sleep(1)
#     # return 3
#
#
# def say(result):
#     print "耗时操作结束了, 并把它返回的结果给我了", result
#
#
# # 用functools.partial包装一下, 传递参数进去
# cb = functools.partial(mySleep, 10)
# d = deferToThread(cb)
# # d.addCallback(say)
#
# print "你还没有结束我就执行了, 哈哈"
#
# reactor.run()


import requests
import json
import sys
import io
from io import StringIO
import sqlite3

def httpGet():

    print "dddddddddddddddddd"

    ip = "172.21.10.227:9989/"
    url = "http://"+ip
    s = requests.session()
    headers ={"Content-type": "application/x-protobuf;charset=utf-8","Connection":"Keep-Alive"}
    # s.headers.update(headers)
    print s.get(url)

    mainPostMessage = {"caseId":"0","times":0,"tableName":"","url":"","id":"101"}
    message ={"param":json.dumps(mainPostMessage)}
    print message

    postMessage = s.post(url,data=message)
    print postMessage

def sqliteTest():

    strId = "1000002"
    strCaseId = "asr_1"
    list = ["asr_2","asr_3","asr_4"]
    count = "10"


    cSql = "create table testFrame (id text,caseId text,nextId text,count text);"
    ctr = sqliteConnect([cSql, 0])

    if  ctr == False:
        print "1"
        # dSql = "drop table testFrame;"
        # sqliteConnect([dSql, 0])
        # cSql = "create table testFrame (id text,caseId text,nextId text,count text);"
        # sqliteConnect([cSql, 0])

    # iSql = "insert into testFrame VALUES (\""+str(strId)+"\",\""+str(strCaseId)+"\",\""+str(list)+"\",\""+str(count)+"\");"
    #     iSql = "insert into testFrame VALUES (\"100000\",\"\",\"\",\"\");"
    #     sqliteConnect([iSql, 0])

    # iSql2 = "insert into testFrame VALUES (\"1000001\",\"\",\"\",\"\");"
    sSql = "select id from testFrame where id ="+strId+";"
    # sSql = "select name from sqlite_master where type = 'table';"
    # sSql = "select id from testFrame ORDER BY id DESC limit 0,1"
    countSql = "select count(*) from testFrame;"
    # sqliteConnect([iSql2, 0])
    dSql = "drop table testFrame;"
    # a = sqliteConnect([sSql,0])

    try:

        for ida in sqliteConnect([sSql,0]):
            print ida[0]

        getNextCaseId(ida[0])

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


sqliteTest()

# if __name__ == '__main__':
#     # httpGet()
#
#     print "start"
#
#     sqliteTest()