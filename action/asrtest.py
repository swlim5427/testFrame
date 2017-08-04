# coding=utf-8
import commonfunc
import time
import os
import threading
import codecs


class AsrTest(object):

    def __init__(self, message, test_case, test_id, data, test_tools):

        self.message = message
        self.case_id = message["caseId"]
        self.url = message["url"]
        self.version = message["version"]

        try:
            self.count = self.message["count"]
        except KeyError:
            self.count = 1

        self.test_case = test_case
        self.data = data
        self.test_id = test_id
        self.test_tools = test_tools

        self.case_list = self.test_case["caselist"]
        self.answer_list = self.test_case["answer"]
        self.decoder_config = self.data["config"]

        self.run_time = commonfunc.public_methods.get_date_time(1, 0)
        self.test_result_file = ""
        self.test_result_file_gbk = ""
        # self.asrResult = self.testPath+self.caseId+"-"+self.testId+"/result/",self.runTime
        # self.asrLog = self.testPath+"log/"+self.runTime+".log"

        self.do_test()

        commonfunc.check_test.check_test(self.message, self.test_id, self.test_result_file)

    def do_test(self):

        pwd = os.getcwd()
        test_folder = self.version+"-" + self.case_id+"-" + self.test_id
        test_path = self.data["config"].split("decoder.conf")[0]
        answer_path = self.test_case["answer"].split("answer.list")[0]

        result_path, log_path = commonfunc.public_methods.mkdir(test_path, test_folder)

        case_path = test_path + test_folder
        os.chdir(pwd)

        if self.url != "":
            commonfunc.public_methods.download(self.url, case_path + "/" + self.test_tools)

        os.chdir(case_path)

        os.system('chmod +x '+self.test_tools)
        asr_log = str(result_path) + "/" + str(self.count) + ".log"
        asr_result = str(result_path) + "/" + str(self.count)

        print asr_log
        print asr_result
        print self.case_id, "do test----", self.test_id, "-----", threading.current_thread().getName()

        os.system("./" +
                  str(self.test_tools) +
                  " --config " + str(self.decoder_config) +
                  " --filelist " + str(self.case_list) +
                  " --log " + str(asr_result) +
                  " --sleep 2 >>" + asr_log)

        os.chdir(answer_path)

        os.system("python pasr_calc_recrate.py "
                  "-s sclite "
                  "-m answer.list "
                  "-r "+str(asr_result) +
                  " -o "+str(asr_result)+"rate")

        test_result = open(str(asr_result)+"rate")

        lines = []
        erase = False
        for line in test_result:
            if line.strip() == "Real time(s):":
                erase = True
            if not erase:
                lines.append(line)
            if line.strip() == "W-------------------------------------------------------":
                erase = False
            if line.strip() == "========================================================":
                erase = True

        test_result.close()

        self.test_result_file = str(asr_result)+"rate_result.txt"
        open(self.test_result_file, 'w').writelines(lines)

        asr_rt = codecs.open(asr_log, 'r', 'utf-8')
        rt = ",rt:"
        global wrt

        for line in reversed(asr_rt.readlines()):
            if rt in line:
                r_line = line.split(rt)[1]
                wrt = "R T : "+r_line
                asr_rt.close()

        test_result_rt = codecs.open(str(self.test_result_file), 'r+', 'utf-8')
        read_test_result = test_result_rt.read()
        test_result_rt.seek(0)
        try:
            test_result_rt.write('\n')
            test_result_rt.write(wrt+'\n')
            test_result_rt.write(read_test_result)
            test_result_rt.close()
        except Exception as e:
            print e
            print "testError"

        self.test_result_file_gbk = str(asr_result)+"rate_result_gbk.txt"

        os.system("iconv -f utf-8 -t gbk "+self.test_result_file+" >"+self.test_result_file_gbk)

        os.chdir(pwd)
        time.sleep(1)
