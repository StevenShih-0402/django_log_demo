# /src/file/tests.py
# 驗證 ZIP 檔案上傳後是否能依副檔名正確解壓至對應目錄。

import io
import zipfile
import os
import shutil
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

class FileUploadTests(TestCase):
    """
    處理檔案上傳與解壓邏輯的測試類別。
    """

    def setUp(self):
        """
        在每個測試開始前，確保測試用的 media 目錄是乾淨的。
        """
        if os.path.exists(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)
        os.makedirs(settings.MEDIA_ROOT)

    def tearDown(self):
        """
        在每個測試結束後，清理測試用的 media 目錄。
        """
        if os.path.exists(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)

    def test_zip_extraction_by_extension(self):
        """
        模擬上傳包含 jpg, pdf, png 的 ZIP 檔並驗證其解壓路徑。
        本測試預期會因為 API 端點 /api/upload/ 尚未定義而失敗。
        """
        # 1. 建立一個記憶體內的 ZIP 檔案
        zip_buffer = io.BytesIO()
        files_to_zip = {
            'test.jpg': b'fake jpg content',
            'test.pdf': b'fake pdf content',
            'test.png': b'fake png content',
        }
        
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zf:
            for filename, content in files_to_zip.items():
                zf.writestr(filename, content)

        zip_file = SimpleUploadedFile(
            "test.zip",
            zip_buffer.getvalue(),
            content_type="application/zip"
        )

        # 2. 調用 API 端點 /api/upload/
        upload_url = "/api/upload/"
        response = self.client.post(upload_url, {'file': zip_file}, format='multipart')

        # 3. 斷言檢查成果 (預期此處會因為 404 而失敗)
        self.assertEqual(response.status_code, 201)

        # 驗證檔案是否按副檔名儲存在對應子目錄
        for ext in ['jpg', 'pdf', 'png']:
            expected_path = os.path.join(settings.MEDIA_ROOT, ext, f'test.{ext}')
            self.assertTrue(os.path.exists(expected_path), f"找不到檔案：media/{ext}/test.{ext}")
