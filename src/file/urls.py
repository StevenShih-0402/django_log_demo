# /src/file/urls.py
# 定義 file 應用程式的內部路由。

from django.urls import path
from .views import FileUploadView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
]
