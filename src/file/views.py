# /src/file/views.py
# 負責處理檔案上傳的 API 請求與回應。

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UploadSerializer
from .services import FileProcessingService

class FileUploadView(APIView):
    """
    提供 ZIP 檔案上傳與自動解壓功能的 View。
    """
    
    def post(self, request, *args, **kwargs):
        """
        處理 POST 請求，驗證 ZIP 檔案後調用服務進行解壓。
        """
        serializer = UploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            try:
                FileProcessingService.process_zip(uploaded_file)
                return Response(
                    {"message": "檔案上傳並解壓成功"}, 
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"error": f"處理 ZIP 檔案時發生錯誤: {str(e)}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
