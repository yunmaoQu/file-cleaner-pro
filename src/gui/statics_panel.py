import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging
from typing import Dict, Any

class StatisticsPanel:
    def __init__(self, parent):
        self.logger = logging.getLogger(__name__)
        self.frame = ttk.LabelFrame(parent, text="Statistics", padding="5")
        self.create_widgets()
        
    def create_widgets(self):
        """创建统计图表组件"""
        # 创建图表框架
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 8))
        
        # 创建画布
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 创建统计信息标签
        self.stats_frame = ttk.LabelFrame(self.frame, text="Summary", padding="5")
        self.stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.total_files_var = tk.StringVar()
        self.duplicate_files_var = tk.StringVar()
        self.total_size_var = tk.StringVar()
        self.potential_savings_var = tk.StringVar()
        
        ttk.Label(self.stats_frame, text="Total Files:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(self.stats_frame, textvariable=self.total_files_var).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(self.stats_frame, text="Duplicate Files:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(self.stats_frame, textvariable=self.duplicate_files_var).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(self.stats_frame, text="Total Size:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(self.stats_frame, textvariable=self.total_size_var).grid(row=2, column=1, sticky=tk.W)
        
        ttk.Label(self.stats_frame, text="Potential Savings:").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(self.stats_frame, textvariable=self.potential_savings_var).grid(row=3, column=1, sticky=tk.W)
        
        # 绑定更新事件
        self.frame.bind('<<ScanComplete>>', self.update_statistics)
        
    def update_statistics(self, event):
        """更新统计信息和图表"""
        results = event.data
        
        # 更新统计信息
        total_files = sum(len(files) for files in results['classified_files'].values())
        duplicate_files = sum(len(files) - 1 for files in results['duplicates'].values())
        total_size = sum(file_info['size'] for file_info in results['large_files'])
        potential_savings = sum(
            sum(os.path.getsize(f) for f in files[1:])
            for files in results['duplicates'].values()
        )
        
        self.total_files_var.set(str(total_files))
        self.duplicate_files_var.set(str(duplicate_files))
        self.total_size_var.set(self.format_size(total_size))
        self.potential_savings_var.set(self.format_size(potential_savings))
        
        # 更新文件类型分布图
        self.ax1.clear()
        # src/gui/statistics_panel.py 续：
        # 更新文件类型分布图
        self.ax1.clear()
        file_types = results['classified_files']
        types = list(file_types.keys())
        counts = [len(files) for files in file_types.values()]
        
        self.ax1.pie(counts, labels=types, autopct='%1.1f%%')
        self.ax1.set_title('File Type Distribution')
        
        # 更新文件大小分布图
        self.ax2.clear()
        size_ranges = ['0-1MB', '1-10MB', '10-100MB', '100MB-1GB', '>1GB']
        size_counts = self._get_size_distribution(results['large_files'])
        
        self.ax2.bar(size_ranges, size_counts)
        self.ax2.set_title('File Size Distribution')
        self.ax2.set_ylabel('Number of Files')
        plt.xticks(rotation=45)
        
        # 调整布局并刷新画布
        self.fig.tight_layout()
        self.canvas.draw()
        
    def _get_size_distribution(self, files: List[Dict[str, Any]]) -> List[int]:
        """计算文件大小分布"""
        size_counts = [0] * 5
        for file_info in files:
            size_mb = file_info['size'] / (1024 * 1024)
            if size_mb < 1:
                size_counts[0] += 1
            elif size_mb < 10:
                size_counts[1] += 1
            elif size_mb < 100:
                size_counts[2] += 1
            elif size_mb < 1024:
                size_counts[3] += 1
            else:
                size_counts[4] += 1
        return size_counts
    
    @staticmethod
    def format_size(size: int) -> str:
        """格式化文件大小显示"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"