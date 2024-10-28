import threading
from queue import Queue
import os
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

class ThreadedScanner:
    def __init__(self, scanner, max_workers=None):
        self.scanner = scanner
        self.max_workers = max_workers or multiprocessing.cpu_count()
        self.file_queue = Queue()
        self.results_queue = Queue()
        self.stop_event = threading.Event()
    
    def scan_directory(self, directory):
        """多线程扫描目录"""
        # 初始化结果字典
        results = {
            'duplicates': {},
            'garbage': [],
            'classified_files': {k: [] for k in self.scanner.file_types.keys()},
            'large_files': [],
            'old_files': []
        }
        
        # 创建线程池
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交文件搜索任务
            search_future = executor.submit(self._find_files, directory)
            
            # 提交文件处理任务
            process_futures = []
            for _ in range(self.max_workers):
                future = executor.submit(self._process_files)
                process_futures.append(future)
            
            # 等待文件搜索完成
            search_future.result()
            
            # 发送停止信号
            self.stop_event.set()
            
            # 等待所有处理任务完成
            for future in process_futures:
                future.result()
            
            # 收集结果
            while not self.results_queue.empty():
                result_type, result_data = self.results_queue.get()
                if result_type == 'duplicate':
                    file_hash, file_path = result_data
                    if file_hash not in results['duplicates']:
                        results['duplicates'][file_hash] = []
                    results['duplicates'][file_hash].append(file_path)
                else:
                    results[result_type].append(result_data)
        
        return results
    
    def _find_files(self, directory):
        """遍历目录并将文件添加到队列"""
        for root, _, files in os.walk(directory):
            for filename in files:
                if self.stop_event.is_set():
                    return
                file_path = os.path.join(root, filename)
                self.file_queue.put(file_path)
    
    def _process_files(self):
        """处理文件队列中的文件"""
        while not self.stop_event.is_set() or not self.file_queue.empty():
            try:
                file_path = self.file_queue.get_nowait()
            except:
                continue
                
            try:
                # 获取文件哈希值
                file_hash = self.scanner.get_file_hash(file_path)
                self.results_queue.put(('duplicate', (file_hash, file_path)))
                
                # 检查文件类型
                file_extension = os.path.splitext(file_path)[1].lower()
                for category, extensions in self.scanner.file_types.items():
                    if file_extension in extensions:
                        self.results_queue.put(('classified_files', (category, file_path)))
                        break
                
                # 检查文件大小
                file_size = os.path.getsize(file_path)
                if file_size > 100 * 1024 * 1024:  # 100MB
                    self.results_queue.put(('large_files', {'path': file_path, 'size': file_size}))
                
            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")