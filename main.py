import sys
import os
import atexit
import signal
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from models import AIModels
from core.file_scanner import FileScanner
from core.file_optimizer import FileOptimizer
from core.file_advisor import FileAdvisor
from cleaner_gui import CleanerGUI

# 全局变量存储应用实例
app = None

class FileCleanerApp:
    def __init__(self):
        # 初始化AI模型
        self.ai_models = AIModels()
        
        # 初始化各个组件
        self.scanner = FileScanner(self.ai_models)
        self.optimizer = FileOptimizer()
        self.advisor = FileAdvisor(self.ai_models)
        
        # 初始化GUI
        self.gui = CleanerGUI(self.scanner, self.optimizer, self.advisor)
    
    def run(self):
        """运行应用程序"""
        self.gui.run()
        
    def cleanup(self):
        """清理资源"""
        print("Cleaning up resources...")
        try:
            # 确保GUI关闭
            if hasattr(self, 'gui') and hasattr(self.gui, 'on_close'):
                self.gui.on_close()
                # gui.on_close已经包含了os._exit调用，所以这个函数不会继续执行
            
            # 如果on_close没有退出程序，那么我们在这里强制退出
            print("Force exit from cleanup")
            os._exit(0)
        except Exception as e:
            print(f"Error during cleanup: {e}")
            os._exit(1)

def signal_handler(sig, frame):
    """处理信号以确保正确关闭"""
    print(f"Received signal {sig}, shutting down...")
    try:
        if app:
            app.cleanup()
        # 强制退出，不执行任何额外的清理操作
        os._exit(0)
    except Exception as e:
        print(f"Error during shutdown: {e}")
        os._exit(1)

def exit_handler():
    """注册退出处理函数"""
    print("Exit handler called...")
    try:
        if app:
            app.cleanup()
    except Exception as e:
        print(f"Error during exit cleanup: {e}")
        # 在异常情况下不调用os._exit，让普通退出过程继续

def main():
    global app
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 注册退出处理函数
    atexit.register(exit_handler)
    
    try:
        app = FileCleanerApp()
        app.run()
    except Exception as e:
        print(f"Application error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()