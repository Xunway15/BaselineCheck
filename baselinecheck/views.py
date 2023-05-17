# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http import FileResponse,HttpResponse
from django.shortcuts import get_list_or_404,get_object_or_404
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
#from check_list import CHECK_LISTS
import os
from . import utils 
from .models import *
import pandas as pd
import json
import re
import datetime

# TODO:
# 唯一性+get_object_or_404
# 导入 
# html 显示不全
# 检测脚本多平台
# 脚本检测内容
# 检测结果格式规范 与后端交互规范
# 检测合格率 检测结果 数据统计 图表形式
# 
# done:
# readme 说明
# 

def getToken(request):
    token=get_token(request)
    return HttpResponse(json.dumps({'token':token}), content_type="application/json,charset=utf-8")

def index(request):
    return render(request, 'baselinecheck/createtask.html', locals())

def create_task(request):
    #前端form提交信息，后端接收并新建任务，最后返回任务是否创建成功（可以有同名任务？）
    if request.method == "POST":
        taskname = request.POST['taskname']
        remark = request.POST['remark']
        server_ip = utils.get_host_ip()
        Tasks.objects.create(name=taskname, remark=remark, serverIp=server_ip)
        result = "创建成功"
    else:
        result = "创建失败"
    return render(request, 'baselinecheck/result.html', locals())

#生成检测脚本：包含serverIP
def generate_checklist(request,taskid):
    if request.method == 'GET':
        server_ip = Tasks.objects.get(id=taskid).serverIp
        addstring = 'ServerIP={}\n'.format(server_ip)+'taskid={}\n'.format(taskid)
        #file_path = os.path.dirname(__file__)
        # if kind == "linux":
        checklist_gen = utils.file_repalce(settings.CHECKLISTS_GEN, settings.LINUX_CHECKLISTT_TEMPLATES, server_ip, taskid, addstring)
        file=open(os.path.join(settings.CHECKLISTS_GEN, checklist_gen), 'rb')
        response =FileResponse(file)
        response['Content-Type']='application/octet-stream'
        response['Content-Disposition']='attachment;filename="{}"'.format(checklist_gen)
        return response
        # except Exception:
        #     raise Http404

def tasklist(request):
    task_list = []
    alltasks = Tasks.objects.all()
    for task in alltasks:
        task_detail = {}
        task_detail['id'] = task.id
        task_detail['name'] = task.name
        task_detail['time'] = task.time
        task_detail['remark'] = task.remark
        task_detail['serverIp'] = task.serverIp
        task_list.append(task_detail)
    return render(request, 'baselinecheck/tasklist.html', locals())

def task(request,taskid):#taskinfo
    #任务信息
    thistask = Tasks.objects.get(id=taskid)
    task_detail = {}
    task_detail['id'] = thistask.id
    task_detail['name'] = thistask.name
    task_detail['time'] = thistask.time
    task_detail['remark'] = thistask.remark
    task_detail['serverIp'] = thistask.serverIp
    #任务主机信息
    host_list = []
    taskhosts = Host_Info.objects.filter(task_id__id=taskid)
    for host in taskhosts:
        hostinfo = {}
        hostinfo['id'] = host.id
        hostinfo['task_id'] = host.task_id.id
        hostinfo['ip'] = host.ip
        hostinfo['macaddr'] = host.macaddr
        hostinfo['netinfo'] = host.netinfo
        hostinfo['osversion'] = host.osversion
        hostinfo['kernelversion'] = host.kernelversion
        hostinfo['time'] = host.time
        host_list.append(hostinfo)
    return render(request, 'baselinecheck/task.html', locals())

def deletetask(request,taskid):
    Tasks.objects.filter(id=taskid).delete()
    return tasklist(request)

def hostinfo(request,taskid,hostid):#主机详情
    #!!get_object_or_404
    # host = Host_Info.objects.get(id=hostid,task_id__id=taskid)
    # Check_result.objects.get(host__id=hostid, task_id__id=taskid)
    host = get_object_or_404(Host_Info, id=hostid, task_id__id=taskid)
    Check_result_obj = get_object_or_404(Check_result, host__id=hostid, task_id__id=taskid)
    check_result = Check_result_obj.check_result.split('$')[1:]
    for i in range(0, len(check_result)):
        if check_result[i] in ['0','1','2','3']:
            check_result[i] = utils.CHECK_RESULTS1[check_result[i]]
    check_info = Check_result_obj.check_info.split('$')[1:]
    
    return render(request, 'baselinecheck/hostinfo.html', locals())

def deletehost(request,taskid,hostid):
    #!!get_list_or_404
    Host_Info.objects.filter(id=hostid, task_id__id=taskid).delete()
    return task(request,taskid)

@csrf_exempt #no csrftoken needed 
def hostupload(request): #主机将结果发送至服务端并记录  taskid,hostip
    #遇到相同ip和taskid时将旧结果删除

    #接收检查结果
    if request.method == "POST":
        f = request.FILES["file"] #<class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
        taskid = f.name.split('_')[-1].split('.')[0]#re.sub('\D','',f.name)
        if not os.path.exists(os.path.join(settings.TASKS_ROOT,taskid)):
            os.makedirs(os.path.join(settings.TASKS_ROOT,taskid))
        if 'HTTP_X_FORWARDED_FOR' in request.META: #if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            hostip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            hostip = request.META['REMOTE_ADDR']
        # print(hostip) 
        #!!!in vmware nat mode,ip is same with serverip 
        Hostpath = os.path.join(settings.TASKS_ROOT,taskid,hostip+'.csv')
        with open(Hostpath,'wb') as fw:
            fw.seek(0)
            fw.truncate()
            for chunk in f.chunks():
                fw.write(chunk)
        result = pd.read_csv(Hostpath, sep='\t',encoding='gb18030', on_bad_lines='skip')#,error_bad_lines=False)
        # result.to_excel( os.path.join(settings.TASKS_ROOT,taskid,hostip+'.xlsx')) #,encoding='gb18030')
    #处理结果
        #如何保存到数据库 / 文件
        #Linuxcheckresult_template.pl pandas.to_pickle/read_pickle
        time = datetime.datetime.strptime(result.iloc[-9,1],'%Y-%m-%d %H:%M:%S')  #!! translate time to standard time format
        task_id = int(result.iloc[-7,1])
        netinfo = result.iloc[-6,1]
        hostname = result.iloc[-5,1]
        macaddr = result.iloc[-4,1]
        #ip = result.iloc[-3,1]
        kernelversion = result.iloc[-2,1]
        osversion = ' '.join(result.tail(1).values[~pd.isnull(result.tail(1).values)])#result.iloc[-1,:].values[~pd.isnull(result.iloc[-1,:].values)]
        result.drop(result.tail(15).index,inplace=True) #!!!删除df结尾其他的信息

        if Tasks.objects.filter(id=task_id).exists():
            thistask = Tasks.objects.get(id=task_id)
            # if not Host_Info.objects.filter(ip=hostip, task_id=thistask).exists():
            #     thishost = Host_Info.objects.create(task_id=thistask,
            #                     ip=hostip,
            #                     time = time,
            #                     netinfo = netinfo,
            #                     hostname = hostname,
            #                     macaddr = macaddr,
            #                     #ip = ip,
            #                     kernelversion = kernelversion,
            #                     osversion = osversion,
            #                     )
            # else:
            #     thishost = Host_Info.objects.get(ip=hostip,task_id=thistask)#!!!可能会返回多个
            Host_Info_default = {'ip':hostip,
                                'time':time,
                                'netinfo':netinfo,
                                'hostname':hostname,
                                'macaddr':macaddr,
                                'kernelversion':kernelversion,
                                'osversion':osversion}
            thishost,created = Host_Info.objects.update_or_create(ip=hostip, task_id=thistask,
                                defaults=Host_Info_default
                                )
            #新建主机检查结果
            
            check_result = "" #result.iloc[:, -3]
            check_info = "" #result.iloc[:, -4]
            for i in range(len(result)):
                check_result+="$"
                check_info+="$" #!! 转义原字符串中的$ \$
                check_result_i = result.iloc[i, -3]
                check_info_i = result.iloc[i, -4]

                if check_result_i in ["FAIL", "TRUE", "MANUAL", "参考子项"]:
                    check_result+=utils.CHECK_RESULTS[check_result_i]
                else:
                    check_result+=check_result_i #'4'
                if pd.isnull(check_info_i):
                    check_info+='NaN'
                else:
                    check_info+=check_info_i
            #!!! baselinecheck.models.Check_result.MultipleObjectsReturned: get() returned more than one Check_result -- it returned 3!
            Check_result_default = { 'check_result': check_result ,'check_info': check_info}
            Check_result.objects.update_or_create(defaults=Check_result_default , task_id=thistask, host=thishost)
            # if not Check_result.objects.filter(task_id=thistask,host=thishost).exists():
            #     Check_result.objects.create(task_id=thistask,host=thishost,check_info=check_info,check_result=check_result)
            # else:
            #     Check_result.objects.update(task_id=thistask,host=thishost,check_info=check_info,check_result=check_result)
            
            return HttpResponse("upload success")
        else:
            return HttpResponse("taskid not found")
    else:
        return HttpResponse("Http menthod should be 'POST'")

def readme(request):

    return render(request, 'baselinecheck/readme.html', locals())
    return HttpResponse(1)
