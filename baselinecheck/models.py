from django.db import models

# Create your models here.

#to upgrade models in datebase,the steps are below:
#0.conda activate py310
#1.python manage.py makemigrations baselinecheck 
#2.python manage.py migrate

class Tasks(models.Model):
    time = models.DateTimeField(auto_now_add=True,verbose_name="任务创建时间")
    name = models.CharField(max_length=100)
    remark = models.CharField(max_length=100)
    serverIp = models.CharField(max_length=100)

class Checklist(models.Model):  #blank=False,null=False 
    Check_item = models.TextField(verbose_name='检查项')
    CHECK_LEVELS = [
        (1,"可选"),
        (2,"一般"),
        (3,"重要"),
    ]
    Check_level = models.IntegerField(choices=CHECK_LEVELS,default=2,verbose_name='检查项级别')   #1：可选 2：一般 3：重要 
    Check_explanation = models.TextField(verbose_name='检查说明')
    Check_standard = models.TextField(verbose_name="标准值")

class Host_Info(models.Model):
    task_id = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    netinfo = models.TextField()
    ip = models.CharField(max_length=100)#GenericIPAddressField() #protocol='ipv4'
    macaddr = models.CharField(max_length=100)
    osversion = models.CharField(max_length=200)
    kernelversion = models.CharField(max_length=200)
    hostname = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=False, verbose_name='扫描时间')
    #check_result = models.BinaryField()

class Check_result(models.Model):
    task_id = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    host = models.ForeignKey(Host_Info, on_delete=models.CASCADE)
    check_result = models.TextField() # char $ as separator
    check_info = models.TextField() # char $ as separator

    # value = models.TextField(verbose_name='检查情况')
    # CHECK_RESULTS = [
    #     (0,"False"),
    #     (1,"True"),
    #     (2,"Manual"),
    # ]
    # result = models.IntegerField(choices=CHECK_RESULTS,default=2,verbose_name='检查结果')
    # time = models.DateTimeField(auto_now_add=False)
    # Checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)







