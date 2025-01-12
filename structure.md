

```
file_cleaner/
│
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── scanner.py          # 基础文件扫描器
│   │   ├── threaded_scanner.py # 多线程扫描器
│   │   ├── optimizer.py        # 文件优化器
│   │   ├── advisor.py          # 文件管理建议
│   │   ├── recovery.py         # 文件恢复功能
│   │   └── backup.py           # 自动备份功能
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── models.py           # AI模型定义
│   │   ├── trainer.py          # 模型训练
│   │   └── predictor.py        # 模型预测
│   │
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py      # 主窗口
│   │   ├── scan_panel.py       # 扫描面板
│   │   ├── results_panel.py    # 结果显示面板
│   │   └── statistics_panel.py # 统计图表面板
│   │
│   └── utils/
│       ├── __init__.py
│       ├── file_utils.py       # 文件操作工具
│       ├── hash_utils.py       # 哈希计算工具
│       └── system_utils.py     # 系统相关工具
│
├── tests/
│   ├── __init__.py
│   ├── test_scanner.py
│   ├── test_optimizer.py
│   ├── test_recovery.py
│   └── test_backup.py
│
├── data/
│   ├── models/                 # 保存训练好的模型
│   ├── backups/               # 文件备份目录
│   └── logs/                  # 日志文件目录
│
├── config/
│   ├── __init__.py
│   ├── settings.py            # 基本配置
│   └── logging_config.py      # 日志配置
│
├── requirements.txt           # 项目依赖
├── setup.py                  # 安装脚本
├── README.md                 # 项目说明
└── main.py                   # 程序入口
