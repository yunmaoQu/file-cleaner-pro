import tkinter as tk
from tkinter import ttk, filedialog
import logging
from typing import Callable

class ScanPanel:
    def __init__(self, parent, scanner):
        self.logger = logging.getLogger(__name__)
        self.scanner = scanner
        self.frame = ttk.LabelFrame(parent, text="Scan", padding="5")
        self.create_widgets()
        
    def create_widgets(self):
        """创建面板组件"""
        # 路径选择
        path_frame = ttk.Frame(self.frame)
        path_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var)
        self.path_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5)
        
        self.browse_btn = ttk.Button(path_frame, text="Browse",
                                   command=self.browse_directory)
        self.browse_btn.grid(row=0, column=1, padx=5)
        
        # 扫描选项
        options_frame = ttk.LabelFrame(self.frame, text="Scan Options", padding="5")
        options_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.scan_duplicates = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Find Duplicates",
                       variable=self.scan_duplicates).grid(row=0, column=0)
        
        self# src/gui/scan_panel.py 续：
        self.scan_large_files = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Find Large Files",
                       variable=self.scan_large_files).grid(row=0, column=1)
        
        self.scan_old_files = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Find Old Files",
                       variable=self.scan_old_files).grid(row=0, column=2)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.frame, 
                                          variable=self.progress_var,
                                          maximum=100)
        self.progress_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # 扫描按钮
        self.scan_btn = ttk.Button(self.frame, text="Start Scan",
                                 command=self.start_scan)
        self.scan_btn.grid(row=3, column=0, pady=5)
        
        # 状态标签
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(self.frame, textvariable=self.status_var)
        self.status_label.grid(row=4, column=0, pady=5)
        
    def browse_directory(self):
        """选择要扫描的目录"""
        directory = filedialog.askdirectory()
        if directory:
            self.path_var.set(directory)
            
    def start_scan(self):
        """开始扫描"""
        directory = self.path_var.get()
        if not directory:
            tk.messagebox.showerror("Error", "Please select a directory first")
            return
            
        try:
            self.scan_btn.config(state='disabled')
            self.status_var.set("Scanning...")
            self.progress_var.set(0)
            
            # 获取扫描选项
            options = {
                'scan_duplicates': self.scan_duplicates.get(),
                'scan_large_files': self.scan_large_files.get(),
                'scan_old_files': self.scan_old_files.get()
            }
            
            # 开始扫描
            def progress_callback(progress: float):
                self.progress_var.set(progress)
                self.frame.update_idletasks()
            
            results = self.scanner.scan_directory(directory, options, progress_callback)
            
            # 更新UI显示结果
            self.status_var.set("Scan completed")
            self.progress_var.set(100)
            
            # 发送结果到其他面板
            self.notify_results(results)
            
        except Exception as e:
            self.logger.error(f"Scan failed: {str(e)}")
            tk.messagebox.showerror("Error", f"Scan failed: {str(e)}")
        finally:
            self.scan_btn.config(state='normal')
            
    def notify_results(self, results: dict):
        """通知其他面板扫描结果"""
        # 发布扫描完成事件
        self.frame.event_generate('<<ScanComplete>>', data=results)