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
import codecs
import MySQLdb
import wave
import numpy
import contextlib
import math
import xml


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

    ip = "127.0.0.1:8000/"
    # ip = "192.168.128.54:9989/"
    url = "http://" + ip
    s = requests.session()
    headers = {"Content-type": "application/x-protobuf;charset=utf-8", "Connection": "Keep-Alive"}
    # s.headers.update(headers)
    mainPostMessage = {"caseId": "asr_1", "version": "2.4.0", "times": 1, "tableName": "testCase.xlsx",
                       "url": "http://172.22.144.204:8080/view/TSP/job/TSPDecoder/601/artifact/package/linux/HawkDecoder"}

    # mainPostMessage = {"caseId":"asr_1","times":2,"tableName":"","url":"","id":""}
    message = {"param": json.dumps(mainPostMessage)}
    print message

    postMessage = s.post(url, data=message)
    print postMessage
    print postMessage.text


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

    # print tValue
    # print testCase
    print nextId
    # print data

    if "-" in nextId:
        next_id_list = []
        print "111"
        nextId = nextId.split("-")
        print nextId[0]
        print nextId[1]

        s = nextId[0].split("_")
        e = nextId[1].split("_")

        for i in range(int(s[1]),int(e[1])+1):
            next_id_list.append(s[0]+"_"+str(i))
            print next_id_list
            print next_id_list[0]
    else:
        nextId = nextId.split(",")
        print nextId[2]


def doShell():
    import os
    s = os.system('cd /home/pachiratest/testCase/path1')
    print s


def read_file():

    file = "/Users/swlim/Documents/1500969727601.log"
    # file2 = "/Users/swlim/Documents/1500969727601rate"
    a = codecs.open(file, 'r','utf-8')

    txt = open(r'/Users/swlim/Documents/ttttttt')

    lines = []
    erase = False
    for line in txt:
        if line.strip() == "Real time(s):":
            erase = True
        if not erase:
            lines.append(line)
        if line.strip() == "W-------------------------------------------------------":
            erase = False
        if line.strip() == "========================================================":
            erase = True

    txt.close()
    open(r'/Users/swlim/Documents/t_r.txt','w').writelines(lines)

    rtk = ",rt:"
    for line in reversed(a.readlines()):
        if rtk in line:
            rLine = line.split(rtk)[1]
            rt = "rt:"+rLine
            a.close()
    print rt

    rff = "/Users/swlim/Documents/t_r.txt"

    b = codecs.open(rff,'r+','utf-8')
    c = b.read()
    b.seek(0)
    b.write(rt+'\n')
    b.write(c)
    b.close()
    # for line in a:
    #     print line


def mysql_connect():
    conn = MySQLdb.connect(host='127.0.0.1',port= 3306,user= 'root',passwd= '123456',db= 'testframe' )
    cur = conn.cursor()
    sql = "select count(*) from testservice_testframe;"
    try:
        sqlResult = cur.execute(sql)
        rList = cur.fetchmany(sqlResult)

        cur.close()
        conn.commit()
        conn.close()
        print rList[0][0]
        # print sqlResult

    except Exception as e:
        print e
    # print "test"


def test_list():

    t_list=['', 'PASR', '', '', '', '', '', 'Snt', '', '', 'Wrd', '', 'Corr', '', '', '', 'Sub', '', '', '', 'Del', '', '', '', 'Ins', '', '', '', 'Err', '', 'S.Err', '']

    L=[]
    for v in t_list:



      v = str.strip(v)
      if v:
          L.append(v)
    print L


def txt():

    txt = open(r'/Users/swlim/work/t1.txt')

    lines = []
    erase = False
    for line in txt:
        if line.strip() == "Real time(s):":
            erase = True
        if not erase:
            lines.append(line)
        if line.strip() == "W-------------------------------------------------------":
            erase = False
        if line.strip() == "========================================================":
            erase = True

    txt.close()
    open(r'/Users/swlim/work/t_r.txt','w').writelines(lines)


def json_test():

    j = {"caseId":"asr_1","version":"2.4.0","times":1,"tableName":"test-case.xlsx","url":{"url1":"artifact/package/linux/HawkDecoder","url2":"artifact1/package/linux/HawkDecoder"}
}
    print j["url"]

    kl = j["url"].keys()
    print kl

    vl = j["url"].values()

    for i in range(1):
        print i


    print vl

    print kl[0]
    print kl[1]

    print j["url"][kl[1]],j["url"][kl[0]]
    #
    # print kl[0]


def char_test():
    c = "http://172.22.144.204:8080/job/TSPDecoder_test/48/artifact/package/linux/libdecoder_dynamic.so"

    l = c.split("/")

    print len(l)

    print l[len(l)-1]


def wav_test(name):

    with contextlib.closing(wave.open(bytes(name).decode('utf-8'), 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        # print duration
        return int(math.floor(duration*1000))


def ref_test():

    ref_file = "/Users/swlim/Desktop/pachira_work/toxml/t_list.ref"
    ref_path = "/Users/swlim/Desktop/pachira_work/toxml"

    ref_file_open = open(ref_file)

    for line in ref_file_open:
        line_n = line.strip().split(" ")
        n = len(line_n)
        line_n_2 = line_n[n-1].split("	")
        voice_name = line_n[0] + " " + line_n_2[0]
        voice_answer = line_n_2[1]
        voice_time = wav_test(voice_name)
        xml_test(voice_time, voice_answer)


def xml_test(voice_time, answer):
    # print "name : " + name
    # print "answer : " + answer

    print voice_time
    print answer

    # wav_file_list = os.system("cat /Users/swlim/Desktop/pachira_work/toxml/t_list.ref |awk '{print $1$2}'")
    # print wav_file_list

# txt()
# read_file()
# mysql_connect()
# doell()
# t = getDateTime()
# downLoad()
# sqliteTest()
# lis# est()
# httpGet()
# test_list()
# openExcel()
# json_test()
# char_test()
# wav_test()
ref_test()
