import io
import zipfile
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import os


class FileUploadTests(TestCase):
    def setUp(self):
        self.upload_url = reverse('file-upload-list')  # 假設使用 ViewSet

    def test_upload_zip_and_unpack(self):
        # 1. 建立一個記憶體內的 ZIP 檔案
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('test_file.txt', 'Hello World')
            zf.writestr('folder/inner.txt', 'Deep file')

        zip_file = SimpleUploadedFile(
            "test.zip",
            zip_buffer.getvalue(),
            content_type="application/zip"
        )

        # 2. 發送 POST 請求
        response = self.client.post(self.upload_url, {'file': zip_file}, format='multipart')

        # 3. 驗證結果
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'Unpacked successfully')

        # 驗證檔案是否真的存在於 media
        expected_path = os.path.join(settings.MEDIA_ROOT, 'unpacked', 'test_file.txt')
        self.assertTrue(os.path.exists(expected_path))
