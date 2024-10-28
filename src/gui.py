import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CleanerGUI:
    def __init__(self, scanner, optimizer, advisor):
        self.scanner = scanner
        self.optimizer = optimizer
        self.advisor = advisor
        self.window = tk.Tk()
        self.window.title("File Cleaner Assistant")
        self.window.geometry("800x600")
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
                self.tree.insert('', 'end', values=('Duplicate', file_path, 
                                                  self.format_size(os.path.getsize(file_path)),
                                                  'Remove duplicate'))
        
        # 显示大文件
        for file_info in scan_results['large_files']:
            self.tree.insert('', 'end', values=('Large File', file_info['path'],
                                              self.format_size(file_info['size']),
                                              'Optimize'))
        
        # 显示旧文件
        for file_info in scan_results['old_files']:
            self.tree.insert('', 'end', values=('Old File', file_info['path'],
                                              self.format_size(os.path.getsize(file_info['path'])),
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
        type_sizes = {k: sum(os.path.getsize(f) for f in v) 
                     for k, v in scan_results['classified_files'].items()}
        ax1.pie(type_sizes.values(), labels=type_sizes.keys(), autopct='%1.1f%%')
        ax1.set_title('File Type Distribution')
        
        # 文件大小柱状图
        file_categories = ['Large Files', 'Duplicates', 'Old Files']
        file_counts = [
            len(scan_results['large_files']),
            sum(len(files) for files in scan_results['duplicates'].values()),
            len(scan_results['old_files'])
        ]
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
            messagebox.showinfo("Info", "Please select items to optimize")
            return
        
        for item in selected_items:
            values = self.tree.item(item)['values']
            file_path = values[1]
            
            if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                result = self.optimizer.optimize_image(file_path)
                if result:
                    messagebox.showinfo("Success", 
                        f"Optimized {file_path}\nSpace saved: {self.format_size(result['saved_space'])}")
            else:
                messagebox.showinfo("Info", f"Cannot optimize {file_path}: Unsupported file type")
    
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
    
    def run(self):
        """运行应用程序"""
        self.window.mainloop()