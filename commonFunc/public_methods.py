import threading
import sqlite3

def sqliteConnect(sql):
    conn = sqlite3.connect('test.db')
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

def checkSql():
    creatTableSql = "create table testFrame (id text,caseId text,nextId text);"
    insertCheckTableSql = "insert into testFrame VALUES (100000,\"\",\"\")"

    sqlList=[creatTableSql,insertCheckTableSql]
    return sqlList

def correspondence(caseId,nextId):
    logicList = [caseId,nextId]


def checkTable():
    countSql = "select count(*) from testFrame"
    countRes = sqliteConnect([countSql,0])
    return countRes

def initTable():
    dSql = "delete from testFrame"
    sqliteConnect([dSql,1])