"""seoTool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path,re_path
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
#from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('redshiftClicks/', include('redshiftClicks.urls')),
    path('', include('web_analytics.urls')),
    path('coursefinder/', include('coursefinder.urls')),
    path('cd-status/', include('cd_status.urls')),
    path('ranking/', include('ranking.urls')),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name="login"),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name="logout"),
    path("register/",user_views.register,name='register'),
    path("profile/",user_views.profile,name='profile'),
    re_path('', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
    path('cd_ranking/', include('cd_ranking.urls')),
    path('rank_tool/', include('rank_tool.urls')),

    path('cd_notification/', include("cd_notification.urls")),

]
