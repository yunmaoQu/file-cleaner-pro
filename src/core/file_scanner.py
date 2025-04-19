import os
import hashlib
from datetime import datetime
import filetype  # 用于文件类型检测

class FileScanner:
    def __init__(self, ai_models):
        self.ai_models = ai_models
        self.file_types = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
            'documents': ['.doc', '.docx', '.pdf', '.txt', '.xlsx'],
            'videos': ['.mp4', '.avi', '.mkv', '.mov'],
            'audio': ['.mp3', '.wav', '.flac'],
            'archives': ['.zip', '.rar', '.7z']
        }
        
    def get_file_hash(self, file_path):
        """计算文件的MD5哈希值"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def scan_directory(self, directory):
        """扫描目录并返回文件分析结果"""
        results = {
            'duplicates': {},
            'garbage': [],
            'classified_files': {k: [] for k in self.file_types.keys()},
            'large_files': [],
            'old_files': []
        }
        
        hash_dict = {}
        
        for root, _, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                try:
                    # 获取文件基本信息
                    file_size = os.path.getsize(file_path)
                    file_extension = os.path.splitext(filename)[1].lower()
                    kind = filetype.guess(file_path)
                    if kind is not None:
                        file_type = kind.mime
                    else:
                        file_type = "unknown"
                    
                    # 分类文件
                    self.classify_file(file_path, file_extension, results)
                    
                    # 检查大文件
                    if file_size > 100 * 1024 * 1024:  # 大于100MB
                        results['large_files'].append({
                            'path': file_path,
                            'size': file_size
                        })
                    
                    # 检查旧文件
                    mtime = os.path.getmtime(file_path)
                    if (datetime.now() - datetime.fromtimestamp(mtime)).days > 180:  # 超过180天
                        results['old_files'].append({
                            'path': file_path,
                            'last_modified': datetime.fromtimestamp(mtime)
                        })
                    
                    # 检查重复文件
                    file_hash = self.get_file_hash(file_path)
                    if file_hash in hash_dict:
                        if file_hash not in results['duplicates']:
                            results['duplicates'][file_hash] = [hash_dict[file_hash]]
                        results['duplicates'][file_hash].append(file_path)
                    else:
                        hash_dict[file_hash] = file_path
                        
                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")
                    
        return results
    
    def classify_file(self, file_path, extension, results):
        """将文件分类到相应类别"""
        for category, extensions in self.file_types.items():
            if extension in extensions:
                results['classified_files'][category].append(file_path)
                break