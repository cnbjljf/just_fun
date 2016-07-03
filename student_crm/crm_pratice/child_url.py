#!/usr/bin/env python
'''

'''
import os
import sys

path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )
from django.conf.urls import url,include
from django.contrib import admin
from crm_pratice import views

urlpatterns = [
    url(r'^$',views.dashboard),
    url(r'customer$',views.customer),
    url(r'customer/new$',views.add_new_customer),
    url(r'^customer/(\d+)/$',views.detail_per_customer),
    url(r'^classes/new$',views.add_new_class),
    url(r'^classes$',views.classes),
    url(r'^classes/(\d+)/$',views.detail_per_class),
    url(r'^teachers$',views.teacher),
    url(r'^teachers/new$',views.add_new_teacher),
    url(r'^student_grade',views.stu_grade),
    url(r'^student_grade/new$',views.add_new_StuRec),
    url(r'^student_grade/(\d+)/$',views.detail_per_StuRec),
]
