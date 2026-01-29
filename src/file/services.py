# /src/file/services.py
# 負責處理 ZIP 檔案解壓與檔案分類存儲的業務邏輯。

import os
import zipfile
import io
import logging
from abc import ABC, abstractmethod
from django.conf import settings

# 初始化 Loggers
logger = logging.getLogger('app.system')
audit_logger = logging.getLogger('audit')

class StorageStrategy(ABC):
    """
    檔案存儲策略的抽象基底類別。
    """
    @abstractmethod
    def get_storage_path(self, filename: str) -> str:
        """
        根據檔名返回目標存儲路徑。
        """
        pass

class JpgStorageStrategy(StorageStrategy):
    """
    處理 JPG 檔案的存儲策略。
    """
    def get_storage_path(self, filename: str) -> str:
        return os.path.join(settings.MEDIA_ROOT, 'jpg', filename)

class PdfStorageStrategy(StorageStrategy):
    """
    處理 PDF 檔案的存儲策略。
    """
    def get_storage_path(self, filename: str) -> str:
        return os.path.join(settings.MEDIA_ROOT, 'pdf', filename)

class PngStorageStrategy(StorageStrategy):
    """
    處理 PNG 檔案的存儲策略。
    """
    def get_storage_path(self, filename: str) -> str:
        return os.path.join(settings.MEDIA_ROOT, 'png', filename)

class DefaultStorageStrategy(StorageStrategy):
    """
    處理其他未知類型檔案的預設存儲策略。
    """
    def get_storage_path(self, filename: str) -> str:
        return os.path.join(settings.MEDIA_ROOT, 'others', filename)

class FileProcessingService:
    """
    協調 ZIP 解壓與策略選取的服務類別。
    """
    
    _strategies = {
        '.jpg': JpgStorageStrategy(),
        '.jpeg': JpgStorageStrategy(),
        '.pdf': PdfStorageStrategy(),
        '.png': PngStorageStrategy(),
    }

    @staticmethod
    def process_zip(zip_file) -> None:
        """
        解析 ZIP 檔案並根據副檔名分發至對應存儲路徑。
        """
        logger.info(f"開始處理 ZIP 檔案: {zip_file.name}")
        
        with zipfile.ZipFile(zip_file, 'r') as zf:
            for file_info in zf.infolist():
                if file_info.is_dir():
                    continue
                
                filename = os.path.basename(file_info.filename)
                _, ext = os.path.splitext(filename.lower())
                
                strategy = FileProcessingService._strategies.get(ext, DefaultStorageStrategy())
                target_path = strategy.get_storage_path(filename)
                
                logger.debug(f"檔案 {filename} 副檔名為 {ext}，選取策略: {strategy.__class__.__name__}")
                
                # 確保目錄存在並寫入檔案
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                with zf.open(file_info) as source, open(target_path, 'wb') as target:
                    target.write(source.read())
                
                audit_logger.info(f"檔案已儲存至: {target_path}")

        logger.info(f"ZIP 檔案處理完成: {zip_file.name}")
