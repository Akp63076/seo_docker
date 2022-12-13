
from django.urls import path
from cd_ranking import views

urlpatterns = [
    path('',views.dashboard1,name="cd_ranking"),    
    path('trend/',views.trend),
    path('export_dash/',views.export_dash)
]
