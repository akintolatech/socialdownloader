from django.urls import path
from .views import download_video, home

urlpatterns = [
    path("", home, name="home"),
    path("download/", download_video, name="download_video"),
]
