"""rank_tool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.rank_tool, name='rank_tool')
Class-based views
    1. Add an import:  from other_app.views import rank_tool
    2. Add a URL to urlpatterns:  path('', rank_tool.as_view(), name='rank_tool')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from . import views
from django.views.static import serve 
#from django.conf.urls import url
from django.conf import settings

urlpatterns = [
    
    path('',views.index,name='rank_tool-index'),
    path('queue',views.queue,name='rank_tool-queue'),
    path('instructions',views.instructions,name='rank_tool-instructions'),
    re_path(r'^uploads/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
	

]
