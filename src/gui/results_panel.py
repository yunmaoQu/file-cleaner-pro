import tkinter as tk
from tkinter import ttk
import logging
from typing import Dict, Any
import json

class ResultsPanel:
    def __init__(self, parent, optimizer):
        self.logger = logging.getLogger(__name__)
        self.optimizer = optimizer
        self.frame = ttk.LabelFrame(parent, text="Results", padding="5")
        self.create_widgets()
        
    def create_widgets(self):
        """创建结果显示组件"""
        # 创建表格
        self.tree = ttk.Treeview(self.frame, columns=('Type', 'Path', 'Size', 'Action'),
                                show='headings')
        
        # 设置列标题
        self.tree.heading('Type', text='Type')
        self.tree.heading('Path', text='Path')
        self.tree.heading('Size', text='Size')
        self.tree.heading('Action', text='Action')
        
        # 设置列宽
        self.tree.column('Type', width=100)
        self.tree.column('Path', width=300)
        self.tree.column('Size', width=100)
        self.tree.column('Action', width=100)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL,
                                command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 放置组件
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 操作按钮框架
        btn_frame = ttk.Frame(self.frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(btn_frame, text="Clean Selected",
                  command=self.clean_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Optimize Selected",
                  command=self.optimize_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Export Results",
                  command=self.export_results).pack(side=tk.LEFT, padx=5)
        
        # 绑定事件处理
        self.tree.bind('<Double-1>', self.on_item_double_click)
        self.frame.bind('<<ScanComplete>>', self.update_results)
        
    def update_results(self, event):
        """更新扫描结果显示"""
        # 清空现有项目
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 获取扫描结果
        results = event.data
        
        # 添加重复文件
        for hash_value, duplicates in results.get('duplicates', {}).items():
            for file_path in duplicates:
                self.tree.insert('', 'end', values=(
                    'Duplicate',
                    file_path,
                    self.format_size(os.path.getsize(file_path)),
                    'Remove'
                ))
                
        # 添加大文件
        for file_info in results.get('large_files', []):
            self.tree.insert('', 'end', values=(
                'Large File',
                file_info['path'],
                self.format_size(file_info['size']),
                'Optimize'
            ))
            
        # 添加旧文件
        for file_info in results.get('old_files', []):
            self.tree.insert('', 'end', values=(
                'Old File',
                file_info['path'],
                self.format_size(os.path.getsize(file_info['path'])),
                'Archive'
            ))
            
    def clean_selected(self):
        """清理选中的文件"""
        selected_items = self.tree.selection()
        if not selected_items:
            tk.messagebox.showinfo("Info", "Please select items to clean")
            return
            
        if tk.messagebox.askyesno("Confirm", "Are you sure you want to clean selected items?"):
            for item in selected_items:
                values = self.tree.item(item)['values']
                try:
                    file_path = values[1]
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        self.tree.delete(item)
                except Exception as e:
                    self.logger.error(f"Failed to delete {file_path}: {str(e)}")
                    tk.messagebox.showerror("Error", f"Failed to delete {file_path}: {str(e)}")
            
            tk.messagebox.showinfo("Success", "Selected items have been cleaned")
            
    def optimize_selected(self):
        """优化选中的文件"""
        selected_items = self.tree.selection()
        if not selected_items:
            tk.messagebox.showinfo("Info", "Please select items to optimize")
            return
            
        for item in selected_items:
            values = self.tree.item(item)['values']
            file_path = values[1]
            try:
                result = self.optimizer.optimize_file(file_path)
                if result:
                    self.tree.set(item, 'Size', self.format_size(result['optimized_size']))
                    self.tree.set(item, 'Action', 'Optimized')
            except Exception as e:
                self.logger.error(f"Failed to optimize {file_path}: {str(e)}")
                tk.messagebox.showerror("Error", f"Failed to optimize {file_path}: {str(e)}")
                
    def export_results(self):
        """导出扫描结果"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                results = []
                for item in self.tree.get_children():
                    values = self.tree.item(item)['values']
                    results.append({
                        'type': values[0],
                        'path': values[1],
                        'size': values[2],
                        'action': values[3]
                    })
                    
                with open(file_path, 'w') as f:
                    json.dump(results, f, indent=4)
                    
                tk.messagebox.showinfo("Success", "Results exported successfully")
                
            except Exception as e:
                self.logger.error(f"Failed to export results: {str(e)}")
                tk.messagebox.showerror("Error", f"Failed to export results: {str(e)}")
                
    def on_item_double_click(self, event):
        """双击项目时的处理"""
        item = self.tree.selection()[0]
        values = self.tree.item(item)['values']
        file_path = values[1]
        
        try:
            # 在文件管理器中显示文件
            if os.path.exists(file_path):
                if sys.platform == 'win32':
                    os.startfile(os.path.dirname(file_path))
                elif sys.platform == 'darwin':
                    subprocess.run(['open', os.path.dirname(file_path)])
                else:
                    subprocess.run(['xdg-open', os.path.dirname(file_path)])
        except Exception as e:
            self.logger.error(f"Failed to open file location: {str(e)}")
            
    @staticmethod
    def format_size(size: int) -> str:
        """格式化文件大小显示"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"