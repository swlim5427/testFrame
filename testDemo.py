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

    strId = "100004"
    strCaseId = "asr_1"
    list = ["asr_2","asr_3","asr_4"]

    cSql = "create table testFrame (id text,caseId text,nextId text);"
    iSql = "insert into testFrame VALUES (\""+str(strId)+"\",\""+str(strCaseId)+"\",\""+str(list)+"\");"


    sSql = "select nextId from testFrame where id ="+strId+";"
    # sSql = "select id from testFrame ORDER BY id DESC limit 0,1"
    countSql = "select count(*) from testFrame;"

    dSql = "drop table testFrame;"

    sqliteConnect([iSql, 0])
    # a = sqliteConnect([sSql,0])

    for ida in sqliteConnect([sSql,0]):
        print ida[0]

    getNextCaseId(ida[0])

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