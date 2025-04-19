import os
import shutil
import threading
import schedule
import time
from datetime import datetime
import json
from pathlib import Path
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any

from src.config.settings import BACKUP_CONFIG
from src.utils.file_utils import FileUtils
from src.utils.system_utils import SystemUtils

class AutoBackup:
    def __init__(self, backup_dir: str):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.backup_log_file = self.backup_dir / "backup_log.json"
        self.backup_thread = None
        self.stop_flag = threading.Event()
        self.backup_history = self._load_backup_history()
        self.logger = logging.getLogger(__name__)

    def _load_backup_history(self) -> Dict:
        """加载备份历史记录"""
        if self.backup_log_file.exists():
            try:
                with open(self.backup_log_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {'backups': []}
        return {'backups': []}

    def _save_backup_history(self):
        """保存备份历史记录"""
        with open(self.backup_log_file, 'w') as f:
            json.dump(self.backup_history, f, indent=4)

    def create_backup(self, source_paths: List[str], backup_name: str = None) -> Dict[str, Any]:
        """创建备份"""
        try:
            # 生成备份名称
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = backup_name or f"backup_{timestamp}"
            backup_path = self.backup_dir / backup_name

            # 创建备份目录
            backup_path.mkdir(exist_ok=True)

            # 收集要备份的文件
            files_to_backup = []
            total_size = 0
            for source_path in source_paths:
                source_path = Path(source_path)
                if source_path.is_file():
                    files_to_backup.append(source_path)
                    total_size += source_path.stat().st_size
                elif source_path.is_dir():
                    for file_path in source_path.rglob('*'):
                        if file_path.is_file():
                            files_to_backup.append(file_path)
                            total_size += file_path.stat().st_size

            # 检查备份大小限制
            if total_size > BACKUP_CONFIG['max_backup_size']:
                raise ValueError("Total backup size exceeds limit")

            # 使用线程池复制文件
            with ThreadPoolExecutor(max_workers=BACKUP_CONFIG.get('max_workers', 4)) as executor:
                for file_path in files_to_backup:
                    relative_path = file_path.relative_to(file_path.parent)
                    dest_path = backup_path / relative_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    executor.submit(shutil.copy2, str(file_path), str(dest_path))

            # 如果启用压缩
            if BACKUP_CONFIG['compression']:
                zip_path = str(backup_path) + '.zip'
                FileUtils.create_zip_file(str(backup_path), zip_path)
                shutil.rmtree(str(backup_path))
                backup_path = Path(zip_path)

            # 记录备份信息
            backup_info = {
                'name': backup_name,
                'timestamp': timestamp,
                'size': FileUtils.get_file_info(str(backup_path))['size'],
                'files_count': len(files_to_backup),
                'compressed': BACKUP_CONFIG['compression'],
                'path': str(backup_path),
                'system_info': SystemUtils.get_system_info()
            }
            
            self.backup_history['backups'].append(backup_info)
            self._save_backup_history()
            
            self.logger.info(f"Backup created successfully: {backup_name}")
            return backup_info

        except Exception as e:
            self.logger.error(f"Backup creation failed: {str(e)}")
            raise

    def start_auto_backup(self, source_paths: List[str]):
        """启动自动备份"""
        def backup_job():
            if not self.stop_flag.is_set():
                try:
                    self.create_backup(source_paths)
                except Exception as e:
                    self.logger.error(f"Auto backup failed: {str(e)}")

        def run_schedule():
            while not self.stop_flag.is_set():
                schedule.run_pending()
                time.sleep(60)

        # 确保停止旧的备份任务
        self.stop_auto_backup()
        
        # 重置停止标志
        self.stop_flag.clear()
        
        # 设置定时任务
        interval_hours = BACKUP_CONFIG['backup_interval'] // 3600
        schedule.every(interval_hours).hours.do(backup_job)

        # 启动备份线程
        self.backup_thread = threading.Thread(
            target=run_schedule, 
            name="backup_scheduler",
            daemon=True
        )
        self.backup_thread.start()
        self.logger.info("Auto backup started")

    def stop_auto_backup(self):
        """停止自动备份"""
        if not self.backup_thread or not self.backup_thread.is_alive():
            self.logger.info("No active backup thread to stop")
            return
            
        self.logger.info(f"Stopping auto backup thread: {self.backup_thread.name}...")
        self.stop_flag.set()
        
        # 给线程一个合理的时间来终止
        try:
            self.logger.info("Waiting for backup thread to terminate...")
            self.backup_thread.join(timeout=2.0)  # 等待最多2秒
            if self.backup_thread.is_alive():
                self.logger.warning(f"Backup thread {self.backup_thread.name} did not terminate gracefully")
                print(f"WARNING: Backup thread {self.backup_thread.name} is still alive after timeout")
            else:
                self.logger.info("Backup thread terminated successfully")
        except Exception as e:
            self.logger.error(f"Error while stopping backup thread: {e}")
            print(f"Error stopping backup thread: {e}")
            
        # 清除所有定时任务
        self.logger.info("Clearing scheduled tasks...")
        schedule.clear()
        self.logger.info("Auto backup stopped")

    def restore_backup(self, backup_name: str, restore_path: str) -> bool:
        """从备份恢复文件"""
        try:
            # 查找备份信息
            backup_info = next(
                (b for b in self.backup_history['backups'] if b['name'] == backup_name),
                None
            )
            if not backup_info:
                raise ValueError(f"Backup not found: {backup_name}")

            backup_path = Path(backup_info['path'])
            restore_path = Path(restore_path)

            if not backup_path.exists():
                raise FileNotFoundError(f"Backup file not found: {backup_path}")

            # 创建恢复目录
            restore_path.mkdir(parents=True, exist_ok=True)

            # 如果是压缩备份
            if backup_info['compressed']:
                shutil.unpack_archive(str(backup_path), str(restore_path))
            else:
                # 复制所有文件
                with ThreadPoolExecutor(max_workers=BACKUP_CONFIG.get('max_workers', 4)) as executor:
                    for src in backup_path.rglob('*'):
                        if src.is_file():
                            relative_path = src.relative_to(backup_path)
                            dest = restore_path / relative_path
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            executor.submit(shutil.copy2, str(src), str(dest))

            self.logger.info(f"Backup restored successfully: {backup_name}")
            return True

        except Exception as e:
            self.logger.error(f"Restore failed: {str(e)}")
            return False

    def cleanup_old_backups(self):
        """清理旧的备份"""
        try:
            current_time = datetime.now()
            keep_days = BACKUP_CONFIG['keep_backups']
            
            # 打印调试信息
            self.logger.debug(f"Cleaning up backups older than {keep_days} days")
            self.logger.debug(f"Current time: {current_time}")
            
            # 筛选需要删除的备份
            backups_to_remove = []
            remaining_backups = []
            
            for backup in self.backup_history['backups']:
                backup_time = datetime.strptime(backup['timestamp'], '%Y%m%d_%H%M%S')
                delta_days = (current_time - backup_time).days
                
                self.logger.debug(f"Backup: {backup['name']}, Date: {backup_time}, Age: {delta_days} days")
                
                if delta_days > keep_days:
                    self.logger.debug(f"Marking for removal: {backup['name']}")
                    backups_to_remove.append(backup)
                else:
                    remaining_backups.append(backup)
            
            # 删除旧备份
            for backup in backups_to_remove:
                backup_path = Path(backup['path'])
                self.logger.debug(f"Removing backup: {backup_path}")
                
                if backup_path.exists():
                    if backup_path.is_dir():
                        shutil.rmtree(str(backup_path))
                    else:
                        backup_path.unlink()
            
            # 更新备份历史
            self.backup_history['backups'] = remaining_backups
            self._save_backup_history()
            
            self.logger.info(f"Removed {len(backups_to_remove)} old backups")
            return len(backups_to_remove)
            
        except Exception as e:
            self.logger.error(f"Cleanup failed: {str(e)}")
            return 0

    def get_backup_info(self, backup_name: str = None) -> Dict:
        """获取备份信息"""
        if backup_name:
            backup = next(
                (b for b in self.backup_history['backups'] if b['name'] == backup_name),
                None
            )
            return backup if backup else {}
        return self.backup_history

    def verify_backup(self, backup_name: str) -> Dict[str, Any]:
        """验证备份完整性"""
        try:
            backup_info = self.get_backup_info(backup_name)
            if not backup_info:
                raise ValueError(f"Backup not found: {backup_name}")

            backup_path = Path(backup_info['path'])
            if not backup_path.exists():
                raise FileNotFoundError(f"Backup file not found: {backup_path}")

            verification_result = {
                'name': backup_name,
                'status': 'verified',
                'errors': [],
                'files_checked': 0,
                'total_size': 0
            }

            if backup_info['compressed']:
                # 验证压缩文件完整性
                import zipfile
                try:
                    with zipfile.ZipFile(str(backup_path)) as zf:
                        bad_files = zf.testzip()
                        if bad_files:
                            verification_result['errors'].append(f"Corrupted files found: {bad_files}")
                            verification_result['status'] = 'corrupted'
                        verification_result['files_checked'] = len(zf.namelist())
                        verification_result['total_size'] = sum(info.file_size for info in zf.filelist)
                except Exception as e:
                    verification_result['errors'].append(f"Zip file verification failed: {str(e)}")
                    verification_result['status'] = 'failed'
            else:
                # 验证普通备份文件
                for file_path in backup_path.rglob('*'):
                    if file_path.is_file():
                        try:
                            verification_result['files_checked'] += 1
                            verification_result['total_size'] += file_path.stat().st_size
                        except Exception as e:
                            verification_result['errors'].append(f"File verification failed: {file_path} - {str(e)}")
                            verification_result['status'] = 'corrupted'

            return verification_result

        except Exception as e:
            self.logger.error(f"Backup verification failed: {str(e)}")
            return {
                'name': backup_name,
                'status': 'failed',
                'errors': [str(e)],
                'files_checked': 0,
                'total_size': 0
            }