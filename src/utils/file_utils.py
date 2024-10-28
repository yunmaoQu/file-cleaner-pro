import os
import shutil
import hashlib
import magic
import logging
from typing import List, Dict, Any
from datetime import datetime
import zipfile

class FileUtils:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    @staticmethod
    def get_file_hash(file_path: str, block_size: int = 65536) -> str:
        """计算文件的MD5哈希值"""
        hasher = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for block in iter(lambda: f.read(block_size), b''):
                    hasher.update(block)
            return hasher.hexdigest()
        except Exception as e:
            raise IOError(f"Failed to calculate hash for {file_path}: {str(e)}")
            
    @staticmethod
    def get_file_type(file_path: str) -> str:
        """获取文件MIME类型"""
        try:
            return magic.from_file(file_path, mime=True)
        except Exception:
            return "application/octet-stream"
            
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """获取文件详细信息"""
        stats = os.stat(file_path)
        return {
            'path': file_path,
            'size': stats.st_size,
            'created': datetime.fromtimestamp(stats.st_ctime),
            'modified': datetime.fromtimestamp(stats.st_mtime),
            'accessed': datetime.fromtimestamp(stats.st_atime),
            'type': FileUtils.get_file_type(file_path),
            'extension': os.path.splitext(file_path)[1].lower()
        }
        
    @staticmethod
    def create_zip_file(source_path: str, output_path: str) -> bool:
        """创建ZIP压缩文件"""
        try:
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                if os.path.isfile(source_path):
                    zf.write(source_path, os.path.basename(source_path))
                else:
                    for root, _, files in os.walk(source_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, source_path)
                            zf.write(file_path, arcname)
            return True
        except Exception as e:
            raise IOError(f"Failed to create zip file: {str(e)}")
            
    @staticmethod
    def extract_zip_file(zip_path: str, extract_path: str) -> bool:
        """解压ZIP文件"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(extract_path)
            return True
        except Exception as e:
            raise IOError(f"Failed to extract zip file: {str(e)}")
            
    @staticmethod
    def safe_delete(file_path: str) -> bool:
        """安全删除文件"""
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            return True
        except Exception as e:
            raise IOError(f"Failed to delete {file_path}: {str(e)}")
            
    @staticmethod
    def safe_move(source: str, destination: str) -> bool:
        """安全移动文件"""
        try:
            shutil.move(source, destination)
            return True
        except Exception as e:
            raise IOError(f"Failed to move file: {str(e)}")
            
    @staticmethod
    def safe_copy(source: str, destination: str) -> bool:
        """安全复制文件"""
        try:
            if os.path.isfile(source):
                shutil.copy2(source, destination)
            else:
                shutil.copytree(source, destination)
            return True
        except Exception as e:
            raise IOError(f"Failed to copy file: {str(e)}")