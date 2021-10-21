
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.urls import path, include # new

urlpatterns = [
    path('', views.homepage, name='web_analytics-homepage'),
    path('analytics/', views.index, name='web_analytics-index'),
    path('keyword-planner/', views.kwplanner, name='web_analytics-kwplanner'),
    path('getFile/', views.getfile, name='web_analytics-getfile'),

    
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)