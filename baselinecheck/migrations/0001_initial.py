# Generated by Django 4.0 on 2023-04-22 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Check_item', models.TextField(verbose_name='检查项')),
                ('Check_level', models.IntegerField(choices=[(1, '可选'), (2, '一般'), (3, '重要')], default=2, verbose_name='检查项级别')),
                ('Check_explanation', models.TextField(verbose_name='检查说明')),
                ('Check_standard', models.TextField(verbose_name='标准值')),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='任务创建时间')),
                ('name', models.CharField(max_length=100)),
                ('remark', models.CharField(max_length=100)),
                ('serverIp', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Host_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('macaddr', models.CharField(max_length=20)),
                ('osversion', models.CharField(max_length=50)),
                ('kernelversion', models.CharField(max_length=50)),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baselinecheck.tasks')),
            ],
        ),
        migrations.CreateModel(
            name='Check_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('value', models.TextField(verbose_name='检查情况')),
                ('result', models.IntegerField(choices=[(0, 'False'), (1, 'True'), (2, 'Manual')], default=2, verbose_name='检查结果')),
                ('Checklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baselinecheck.checklist')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baselinecheck.host_info')),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baselinecheck.tasks')),
            ],
        ),
    ]
