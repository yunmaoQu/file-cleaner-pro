# File Cleaner Pro

## Introduction
File Cleaner Pro is an AI-powered file management and cleaning tool. It helps you find duplicate, large, and old files, optimize images, backup important data, and manage your storage efficiently with a modern GUI.

https://deepwiki.com/yunmaoQu/file-cleaner-pro
## Features

- **🔍 Intelligent File Scanning**  
  Deep learning-based duplicate file detection, smart file classification, large/old file identification, garbage file detection
- **🤖 AI-Powered Optimization**  
  Image compression (JPG/PNG), file importance analysis, content-aware file optimization
- **🔄 Automated Backup**  
  Scheduled and incremental backups, easy restore functionality
- **📊 Advanced Analytics**  
  Storage analysis, file usage patterns, space saving suggestions
- **🖥️ User-friendly GUI**  
  Modern interface, real-time progress, secure deletion


## Quick Start

### Local Run
1. **Install Python 3.10 or higher**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the application**
   ```bash
   python main.py
   ```

### Docker Run
1. **Build the image**
   ```bash
   docker build -t file-cleaner-pro .
   ```
2. **Run the container**
   ```bash
   docker run -it --rm \
     -e DISPLAY=$DISPLAY \
     -v /tmp/.X11-unix:/tmp/.X11-unix \
     -v /your/data/path:/data \
     file-cleaner-pro
   ```
   > For GUI in Windows/Mac, use VNC or X11 forwarding.

---

## Build & Release

### Build Standalone Executable (Windows example)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
# The binary will be in dist/main.exe
```

### Publish to PyPI
1. Edit `setup.py` and `setup.cfg` as needed.
2. Build and upload:
   ```bash
   python setup.py sdist bdist_wheel
   twine upload dist/*
   ```

## Usage

### GUI
1. Launch the app
2. Select a directory to scan
3. Choose scan options (e.g. find duplicates, large files, old files)
4. View and manage results
5. Apply recommended optimizations or backup

### CLI (if supported)
```bash
python main.py --help
```


## Project Structure

```text
file-cleaner-pro/
├── src/
│   ├── core/          # Core functionality
│   ├── ai/            # AI models and training
│   ├── gui/           # GUI interface
│   └── utils/         # Utility functions
├── tests/             # Test suite
├── config/            # Configuration files
├── data/              # Data directory
├── requirements.txt   # Dependencies
├── Dockerfile         # Docker support
├── setup.py           # pip/packaging
└── README.md
```


## Configuration

- Edit `config/settings.py` to customize:
  - Scanning parameters
  - AI model settings
  - Backup preferences
  - Performance options

- Environment variables (optional):
  ```bash
  export APP_DEBUG=True
  export SCAN_MAX_WORKERS=4
  export AI_USE_GPU=True
  export BACKUP_ENABLED=True
  ```


## FAQ

- **GUI not showing in Docker?**  
  Use X11 or VNC, or run locally.
- **Scan/optimize errors?**  
  Check dependencies, Python version, file permissions.
- **Supported file types?**  
  Image optimization supports jpg/jpeg/png. Other types are not auto-optimized.
- **How to contribute?**  
  Pull requests and issues are welcome! See CONTRIBUTING.md for details.

---

## Testing

```bash
pytest
# or with coverage
pytest --cov=src tests/
```

---

## License

MIT License. See LICENSE for details.

---

## Contact

- Author: ymqu823
- Email: ymqu823@gmail.com
- GitHub: [yunmaoQu](https://github.com/yunmaoQu823)

## Version History

### 1.0.0 (Current)
- Initial release
- Core functionality
- AI-powered features
- GUI interface

### Planned Features
- [ ] Cloud backup integration
- [ ] Advanced file recovery
- [ ] Network drive support
- [ ] Plugin system

## Community

Join our [Discussions](https://github.com/username/file-cleaner-pro/discussions) to:
- Ask questions
- Share ideas
- Get help
- Show your projects
- Connect with other users

---

⭐ Star us on GitHub if you find this project useful!

