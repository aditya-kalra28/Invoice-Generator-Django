
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from invoiceApp import views


urlpatterns = [
    path('',views.index,name="index")
]
