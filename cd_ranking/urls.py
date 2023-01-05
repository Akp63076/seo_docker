
from django.urls import path
from cd_ranking import views

urlpatterns = [
    path('',views.dashboard1,name="cd_ranking"),    
    path('trend/',views.trend),
    path('export_dash/',views.export_dash),
    path('category/',views.Test.category),
    path('category_tag/<str:frequency>/',views.category_tag_filter),
    path('test/',views.test)

]
