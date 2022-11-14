
from django.urls import path
from dashboard import views

urlpatterns = [
    path('',views.dashboard1,name="dashboard"),    
    path('trend/',views.trend),
    path('export_dash/',views.export_dash)
]
