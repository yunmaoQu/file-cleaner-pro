import os
import sys
from models import AIModels
from file_scanner import FileScanner
from file_optimizer import FileOptimizer
from file_advisor import FileAdvisor
from gui import CleanerGUI

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

def main():
    try:
        app = FileCleanerApp()
        app.run()
    except Exception as e:
        print(f"Application error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()