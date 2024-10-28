import unittest
import os
import tempfile
from datetime import datetime
from src.core.backup import AutoBackup

class TestBackup(unittest.TestCase):
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.backup_dir = tempfile.mkdtemp()
        self.backup = AutoBackup(self.backup_dir)
        
        # 创建测试文件
        self.create_test_files()
        
    def tearDown(self):
        """测试后清理"""
        self.backup.stop_auto_backup()
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.backup_dir)
        
    def create_test_files(self):
        """创建测试文件"""
        self.test_files = []
        for i in range(3):
            path = os.path.join(self.test_dir, f'test{i}.txt')
            with open(path, 'w') as f:
                f.write(f'content {i}')
            self.test_files.append(path)
            
    def test_create_backup(self):
        """测试创建备份功能"""
        backup_info = self.backup.create_backup(self.test_files)
        
        self.assertIsNotNone(backup_info)
        self.assertTrue(os.path.exists(backup_info['path']))
        self.assertEqual(backup_info['files_count'], 3)
        
    def test_restore_backup(self):
        """测试恢复备份功能"""
        # 创建备份
        backup_info = self.backup.create_backup(self.test_files)
        
        # 删除原始文件
        for file in self.test_files:
            os.remove(file)
            
        # 恢复备份
        restore_path = tempfile.mkdtemp()
        result = self.backup.restore_backup(backup_info['name'], restore_path)
        
        self.assertTrue(result)
        self.assertTrue(all(os.path.exists(
            os.path.join(restore_path, os.path.basename(f)))
            for f in self.test_files
        ))
        
    def test_verify_backup(self):
        """测试验证备份功能"""
        backup_info = self.backup.create_backup(self.test_files)
        
        verification = self.backup.verify_backup(backup_info['name'])
        
        self.assertEqual(verification['status'], 'verified')
        self.assertEqual(verification['files_checked'], 3)
        self.assertEqual(len(verification['errors']), 0)
        
    def test_auto_backup(self):
        """测试自动备份功能"""
        # 启动自动备份
        self.backup.start_auto_backup(self.test_files)
        
        # 等待一个备份周期
        import time
        time.sleep(2)
        
        # 检查是否创建了备份
        backups = self.backup.get_backup_info()
        self.assertGreater(len(backups['backups']), 0)
        
    def test_cleanup_old_backups(self):
        """测试清理旧备份功能"""
        # 创建备份
        backup_info = self.backup.create_backup(self.test_files)
        
        # 修改备份时间为31天前
        backup_path = Path(backup_info['path'])
        backup_time = backup_path.stat().st_ctime
        os.utime(str(backup_path), (backup_time - 31*24*3600, backup_time - 31*24*3600))
        
        # 清理旧备份
        removed_count = self.backup.cleanup_old_backups()
        
        self.assertEqual(removed_count, 1)
        self.assertFalse(backup_path.exists())

if __name__ == '__main__':
    unittest.main()