import os
import shutil
import json
from datetime import datetime

class FileRecovery:
    def __init__(self, backup_dir="./backup"):
        self.backup_dir = backup_dir
        self.recovery_log = os.path.join(backup_dir, "recovery_log.json")
        self.deleted_files = {}
        self.load_recovery_log()
    
    def load_recovery_log(self):
        """加载恢复日志"""
        if os.path.exists(self.recovery_log):
            with open(self.recovery_log, 'r') as f:
                self.deleted_files = json.load(f)
    
    def save_recovery_log(self):
        """保存恢复日志"""
        os.makedirs(self.backup_dir, exist_ok=True)
        with open(self.recovery_log, 'w') as f:
            json.dump(self.deleted_files, f)
    
    def backup_before_delete(self, file_path):
        """删除前备份文件"""
        if not os.path.exists(file_path):
            return None
            
        # 创建备份文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{os.path.basename(file_path)}_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        # 创建备份目录
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # 复制文件到备份目录
        shutil.copy2(file_path, backup_path)
        
        # 记录删除信息
        self.deleted_files[file_path] = {
            'backup_path': backup_path,
            'timestamp': timestamp,
            'original_path': file_path
        }
        self.save_recovery_log()
        
        return backup_path
    
    def recover_file(self, original_path):
        """恢复已删除的文件"""
        if original_path not in self.deleted_files:
            raise FileNotFoundError("No backup found for this file")
        
        backup_info = self.deleted_files[original_path]
        backup_path = backup_info['backup_path']
        
        if not os.path.exists(backup_path):
            raise FileNotFoundError("Backup file not found")
        
        # 确保目标目录存在
        os.makedirs(os.path.dirname(original_path), exist_ok=True)
        
        # 恢复文件
        shutil.copy2(backup_path, original_path)
        
        # 删除备份记录
        del self.deleted_files[original_path]
        self.save_recovery_log()
        
        return original_path
    
    def list_recoverable_files(self):
        """列出可恢复的文件"""
        return [
            {
                'original_path': path,
                'backup_path': info['backup_path'],
                'timestamp': info['timestamp']
            }
            for path, info in self.deleted_files.items()
        ]
    
    def cleanup_old_backups(self, days=30):
        """清理旧的备份文件"""
        current_time = datetime.now()
        deleted_count = 0
        
        for path, info in list(self.deleted_files.items()):
            backup_time = datetime.strptime(info['timestamp'], '%Y%m%d_%H%M%S')
            if (current_time - backup_time).days > days:
                backup_path = info['backup_path']
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                del self.deleted_files[path]
                deleted_count += 1
        
        self.save_recovery_log()
        return deleted_count