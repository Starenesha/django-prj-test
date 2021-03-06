"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from meter.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MetersList, name='list_meters'),
    path('create/', CreateMeter.as_view(), name='create_meter'),
    path('<str:slug>/',MeterDetail.as_view(), name='meter_detail'),
    path('<str:slug>/delete/',MeterDelete.as_view(),name='meter_delete'),
    path('<str:slug>/delete-data/',meter_delete_data, name='meter_delete_data'),

]
