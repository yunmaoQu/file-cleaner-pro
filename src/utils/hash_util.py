import hashlib
import xxhash
from typing import Union, BinaryIO
import logging

class HashUtils:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    @staticmethod
    def calculate_md5(data: Union[str, bytes, BinaryIO]) -> str:
        """计算MD5哈希值"""
        hasher = hashlib.md5()
        
        try:
            if isinstance(data, str):
                hasher.update(data.encode())
            elif isinstance(data, bytes):
                hasher.update(data)
            else:  # 文件对象
                for chunk in iter(lambda: data.read(65536), b''):
                    hasher.update(chunk)
                    
            return hasher.hexdigest()
        except Exception as e:
            raise ValueError(f"Failed to calculate MD5: {str(e)}")
            
    @staticmethod
    def calculate_sha256(data: Union[str, bytes, BinaryIO]) -> str:
        """计算SHA256哈希值"""
        hasher = hashlib.sha256()
        
        try:
            # src/utils/hash_utils.py 续：
            if isinstance(data, str):
                hasher.update(data.encode())
            elif isinstance(data, bytes):
                hasher.update(data)
            else:  # 文件对象
                for chunk in iter(lambda: data.read(65536), b''):
                    hasher.update(chunk)
                    
            return hasher.hexdigest()
        except Exception as e:
            raise ValueError(f"Failed to calculate SHA256: {str(e)}")
            
    @staticmethod
    def calculate_xxhash(data: Union[str, bytes, BinaryIO]) -> str:
        """计算xxHash值（更快的哈希算法）"""
        hasher = xxhash.xxh64()
        
        try:
            if isinstance(data, str):
                hasher.update(data.encode())
            elif isinstance(data, bytes):
                hasher.update(data)
            else:  # 文件对象
                for chunk in iter(lambda: data.read(65536), b''):
                    hasher.update(chunk)
                    
            return hasher.hexdigest()
        except Exception as e:
            raise ValueError(f"Failed to calculate xxHash: {str(e)}")
            
    @classmethod
    def get_file_hash(cls, file_path: str, algorithm: str = 'md5') -> str:
        """获取文件的哈希值"""
        try:
            with open(file_path, 'rb') as f:
                if algorithm.lower() == 'md5':
                    return cls.calculate_md5(f)
                elif algorithm.lower() == 'sha256':
                    return cls.calculate_sha256(f)
                elif algorithm.lower() == 'xxhash':
                    return cls.calculate_xxhash(f)
                else:
                    raise ValueError(f"Unsupported hash algorithm: {algorithm}")
        except Exception as e:
            raise IOError(f"Failed to calculate file hash: {str(e)}")