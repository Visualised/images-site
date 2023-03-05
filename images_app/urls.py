from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.UploadFile.as_view(), name="images-app-upload"),
    path("list/", views.ListFile.as_view(), name="images-app-list"),
]