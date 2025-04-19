import unittest
import os
import shutil
import tempfile
from src.core.file_scanner import FileScanner
from src.core.threaded_scanner import ThreadedScanner

# 创建一个AI模型的模拟对象
class MockAIModels:
    def __init__(self):
        self.importance_model = None
        self.duplicate_model = None
        
    def predict_importance(self, file_info):
        return 0.5  # 返回一个固定的重要性得分
        
    def predict_duplicates(self, file1, file2):
        return 0.8  # 返回一个固定的相似度得分

class TestScanner(unittest.TestCase):
    def setUp(self):
        """测试前创建临时测试目录和文件"""
        self.test_dir = tempfile.mkdtemp()
        self.ai_models = MockAIModels()
        self.scanner = FileScanner(self.ai_models)
        self.threaded_scanner = ThreadedScanner(self.scanner)
        
        # 创建测试文件
        self.create_test_files()
        
    def tearDown(self):
        """测试后清理临时文件"""
        shutil.rmtree(self.test_dir)
        
    def create_test_files(self):
        """创建测试文件"""
        # 创建普通文件
        with open(os.path.join(self.test_dir, 'test1.txt'), 'w') as f:
            f.write('test content 1')
        with open(os.path.join(self.test_dir, 'test2.txt'), 'w') as f:
            f.write('test content 2')
            
        # 创建重复文件
        with open(os.path.join(self.test_dir, 'duplicate1.txt'), 'w') as f:
            f.write('duplicate content')
        with open(os.path.join(self.test_dir, 'duplicate2.txt'), 'w') as f:
            f.write('duplicate content')
            
        # 创建大文件
        with open(os.path.join(self.test_dir, 'large_file.dat'), 'wb') as f:
            f.write(b'0' * 1024 * 1024)  # 1MB
            
    def test_scan_directory(self):
        """测试目录扫描功能"""
        results = self.scanner.scan_directory(self.test_dir)
        
        self.assertIn('duplicates', results)
        self.assertIn('large_files', results)
        self.assertIn('classified_files', results)
        
        # 验证重复文件检测
        duplicate_count = sum(len(files) for files in results['duplicates'].values())
        self.assertEqual(duplicate_count, 2)
        
        # 验证大文件检测
        self.assertEqual(len(results['large_files']), 1)
        
    def test_threaded_scan(self):
        """测试多线程扫描功能"""
        results = self.threaded_scanner.scan_directory(self.test_dir)
        
        self.assertIn('duplicates', results)
        self.assertIn('large_files', results)
        self.assertIn('classified_files', results)
        
    def test_file_classification(self):
        """测试文件分类功能"""
        results = self.scanner.scan_directory(self.test_dir)
        
        # 验证文本文件分类
        self.assertIn('documents', results['classified_files'])
        txt_files = results['classified_files']['documents']
        self.assertTrue(any(f.endswith('.txt') for f in txt_files))
        
    def test_error_handling(self):
        """测试错误处理"""
        # 测试不存在的目录
        with self.assertRaises(FileNotFoundError):
            self.scanner.scan_directory('/nonexistent/directory')
            
        # 测试无权限目录
        if os.name != 'nt':  # Unix系统
            no_access_dir = os.path.join(self.test_dir, 'no_access')
            os.mkdir(no_access_dir)
            os.chmod(no_access_dir, 0o000)
            
            results = self.scanner.scan_directory(no_access_dir)
            self.assertIn('errors', results)
            
if __name__ == '__main__':
    unittest.main()