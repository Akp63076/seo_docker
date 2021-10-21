from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.urls import path, include  # new

urlpatterns = [
    path("form/", views.index, name="coursefinder-index"),

    path("levelbins/7lq2x/", views.levellist, name="coursefinder-levellist"),
    path("streams", views.streamlist, name="coursefinder-streamlist"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
