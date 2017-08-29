# -*- coding: utf-8 -*-

import wave
import contextlib
import math
import sys
import xml.dom.minidom


def get_file(file_path):

    line_dict = []

    try:
        ref_file = open(file_path, "rw")
        lines = ref_file.readlines()
        for line in lines:
            line = line.strip('\n')
            line_dict.append(line)

    except:
        print "no ref_file,check path"

    for i in range(len(line_dict)):
        read_ref(line_dict[i])


def get_wav_time(name):

    try:
        with contextlib.closing(wave.open(name, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return int(math.floor(duration*1000))
    except:
        print '找不到文件' + name
        return 1

def read_ref(ref_file):
    ref_file.replace("\n", "")
    # ref_file = "/Users/swlim/Desktop/pachira_work/toxml/t_list.ref"

    try:
        ref_file_open = open(ref_file)

    except:

        print '找不到文件' + ref_file
        return

    for line in ref_file_open:
        line_n = line.strip().split(" ")
        n = len(line_n)
        line_n_2 = line_n[n-1].split("	")
        voice_name = line_n[0] + " " + line_n_2[0]
        voice_answer = line_n_2[1]
        voice_time = get_wav_time(voice_name)

        if voice_time != 1:
            voice_answer_s, voice_time_s = split_name_time(voice_answer, voice_time)

            write_xml(voice_time, voice_name, voice_answer_s, voice_time_s)


def split_name_time(answer, voice_time):

    answer_dict = []
    voice_answer_s = ""

    len_answer = len(answer)/3

    for i in range(len_answer):

        i *= 3
        k = i + 3

        voice_answer = answer[i:k]+" "
        answer_dict.append(voice_answer)

    time_s = voice_time/len_answer
    answer_f = ""
    time_f = ""
    voice_time_start = 0
    voice_time_end = time_s
    voice_time_s = ""

    time_dict = []

    for i in range(len_answer):

        voice_time_d = str(voice_time_start) + "," + str(voice_time_end) + " "
        time_dict.append(voice_time_d)

        voice_time_start += time_s
        voice_time_end += time_s

    for i in range(len(answer_dict)):
        answer_f = answer_f + answer_dict[i]
        time_f = time_f + time_dict[i]
        voice_answer_s = answer_f
        voice_time_s = time_f

    return voice_answer_s, voice_time_s


def write_xml(voice_time, voice_name, voice_answer_s, voice_time_s):

    doc = xml.dom.minidom.Document()
    node_root = doc.createElement('RecognizeResult')

    doc.appendChild(node_root)

    node_speech = doc.createElement('Speech')
    node_speech.setAttribute('Uri', voice_name)
    node_speech.setAttribute('Duration', str(voice_time))

    node_root.appendChild(node_speech)

    node_result_code = doc.createElement('ResultCode')
    node_result_code.appendChild(doc.createTextNode("0"))

    node_confidence = doc.createElement('Confidence')
    node_confidence.appendChild(doc.createTextNode("100"))

    node_subject = doc.createElement('Subject')
    node_subject.setAttribute('Name', "RecognizeText")

    node_role = doc.createElement('Role')
    node_role.setAttribute('Name', "R0")

    node_end_point = doc.createElement('EndPoint')
    node_end_point.setAttribute('Count', "1")

    node_item = doc.createElement('Item')
    node_item.setAttribute('Begin', "0")
    node_item.setAttribute('End', str(voice_time))

    note_text = doc.createElement('Text')
    note_text.appendChild(doc.createTextNode(voice_answer_s))

    note_time = doc.createElement('Time')
    note_time.appendChild(doc.createTextNode(str(voice_time_s)))

    node_item.appendChild(note_text)
    node_item.appendChild(note_time)

    node_end_point.appendChild(node_item)
    node_role.appendChild(node_end_point)
    node_subject.appendChild(node_role)
    node_speech.appendChild(node_result_code)
    node_speech.appendChild(node_confidence)
    node_speech.appendChild(node_subject)

    fp = open('/Users/swlim/Desktop/pachira_work/toxml/' + str(voice_time) + ".xml", 'w')
    doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
    print str(voice_time) + ".xml"


if __name__ == '__main__':

    try:
        file_path = sys.argv[1]
        # file_path = "/Users/swlim/python/testFrame/filelist"
        file_list = get_file(file_path)

    except Exception as e:
        print e
        print "\nno file input"
        print "input file like:"
        print "python toXml /home/test/filename\n"
