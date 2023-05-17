# -*- coding: UTF-8 -*-
import os

import pandas as pd
def readcsv(filename):
    #filename = 'checkList.csv' 
    return pd.read_csv(filename, sep='\t',encoding='gb18030',error_bad_lines=False)#encoding='unicode_escape'
    df.to_excel("output.xlsx",encoding='gb18030')

import json
CHECK_RESULTS = {
    "FAIL":'0',
    "TRUE":'1',
    "MANUAL":'2',
    "参考子项":'3',
    #'4':其他数据
}
CHECK_RESULTS1 = {
    '0':"FAIL",
    '1':"TRUE",
    '2':"MANUAL",
   '3':"参考子项",
    #'4':其他数据
}


import socket
def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
        return ip

import fileinput
def file_repalce(CHECKLISTS_GEN, CHECKLIST_Template, ServerIP, taskid, addstring ):
    # with fileinput.FileInput(CHECKLISTS_GEN, inplace=True) as file: #, openhook=fileinput.hook_encoded('utf-8', '')
    #     for i, line in enumerate(file):
    #         if i == 0:
    #             print('ServerIP={}'.format(ServerIP), end='')
    #         else:
    #             print(line, end='')

    checklist_gen = 'checklist_{}_{}.sh'.format(ServerIP,taskid)
    with open( CHECKLIST_Template, 'r', encoding="utf-8") as fr:
        with open( os.path.join(CHECKLISTS_GEN, checklist_gen), 'w', encoding="utf-8", newline='\n') as fw:
            fw.seek(0)
            fw.truncate()
            fw.write(addstring)
            # fw.write('ServerIP={}\n'.format(ServerIP))
            # fw.write('taskid={}\n'.format())
            for i, line in enumerate(fr):
                fw.write(line)
    return checklist_gen

def handle_uploaded_file(f):
    return
    with open("some/file/name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)