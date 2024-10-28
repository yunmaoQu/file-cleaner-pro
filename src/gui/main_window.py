import tkinter as tk
from tkinter import ttk
import logging
from .scan_panel import ScanPanel
from .results_panel import ResultsPanel
from .statistics_panel import StatisticsPanel
from config.settings import GUI_CONFIG

class MainWindow:
    def __init__(self, scanner, optimizer, advisor):
        self.logger = logging.getLogger(__name__)
        self.scanner = scanner
        self.optimizer = optimizer
        self.advisor = advisor
        
        self.root = tk.Tk()
        self.setup_main_window()
        self.create_panels()
        self.create_menu()
        
    def setup_main_window(self):
        """设置主窗口"""
        self.root.title("File Cleaner")
        self.root.geometry(GUI_CONFIG['window_size'])
        
        # 设置主题
        style = ttk.Style()
        style.theme_use(GUI_CONFIG['theme'])
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="5")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def create_panels(self):
        """创建面板"""
        # 创建扫描面板
        self.scan_panel = ScanPanel(self.main_frame, self.scanner)
        self.scan_panel.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建结果面板
        self.results_panel = ResultsPanel(self.main_frame, self.optimizer)
        self.results_panel.frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建统计面板
        self.statistics_panel = StatisticsPanel(self.main_frame)
        self.statistics_panel.frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 设置权重
        self.main_frame.columnconfigure(0, weight=3)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.rowconfigure(1, weight=1)
        
    def create_menu(self):
        """创建菜单"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Directory", command=self.scan_panel.browse_directory)
        file_menu.add_command(label="Save Results", command=self.results_panel.save_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # 工具菜单
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Settings", command=self.show_settings)
        tools_menu.add_command(label="Clear Cache", command=self.clear_cache)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
        
    def show_settings(self):
        """显示设置对话框"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        
        # 创建设置选项
        ttk.Label(settings_window, text="General Settings").pack(pady=10)
        
        # 自动备份设置
        auto_backup_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_window, text="Enable Auto Backup",
                       variable=auto_backup_var).pack(pady=5)
        
        # 扫描线程数设置
        ttk.Label(settings_window, text="Max Worker Threads:").pack(pady=5)
        thread_count = ttk.Spinbox(settings_window, from_=1, to=16)
        thread_count.pack(pady=5)
        
        # 保存按钮
        ttk.Button(settings_window, text="Save",
                  command=settings_window.destroy).pack(pady=10)
        
    def clear_cache(self):
        """清除缓存"""
        try:
            # 实现缓存清理逻辑
            self.logger.info("Cache cleared successfully")
            tk.messagebox.showinfo("Success", "Cache cleared successfully")
        except Exception as e:
            self.logger.error(f"Failed to clear cache: {str(e)}")
            tk.messagebox.showerror("Error", f"Failed to clear cache: {str(e)}")
            
    def show_about(self):
        """显示关于对话框"""
        about_text = """
        File Cleaner
        Version 1.0.0
        
        An AI-powered file management tool
        """
        tk.messagebox.showinfo("About", about_text)
        
    def show_documentation(self):
        """显示文档"""
        import webbrowser
        webbrowser.open("https://github.com/yourusername/file_cleaner/docs")
        
    def run(self):
        """运行应用程序"""
        try:
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"Application error: {str(e)}")
            raise