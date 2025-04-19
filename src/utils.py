import os
import logging
import logging.config
from datetime import datetime
import hashlib
import filetype

def setup_logging(config):
    """设置日志系统"""
    logging.config.dictConfig(config)
    return logging.getLogger(__name__)

def get_file_hash(file_path, block_size=65536):
    """计算文件哈希值"""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            hasher.update(block)
    return hasher.hexdigest()

def format_size(size):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def get_file_age(file_path):
    """获取文件年龄（天）"""
    mtime = os.path.getmtime(file_path)
    age = (datetime.now() - datetime.fromtimestamp(mtime)).days
    return age

def is_system_file(file_path):
    """检查是否为系统文件"""
    system_patterns = [
        'System Volume Information',
        '$Recycle.Bin',
        'pagefile.sys',
        'hiberfil.sys',
        'swapfile.sys'
    ]
    return any(pattern in file_path for pattern in system_patterns)

def create_backup_filename(file_path):
    """创建备份文件名"""
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    name, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return os.path.join(directory, f"{name}_backup_{timestamp}{ext}")

def safe_remove(file_path):
    """安全删除文件"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        logging.error(f"Error removing file {file_path}: {str(e)}")
        return False

def get_mime_type(file_path):
    """获取文件MIME类型"""
    kind = filetype.guess(file_path)
    if kind is not None:
        return kind.mime
    else:
        return "unknown"