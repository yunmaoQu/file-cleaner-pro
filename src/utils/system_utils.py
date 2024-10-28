import os
import sys
import platform
import psutil
import logging
from typing import Dict, Any
import json
from datetime import datetime

class SystemUtils:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """获取系统信息"""
        try:
            info = {
                'platform': platform.system(),
                'platform_release': platform.release(),
                'platform_version': platform.version(),
                'architecture': platform.machine(),
                'processor': platform.processor(),
                'ram': psutil.virtual_memory().total,
                'python_version': sys.version,
            }
            return info
        except Exception as e:
            logging.error(f"Failed to get system info: {str(e)}")
            return {}
            
    @staticmethod
    def get_disk_usage(path: str = None) -> Dict[str, Any]:
        """获取磁盘使用情况"""
        try:
            if path is None:
                path = os.path.abspath(os.sep)  # 根目录
                
            usage = psutil.disk_usage(path)
            return {
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent
            }
        except Exception as e:
            logging.error(f"Failed to get disk usage: {str(e)}")
            return {}
            
    @staticmethod
    def get_memory_usage() -> Dict[str, Any]:
        """获取内存使用情况"""
        try:
            memory = psutil.virtual_memory()
            return {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'percent': memory.percent
            }
        except Exception as e:
            logging.error(f"Failed to get memory usage: {str(e)}")
            return {}
            
    @staticmethod
    def get_cpu_usage() -> float:
        """获取CPU使用率"""
        try:
            return psutil.cpu_percent(interval=1)
        except Exception as e:
            logging.error(f"Failed to get CPU usage: {str(e)}")
            return 0.0
            
    @staticmethod
    def is_admin() -> bool:
        """检查是否具有管理员权限"""
        try:
            if platform.system() == 'Windows':
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except Exception:
            return False
            
    @staticmethod
    def get_process_info() -> Dict[str, Any]:
        """获取当前进程信息"""
        try:
            process = psutil.Process()
            return {
                'pid': process.pid,
                'memory_usage': process.memory_info().rss,
                'cpu_percent': process.cpu_percent(),
                'threads': process.num_threads(),
                'start_time': datetime.fromtimestamp(process.create_time()).isoformat()
            }
        except Exception as e:
            logging.error(f"Failed to get process info: {str(e)}")
            return {}
            
    def monitor_system_resources(self, interval: int = 60) -> None:
        """监控系统资源使用情况"""
        try:
            while True:
                resources = {
                    'timestamp': datetime.now().isoformat(),
                    'cpu_usage': self.get_cpu_usage(),
                    'memory_usage': self.get_memory_usage(),
                    'disk_usage': self.get_disk_usage(),
                    'process_info': self.get_process_info()
                }
                
                # 记录资源使用情况
                self.logger.info(f"System resources: {json.dumps(resources)}")
                
                # 检查资源使用是否超过阈值
                if resources['cpu_usage'] > 90:
                    self.logger.warning("High CPU usage detected")
                if resources['memory_usage']['percent'] > 90:
                    self.logger.warning("High memory usage detected")
                if resources['disk_usage']['percent'] > 90:
                    self.logger.warning("High disk usage detected")
                    
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.logger.info("System monitoring stopped")
        except Exception as e:
            self.logger.error(f"System monitoring failed: {str(e)}")
            
    @staticmethod
    def clean_system_temp() -> bool:
        """清理系统临时文件"""
        try:
            temp_dirs = []
            if platform.system() == 'Windows':
                temp_dirs = [os.environ.get('TEMP'), os.environ.get('TMP')]
            else:
                temp_dirs = ['/tmp']
                
            for temp_dir in temp_dirs:
                if temp_dir and os.path.exists(temp_dir):
                    for item in os.listdir(temp_dir):
                        item_path = os.path.join(temp_dir, item)
                        try:
                            if os.path.isfile(item_path):
                                os.remove(item_path)
                            elif os.path.isdir(item_path):
                                shutil.rmtree(item_path)
                        except Exception as e:
                            logging.warning(f"Failed to remove {item_path}: {str(e)}")
                            
            return True
            
        except Exception as e:
            logging.error(f"Failed to clean system temp: {str(e)}")
            return False