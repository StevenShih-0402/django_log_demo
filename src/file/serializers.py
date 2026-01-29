# /src/file/serializers.py
# 負責驗證上傳的 ZIP 檔案。

from rest_framework.serializers import Serializer, FileField, ValidationError

class UploadSerializer(Serializer):
    """
    處理 ZIP 檔案上傳驗證的序列化器。
    """
    file = FileField(help_text="請上傳 ZIP 格式的壓縮檔")

    def validate_file(self, value):
        """
        驗證檔案是否為 zip 格式。
        """
        if not value.name.endswith('.zip'):
            raise ValidationError("僅支援 ZIP 格式檔案。")
        return value