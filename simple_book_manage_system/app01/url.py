#!/usr/bin/env python
'''

'''
import os
import sys

path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append( path )



from django.conf.urls import url,include
from django.contrib import admin
from app01 import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^author', views.Author),
    url(r'^publisher',views.Publisher),
    url(r'^book',views.Book),
    url(r'test',views.test)
]