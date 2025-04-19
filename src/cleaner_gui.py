import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import time
import threading

class CleanerGUI:
    def __init__(self, scanner, optimizer, advisor):
        self.scanner = scanner
        self.optimizer = optimizer
        self.advisor = advisor
        self.window = tk.Tk()
        self.window.title("File Cleaner Assistant")
        self.window.geometry("800x600")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        self.main_frame = ttk.Frame(self.window, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 扫描按钮和路径选择
        self.scan_frame = ttk.LabelFrame(self.main_frame, text="Scan", padding="5")
        self.scan_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(self.scan_frame, textvariable=self.path_var)
        self.path_entry.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        self.browse_button = ttk.Button(self.scan_frame, text="Browse", command=self.browse_directory)
        self.browse_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.scan_button = ttk.Button(self.scan_frame, text="Start Scan", command=self.start_scan)
        self.scan_button.grid(row=0, column=2, padx=5, pady=5)
        
        # 结果显示区域
        self.results_frame = ttk.LabelFrame(self.main_frame, text="Results", padding="5")
        self.results_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建表格来显示结果
        self.tree = ttk.Treeview(self.results_frame, columns=('Type', 'Path', 'Size', 'Action'))
        self.tree.heading('Type', text='Type')
        self.tree.heading('Path', text='Path')
        self.tree.heading('Size', text='Size')
        self.tree.heading('Action', text='Action')
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 操作按钮
        self.action_frame = ttk.Frame(self.main_frame, padding="5")
        self.action_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.clean_button = ttk.Button(self.action_frame, text="Clean Selected", command=self.clean_selected)
        self.clean_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.optimize_button = ttk.Button(self.action_frame, text="Optimize Selected", command=self.optimize_selected)
        self.optimize_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.backup_button = ttk.Button(self.action_frame, text="Backup Selected", command=self.backup_selected)
        self.backup_button.grid(row=0, column=2, padx=5, pady=5)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var)
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
    
    def browse_directory(self):
        """选择要扫描的目录"""
        directory = filedialog.askdirectory()
        if directory:
            self.path_var.set(directory)
    
    def start_scan(self):
        """开始扫描目录"""
        directory = self.path_var.get()
        if not directory:
            messagebox.showerror("Error", "Please select a directory first")
            return
        
        try:
            self.status_var.set("Scanning...")
            self.window.update()
            
            # 执行扫描
            scan_results = self.scanner.scan_directory(directory)
            
            # 获取优化建议
            optimization_suggestions = self.optimizer.suggest_optimizations(scan_results)
            
            # 获取管理建议
            recommendations = self.advisor.generate_recommendations(scan_results)
            
            # 清空现有结果
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # 显示扫描结果
            self.display_results(scan_results, optimization_suggestions, recommendations)
            
            self.status_var.set("Scan completed")
            
            # 显示统计图表
            self.show_statistics(scan_results)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during scanning: {str(e)}")
            self.status_var.set("Scan failed")
    
    def display_results(self, scan_results, optimization_suggestions, recommendations):
        """显示扫描结果"""
        # 显示重复文件
        for hash_value, duplicates in scan_results['duplicates'].items():
            for file_path in duplicates:
                size = os.path.getsize(file_path)
                if math.isnan(size):
                    size = 0
                self.tree.insert('', 'end', values=('Duplicate', file_path, 
                                                  self.format_size(size),
                                                  'Remove duplicate'))
        
        # 显示大文件
        for file_info in scan_results['large_files']:
            size = file_info['size']
            if math.isnan(size):
                size = 0
            self.tree.insert('', 'end', values=('Large File', file_info['path'],
                                              self.format_size(size),
                                              'Optimize'))
        
        # 显示旧文件
        for file_info in scan_results['old_files']:
            size = os.path.getsize(file_info['path'])
            if math.isnan(size):
                size = 0
            self.tree.insert('', 'end', values=('Old File', file_info['path'],
                                              self.format_size(size),
                                              'Archive'))
    
    def format_size(self, size):
        """格式化文件大小显示"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"
    
    def show_statistics(self, scan_results):
        """显示统计图表"""
        # 创建新窗口显示统计信息
        stats_window = tk.Toplevel(self.window)
        stats_window.title("Scan Statistics")
        stats_window.geometry("600x400")
        
        # 创建图表
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        
        # 文件类型分布饼图
        type_sizes = {k: sum(os.path.getsize(f) for f in v) for k, v in scan_results['classified_files'].items()}
        total = sum(type_sizes.values())
        if total == 0 or any(math.isnan(v) for v in type_sizes.values()):
            # 避免全为0或有NaN时绘图
            ax1.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=14)
        else:
            ax1.pie(type_sizes.values(), labels=type_sizes.keys(), autopct='%1.1f%%')
        ax1.set_title('File Type Distribution')
        
        # 文件大小柱状图
        file_categories = ['Large Files', 'Duplicates', 'Old Files']
        file_counts = [
            len(scan_results['large_files']),
            sum(len(files) for files in scan_results['duplicates'].values()),
            len(scan_results['old_files'])
        ]
        # NaN 检查
        file_counts = [0 if math.isnan(x) else x for x in file_counts]
        ax2.bar(file_categories, file_counts)
        ax2.set_title('File Counts by Category')
        
        # 将图表添加到窗口
        canvas = FigureCanvasTkAgg(fig, master=stats_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
    
    def clean_selected(self):
        """清理选中的文件"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Please select items to clean")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to clean selected items?"):
            for item in selected_items:
                values = self.tree.item(item)['values']
                try:
                    os.remove(values[1])  # values[1] 是文件路径
                    self.tree.delete(item)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete {values[1]}: {str(e)}")
            
            messagebox.showinfo("Success", "Selected items have been cleaned")
    
    def optimize_selected(self):
        """优化选中的文件"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "请选择要优化的文件")
            return
        
        # 询问用户是否要删除原始文件
        delete_original = messagebox.askyesno("删除原始文件", 
            "优化完成后是否删除原始文件？\n\n注意：只有当优化成功且节省了空间时才会删除原始文件。")
        
        # 询问是否一并删除副本文件
        delete_copies = False
        if delete_original:
            delete_copies = messagebox.askyesno("删除副本文件", 
                "是否同时删除与原始文件相关的副本文件？\n例如：同名但包含'副本'字样的文件")
        
        optimization_results = []
        for item in selected_items:
            values = self.tree.item(item)['values']
            file_path = values[1]
            
            if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
                result = self.optimizer.optimize_image(file_path)
                if result:
                    optimization_results.append(result)
            else:
                messagebox.showinfo("Info", f"无法优化 {file_path}\n不支持的文件类型 - 仅支持图像文件")
        
        # 处理优化结果
        if not optimization_results:
            return
            
        # 计算总结果
        successful = [r for r in optimization_results if r.get('success', False)]
        already_optimized = [r for r in optimization_results if r.get('already_optimized', False)]
        failed = [r for r in optimization_results if not r.get('success', True) and not r.get('already_optimized', False)]
        
        # 如果用户选择了删除原始文件，且有成功优化的文件
        deleted_files = []
        deleted_copies = []
        if delete_original and successful:
            for result in successful:
                try:
                    original_path = result['original_path']
                    # 删除原始文件
                    if os.path.exists(original_path):
                        os.remove(original_path)
                        deleted_files.append(original_path)
                    
                    # 如果选择删除副本文件，查找并删除相关副本
                    if delete_copies:
                        self._delete_related_copies(original_path, deleted_copies)
                        
                except Exception as e:
                    print(f"Error deleting original file {original_path}: {e}")
        
        total_original = sum(r['original_size'] for r in optimization_results)
        total_optimized = sum(r['optimized_size'] for r in successful)
        total_saved = sum(r['saved_space'] for r in successful)
        
        # 构建结果消息
        if successful:
            if len(successful) == 1:
                # 单个文件优化成功的消息
                r = successful[0]
                saved_percent = (r['saved_space'] / r['original_size']) * 100 if r['original_size'] > 0 else 0
                
                # 确保路径使用正确的分隔符
                optimized_path = os.path.normpath(r['optimized_path'])
                
                msg = (f"优化成功: {os.path.basename(r['original_path'])}\n\n"
                       f"原始大小: {self.format_size(r['original_size'])}\n"
                       f"优化后大小: {self.format_size(r['optimized_size'])}\n"
                       f"节省空间: {self.format_size(r['saved_space'])} ({saved_percent:.1f}%)\n"
                       f"格式: {r['format']}\n\n"
                       f"保存到: {optimized_path}")
                
                if r['original_path'] in deleted_files:
                    msg += "\n\n原始文件已删除"
                    
                if deleted_copies:
                    msg += f"\n同时删除了 {len(deleted_copies)} 个相关副本文件"
                    
                messagebox.showinfo("优化成功", msg)
            else:
                # 多个文件优化成功的汇总消息
                saved_percent = (total_saved / total_original) * 100 if total_original > 0 else 0
                msg = (f"成功优化 {len(successful)} 个文件\n\n"
                       f"总原始大小: {self.format_size(total_original)}\n"
                       f"总优化后大小: {self.format_size(total_optimized)}\n"
                       f"总节省空间: {self.format_size(total_saved)} ({saved_percent:.1f}%)\n\n")
                
                # 添加详细信息
                for i, r in enumerate(successful, 1):
                    file_saved_percent = (r['saved_space'] / r['original_size']) * 100 if r['original_size'] > 0 else 0
                    file_msg = f"{i}. {os.path.basename(r['original_path'])}: 节省 {self.format_size(r['saved_space'])} ({file_saved_percent:.1f}%)"
                    if r['original_path'] in deleted_files:
                        file_msg += " (原始文件已删除)"
                    msg += file_msg + "\n"
                
                if deleted_copies:
                    msg += f"\n同时删除了 {len(deleted_copies)} 个相关副本文件"
                    
                messagebox.showinfo("批量优化结果", msg)
        
        # 显示已经优化过的文件
        if already_optimized:
            files = "\n".join(os.path.basename(r['original_path']) for r in already_optimized)
            messagebox.showinfo("已优化文件", f"以下 {len(already_optimized)} 个文件已经优化过:\n\n{files}")
        
        # 显示优化失败的文件
        if failed:
            files = "\n".join(os.path.basename(r['original_path']) for r in failed)
            messagebox.showinfo("优化失败", f"以下 {len(failed)} 个文件优化失败:\n\n{files}")
            
        # 刷新列表显示
        status_msg = f"优化完成: 成功 {len(successful)}, 已优化 {len(already_optimized)}, 失败 {len(failed)}"
        if deleted_files:
            status_msg += f", 删除原始文件 {len(deleted_files)}"
        if deleted_copies:
            status_msg += f", 删除副本文件 {len(deleted_copies)}"
        self.status_var.set(status_msg)
    
    def _delete_related_copies(self, file_path, deleted_list):
        """删除与指定文件相关的副本文件"""
        try:
            dir_path = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            
            # 获取文件的基本名称（移除可能的 "副本" 字样）
            base_name = name.replace(" - 副本", "").replace("_副本", "").replace("(副本)", "")
            
            # 构建可能的副本文件名模式
            copy_patterns = [
                f"{base_name} - 副本{ext}",
                f"{base_name}_副本{ext}",
                f"{base_name}(副本){ext}",
                f"{base_name} - 副本 ({d}){ext}" for d in range(1, 10)
            ]
            
            # 遍历目录查找匹配的副本文件
            for filename in os.listdir(dir_path):
                file_path = os.path.join(dir_path, filename)
                if os.path.isfile(file_path) and any(filename == pattern for pattern in copy_patterns):
                    try:
                        os.remove(file_path)
                        deleted_list.append(file_path)
                        print(f"Deleted copy file: {file_path}")
                    except Exception as e:
                        print(f"Failed to delete copy file {file_path}: {e}")
                        
        except Exception as e:
            print(f"Error finding related copies: {e}")
    
    def backup_selected(self):
        """备份选中的文件"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Please select items to backup")
            return
        
        backup_dir = filedialog.askdirectory(title="Select Backup Directory")
        if not backup_dir:
            return
        
        for item in selected_items:
            values = self.tree.item(item)['values']
            file_path = values[1]
            try:
                filename = os.path.basename(file_path)
                backup_path = os.path.join(backup_dir, filename)
                shutil.copy2(file_path, backup_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to backup {file_path}: {str(e)}")
        
        messagebox.showinfo("Success", "Selected items have been backed up")
    
    def on_close(self):
        """关闭应用程序并终止所有后台线程"""
        try:
            print("Closing application...")
            
            # 终止扫描器中的线程
            if hasattr(self.scanner, 'threaded_scanner'):
                print("Stopping scanner threads...")
                # 设置停止事件
                self.scanner.threaded_scanner.stop_event.set()
                
            # 终止优化器中的线程
            if hasattr(self.optimizer, 'stop_all_tasks'):
                print("Stopping optimizer tasks...")
                self.optimizer.stop_all_tasks()
                
            # 终止备份过程中的线程
            if hasattr(self.optimizer, 'backup') and hasattr(self.optimizer.backup, 'stop_auto_backup'):
                print("Stopping backup threads...")
                self.optimizer.backup.stop_auto_backup()
                
            # 等待一小段时间以确保线程有机会终止
            time.sleep(0.5)
            
            # 打印所有线程信息
            print("Current threads:")
            for thread in threading.enumerate():
                print(f"  - {thread.name} (daemon: {thread.daemon})")
                
            # 销毁窗口
            print("Destroying window...")
            self.window.destroy()
            
            # 强制终止进程 - 最后的手段
            print("Forcing application exit...")
            import os
            os._exit(0)  # 强制退出，不会调用清理处理程序
            
        except Exception as e:
            print(f"Error while closing application: {e}")
            # 如果出现异常，仍然强制退出
            import os
            os._exit(1)
    
    def run(self):
        """运行应用程序"""
        self.window.mainloop()

__all__ = ['CleanerGUI']