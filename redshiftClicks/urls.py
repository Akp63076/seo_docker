
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.urls import path, include # new

urlpatterns = [
    
    path('clicks/', views.index, name='redshiftClicks-index'),
    path('start/',views.longtask, name='redshiftClicks-longtask'),
    
    path('status/<task_id>/',views.taskstatus, name='redshiftClicks-taskstatus'),
    
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)