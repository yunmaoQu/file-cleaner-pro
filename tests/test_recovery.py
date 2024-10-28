import unittest
import os
import tempfile
from src.core.recovery import FileRecovery

class TestRecovery(unittest.TestCase):
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.backup_dir = tempfile.mkdtemp()
        self.recovery = FileRecovery(self.backup_dir)
        
        # 创建测试文件
        self.test_file_path = os.path.join(self.test_dir, 'test.txt')
        with open(self.test_file_path, 'w') as f:
            f.write('test content')
            
    # tests/test_recovery.py 续：
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.backup_dir)
        
    def test_backup_before_delete(self):
        """测试删除前备份功能"""
        # 执行备份
        backup_path = self.recovery.backup_before_delete(self.test_file_path)
        
        self.assertIsNotNone(backup_path)
        self.assertTrue(os.path.exists(backup_path))
        
        # 验证备份内容
        with open(backup_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, 'test content')
        
    def test_recover_file(self):
        """测试文件恢复功能"""
        # 先备份后删除
        backup_path = self.recovery.backup_before_delete(self.test_file_path)
        os.remove(self.test_file_path)
        
        # 恢复文件
        restored_path = self.recovery.recover_file(self.test_file_path)
        
        self.assertTrue(os.path.exists(restored_path))
        with open(restored_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, 'test content')
        
    def test_list_recoverable_files(self):
        """测试可恢复文件列表功能"""
        # 创建多个备份
        files = []
        for i in range(3):
            path = os.path.join(self.test_dir, f'test{i}.txt')
            with open(path, 'w') as f:
                f.write(f'content {i}')
            self.recovery.backup_before_delete(path)
            files.append(path)
            
        recoverable = self.recovery.list_recoverable_files()
        
        self.assertEqual(len(recoverable), 3)
        self.assertTrue(all(f['original_path'] in files for f in recoverable))
        
    def test_cleanup_old_backups(self):
        """测试清理旧备份功能"""
        # 创建备份
        backup_path = self.recovery.backup_before_delete(self.test_file_path)
        
        # 修改备份时间为31天前
        backup_time = os.path.getctime(backup_path)
        os.utime(backup_path, (backup_time - 31*24*3600, backup_time - 31*24*3600))
        
        # 清理旧备份
        deleted_count = self.recovery.cleanup_old_backups(days=30)
        
        self.assertEqual(deleted_count, 1)
        self.assertFalse(os.path.exists(backup_path))

if __name__ == '__main__':
    unittest.main()