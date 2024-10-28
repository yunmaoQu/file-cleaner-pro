# config/settings.py

import os
import multiprocessing
from pathlib import Path

# 基础路径配置
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
MODELS_DIR = DATA_DIR / 'models'
BACKUP_DIR = DATA_DIR / 'backups'
LOGS_DIR = DATA_DIR / 'logs'
TEMP_DIR = DATA_DIR / 'temp'

# 确保必要的目录存在
for directory in [DATA_DIR, MODELS_DIR, BACKUP_DIR, LOGS_DIR, TEMP_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# 应用配置
APP_CONFIG = {
    'name': 'File Cleaner',
    'version': '1.0.0',
    'author': 'Your Name',
    'debug': True,
}

# 文件类型配置
FILE_TYPES = {
    'images': {
        'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.ico'],
        'mime_types': ['image/'],
        'max_size': 10 * 1024 * 1024,  # 10MB
        'optimize_formats': ['webp', 'jpg']
    },
    'documents': {
        'extensions': ['.doc', '.docx', '.pdf', '.txt', '.xlsx', '.ppt', '.pptx', '.odt'],
        'mime_types': ['application/pdf', 'application/msword', 'text/'],
        'max_size': 50 * 1024 * 1024,  # 50MB
        'archive_after_days': 180
    },
    'videos': {
        'extensions': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
        'mime_types': ['video/'],
        'max_size': 1024 * 1024 * 1024,  # 1GB
        'compress_threshold': 100 * 1024 * 1024  # 100MB
    },
    'audio': {
        'extensions': ['.mp3', '.wav', '.flac', '.m4a', '.ogg', '.aac'],
        'mime_types': ['audio/'],
        'max_size': 100 * 1024 * 1024  # 100MB
    },
    'archives': {
        'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
        'mime_types': ['application/zip', 'application/x-rar', 'application/x-7z-compressed'],
        'max_size': 2 * 1024 * 1024 * 1024  # 2GB
    },
    'code': {
        'extensions': ['.py', '.java', '.cpp', '.h', '.js', '.html', '.css', '.php'],
        'mime_types': ['text/'],
        'backup_frequency': 'daily'
    }
}

# 扫描配置
SCAN_CONFIG = {
    'max_workers': multiprocessing.cpu_count(),
    'chunk_size': 1024 * 1024,  # 1MB
    'ignore_patterns': [
        '.*',  # 隐藏文件
        '~$*',  # 临时文件
        'Thumbs.db',
        '.DS_Store',
        '*.tmp',
        '*.temp'
    ],
    'min_file_size': 1024,  # 1KB
    'max_file_size': 10 * 1024 * 1024 * 1024,  # 10GB
    'follow_symlinks': False,
    'scan_system_files': False,
}

# AI模型配置
AI_CONFIG = {
    'models': {
        'importance': {
            'path': MODELS_DIR / 'importance_model.h5',
            'input_size': 10,
            'threshold': 0.7
        },
        'duplicate': {
            'path': MODELS_DIR / 'duplicate_model.h5',
            'input_size': 224,
            'similarity_threshold': 0.95
        }
    },
    'batch_size': 32,
    'use_gpu': True,
    'memory_limit': 1024 * 1024 * 1024,  # 1GB
}

# 备份配置
BACKUP_CONFIG = {
    'enabled': True,
    'compression': True,
    'compression_level': 6,
    'encryption': False,
    'encryption_key': None,
    'max_backups': 5,
    'backup_interval': 24 * 60 * 60,  # 24小时
    'retention_period': 30 * 24 * 60 * 60,  # 30天
    'min_free_space': 10 * 1024 * 1024 * 1024,  # 10GB
    'exclude_patterns': [
        '*.tmp',
        '*.temp',
        'node_modules',
        'venv',
        '__pycache__'
    ]
}

# 优化配置
OPTIMIZATION_CONFIG = {
    'image': {
        'max_dimension': 1920,
        'quality_levels': {
            'high': 85,
            'medium': 60,
            'low': 40
        },
        'convert_to_webp': True,
        'strip_metadata': True
    },
    'video': {
        'max_resolution': '1080p',
        'target_bitrate': '2M',
        'audio_bitrate': '128k',
        'codec': 'h264'
    },
    'document': {
        'compress_pdf': True,
        'max_pdf_quality': 150,
        'convert_doc_to_pdf': True
    }
}

# GUI配置
GUI_CONFIG = {
    'theme': 'default',
    'window_size': '1024x768',
    'min_window_size': '800x600',
    'max_recent_files': 10,
    'auto_refresh': True,
    'refresh_interval': 5000,  # 5秒
    'show_tooltips': True,
    'confirm_deletions': True,
    'show_hidden_files': False
}

# 性能配置
PERFORMANCE_CONFIG = {
    'max_memory_usage': 0.75,  # 最大内存使用率
    'max_cpu_usage': 0.9,  # 最大CPU使用率
    'io_buffer_size': 8192,  # 8KB
    'cache_size': 100 * 1024 * 1024,  # 100MB
    'temp_cleanup_interval': 3600,  # 1小时
    'max_open_files': 1000
}

# 安全配置
SECURITY_CONFIG = {
    'require_confirmation': True,
    'backup_before_delete': True,
    'secure_delete': False,  # 安全删除（多次覆写）
    'max_file_size_no_confirm': 100 * 1024 * 1024,  # 100MB
    'restricted_paths': [
        '/System',
        '/Windows',
        '/Program Files'
    ]
}

# 错误处理配置
ERROR_CONFIG = {
    'max_retries': 3,
    'retry_delay': 1,  # 秒
    'ignore_errors': False,
    'error_notification': True,
    'log_errors': True
}

# 开发模式配置
if APP_CONFIG['debug']:
    SCAN_CONFIG['max_workers'] = 2
    AI_CONFIG['use_gpu'] = False
    BACKUP_CONFIG['backup_interval'] = 5 * 60  # 5分钟
    BACKUP_CONFIG['retention_period'] = 24 * 60 * 60  # 1天
    GUI_CONFIG['refresh_interval'] = 1000  # 1秒
    ERROR_CONFIG['ignore_errors'] = True
    
    # 添加测试目录
    TEST_DIR = DATA_DIR / 'test'
    TEST_DIR.mkdir(exist_ok=True)
    
    # 测试数据配置
    TEST_CONFIG = {
        'sample_files': TEST_DIR / 'samples',
        'test_backups': TEST_DIR / 'backups',
        'test_results': TEST_DIR / 'results'
    }
    
    # 确保测试目录存在
    for dir_path in TEST_CONFIG.values():
        dir_path.mkdir(exist_ok=True)

# 环境变量覆盖
def load_env_config():
    """从环境变量加载配置"""
    import os
    
    # 应用配置
    APP_CONFIG['debug'] = os.getenv('APP_DEBUG', APP_CONFIG['debug'])
    
    # 扫描配置
    if 'SCAN_MAX_WORKERS' in os.environ:
        SCAN_CONFIG['max_workers'] = int(os.getenv('SCAN_MAX_WORKERS'))
    
    # AI配置
    if 'AI_USE_GPU' in os.environ:
        AI_CONFIG['use_gpu'] = os.getenv('AI_USE_GPU').lower() == 'true'
    
    # 备份配置
    if 'BACKUP_ENABLED' in os.environ:
        BACKUP_CONFIG['enabled'] = os.getenv('BACKUP_ENABLED').lower() == 'true'
    
    if 'BACKUP_ENCRYPTION_KEY' in os.environ:
        BACKUP_CONFIG['encryption'] = True
        BACKUP_CONFIG['encryption_key'] = os.getenv('BACKUP_ENCRYPTION_KEY')

# 加载自定义配置文件
def load_custom_config():
    """从自定义配置文件加载配置"""
    custom_config_path = BASE_DIR / 'custom_config.py'
    if custom_config_path.exists():
        try:
            with open(custom_config_path) as f:
                exec(f.read(), globals())
            print("Loaded custom configuration")
        except Exception as e:
            print(f"Error loading custom configuration: {e}")

# 验证配置
def validate_config():
    """验证配置的有效性"""
    # 验证路径配置
    required_dirs = [DATA_DIR, MODELS_DIR, BACKUP_DIR, LOGS_DIR]
    for dir_path in required_dirs:
        if not dir_path.exists():
            raise ValueError(f"Required directory does not exist: {dir_path}")
    
    # 验证AI模型配置
    if AI_CONFIG['use_gpu']:
        try:
            import tensorflow as tf
            if not tf.test.is_gpu_available():
                print("Warning: GPU is enabled but not available, falling back to CPU")
                AI_CONFIG['use_gpu'] = False
        except ImportError:
            print("Warning: TensorFlow not installed, GPU support disabled")
            AI_CONFIG['use_gpu'] = False
    
    # 验证备份配置
    if BACKUP_CONFIG['encryption'] and not BACKUP_CONFIG['encryption_key']:
        raise ValueError("Encryption is enabled but no encryption key provided")
    
    # 验证性能配置
    if PERFORMANCE_CONFIG['max_memory_usage'] > 0.9:
        print("Warning: High memory usage limit may cause system instability")
    
    # 验证文件类型配置
    for file_type, config in FILE_TYPES.items():
        if 'extensions' not in config:
            raise ValueError(f"Missing extensions for file type: {file_type}")
        if 'mime_types' not in config:
            raise ValueError(f"Missing mime types for file type: {file_type}")

# 初始化配置
def init_config():
    """初始化配置"""
    # 加载环境变量配置
    load_env_config()
    
    # 加载自定义配置
    load_custom_config()
    
    # 验证配置
    validate_config()
    
    # 创建必要的目录
    for directory in [DATA_DIR, MODELS_DIR, BACKUP_DIR, LOGS_DIR, TEMP_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    
    # 设置日志目录权限
    try:
        LOGS_DIR.chmod(0o755)
    except Exception as e:
        print(f"Warning: Failed to set log directory permissions: {e}")
    
    # 清理临时目录
    try:
        import shutil
        shutil.rmtree(TEMP_DIR)
        TEMP_DIR.mkdir()
    except Exception as e:
        print(f"Warning: Failed to clean temporary directory: {e}")
    
    return {
        'app_config': APP_CONFIG,
        'scan_config': SCAN_CONFIG,
        'ai_config': AI_CONFIG,
        'backup_config': BACKUP_CONFIG,
        'optimization_config': OPTIMIZATION_CONFIG,
        'gui_config': GUI_CONFIG,
        'performance_config': PERFORMANCE_CONFIG,
        'security_config': SECURITY_CONFIG,
        'error_config': ERROR_CONFIG,
        'file_types': FILE_TYPES
    }

# 导出配置
CONFIG = init_config()

# 配置是否已初始化的标志
CONFIG_INITIALIZED = True

def get_config():
    """获取当前配置"""
    if not CONFIG_INITIALIZED:
        raise RuntimeError("Configuration not initialized")
    return CONFIG

def update_config(new_config):
    """更新配置"""
    global CONFIG
    CONFIG.update(new_config)
    validate_config()
    return CONFIG

# 如果是直接运行此文件，打印配置信息
if __name__ == '__main__':
    import json
    
    def config_to_dict(config):
        """转换配置为可序列化的字典"""
        result = {}
        for key, value in config.items():
            if isinstance(value, Path):
                result[key] = str(value)
            elif isinstance(value, dict):
                result[key] = config_to_dict(value)
            else:
                result[key] = value
        return result
    
    # 打印当前配置
    print(json.dumps(config_to_dict(CONFIG), indent=2))