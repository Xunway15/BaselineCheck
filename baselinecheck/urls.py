from django.urls import path
from . import views
from django.conf import settings

app_name = "baselinecheck"
urlpatterns = [
    path('', views.index, name='index'),
    path('generate_checklist/<int:taskid>',views.generate_checklist, name='generate_checklist'),
    path('create_task/',views.create_task, name='create_task'),
    path('tasklist/',views.tasklist, name='tasklist'),
    path('task/<int:taskid>',views.task, name='task'),
    path('deletetask/<int:taskid>',views.deletetask, name='deletetask'),
    path('hostinfo/<int:taskid>/<int:hostid>',views.hostinfo, name='hostinfo'),
    path('deletehost/<int:taskid>/<int:hostid>',views.deletehost, name='deletehost'),
    path('hostupload/', views.hostupload, name='hostupload'),

    path('readme/', views.readme, name='readme'),
    path('gettoken/', views.getToken, name='gettoken'),
]


