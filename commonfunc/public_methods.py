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

    ctf_sql = "create table testFrame " \
              "(""id text,caseId text,nextId text,count text,times text,nowCaseId text,leftNextId text);"

    cp_sql = "create table testPath (path text);"

    '''
    id:执行id
    caseId:启动测试的用例id
    nextid:本次除caseId外所需要执行的caseId
    count:当前执行到第几次
    times:总计要执行多少次
    nowCaseId:当前执行的caseId
    leftNextId:剩余要执行的caseId
    '''

    sqlite_connect([ctf_sql, 0])
    sqlite_connect([cp_sql, 0])

    count_sql = "select count(*) from testFrame;"
    itf_sql = "insert into testFrame VALUES (""\"1000001\",\"\",\"\",\"\",\"\",\"\",\"\");"

    ip_sql = "insert into testPath VALUES ("+"\""+path+"\")"
    line_count = ""
    try:
        # global line_count
        for ida in sqlite_connect([count_sql, 0]):
            line_count = ida[0]

        if line_count == 0:

            sqlite_connect([itf_sql, 0])
            sqlite_connect([ip_sql, 0])
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
    new_threading = threading.Thread(target=test_frame_distribute.TestFrameDistribute, args=p)

    return new_threading


def get_next_caseid(next_id):

    if next_id != 0:
        if next_id.replace('[', ''):
            next_id = next_id.replace('[', '')
            next_id = next_id.replace(']', '')
        next_id = next_id.replace('u\'', '')
        next_id = next_id.replace('\'', '')
        next_id = next_id.replace(' ', '')
        next_caseid = next_id.split(',')
        return next_caseid

    else:
        return next_id


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


def get_date_time(file_name, now_time):

    date_time = datetime.datetime.now()

    if file_name == 1 and now_time == 0:

        input_year = date_time.year
        input_month = date_time.month
        input_day = date_time.day
        input_hour = date_time.hour
        input_minute = date_time.minute
        input_second = date_time.second
        microsecond_time = date_time.microsecond

        imput_datetime = datetime.datetime(
                year=int(input_year),
                month=int(input_month),
                day=int(input_day),
                hour=int(input_hour),
                minute=int(input_minute),
                second=int(input_second)
        )
        format_time = long(round(time.mktime(imput_datetime.timetuple())))

        now_time = long(str(format_time) + str(microsecond_time/1000))

        return now_time

    else:
        return date_time


def mkdir(test_path, test_folder):

    os.chdir(test_path)
    try:
        os.makedirs(test_folder)
        os.chdir(test_folder)
        os.makedirs("result")
        os.makedirs("log")

    except Exception as e:
        print e

    result = str(test_path) + str(test_folder) + "/" + "result"
    log = str(test_path) + str(test_folder) + "/" + "log"
    return result, log
