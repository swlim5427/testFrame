# coding=utf-8
import xlrd
import json
from action import *
import public_methods
import logging


class TestFrameDistribute():

    def __init__(self, message):

        self.message = message
        tp_sql = "select path from testPath;"

        for test_path in public_methods.sqlite_connect([tp_sql, 0]):
            table_path = test_path[0]
            print table_path

        self.table_name = table_path+"/testcase/"+message["tableName"]
        self.case_id = message["caseId"]
        self.run_times = message["times"]
        # self.version = message["version"]
        # self.url = message["url"]

        self.haveNext = 0

        self.get_testcase()

    def get_testcase(self):

        test_table = xlrd.open_workbook(self.table_name)
        self.test_table_sheet = test_table.sheets()[0]

        self.rowNum = self.test_table_sheet.nrows

        for i in range(self.rowNum):
            if self.test_table_sheet.cell(i, 0).value == self.case_id:

                t_value = self.test_table_sheet.cell(i, 2).value
                self.test_case = json.loads(t_value)

                d_value = self.test_table_sheet.cell(i, 3).value
                self.data = json.loads(d_value)
                self.test_tools = self.test_table_sheet.cell(i, 4).value
                next_id = self.test_table_sheet.cell(i, 5).value

        next_case_id = public_methods.get_next_caseid(next_id)

        try:
            self.run_id = self.message["id"]

        except:

            select_sql = "select id from testFrame ORDER BY id DESC limit 0,1"

            for test_id in public_methods.sqlite_connect([select_sql, 0]):
                self.test_id = test_id

            now_case_id = self.case_id
            left_case_id = next_case_id

            ''' 记录本次测试初始参数 '''
            insert_sql = "insert into testFrame VALUES (" \
                   "\""+str(int(test_id[0])+1)+"\",\""+str(self.case_id)+"\",\""+str(next_case_id)+"\",\""+str(0)+"\",\""+str(self.run_times)+"\",\""+str(now_case_id)+"\",\""+str(left_case_id)+"\");"
            public_methods.sqlite_connect([insert_sql, 0])

        self.test_distribute()

    def test_distribute(self):

        case_type = self.case_id.split('_')[0]

        ''' 判断测试类型 '''

        if case_type == "asr":

            try:
                run_id = self.message["id"]
                logging.info(run_id, "distribute test")

            except KeyError:

                run_id = int(self.test_id[0])+1

                update_sql = "update testFrame SET count = "+"\""+str(1)+"\" where id ="+str(run_id)+";"
                public_methods.sqlite_connect([update_sql, 1])

            asrtest.AsrTest(self.message, self.test_case, str(run_id), self.data, self.test_tools)
