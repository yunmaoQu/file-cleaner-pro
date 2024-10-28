


# File Cleaner Pro

An AI-powered file management and cleaning tool that helps you organize, optimize, and maintain your files efficiently.

## Features

### Core Features
- 🔍 **Intelligent File Scanning**
  - Deep learning-based duplicate file detection
  - Smart file classification
  - Large file identification
  - Garbage file detection

- 🤖 **AI-Powered Optimization**
  - Intelligent image compression
  - Smart format conversion
  - Content-aware file optimization
  - Automated file importance assessment

- 🔄 **Automated Backup**
  - Scheduled automatic backups
  - Incremental backup support
  - Backup encryption
  - Easy restore functionality

- 📊 **Advanced Analytics**
  - Detailed storage analysis
  - File usage patterns
  - Duplicate file reports
  - Space saving recommendations

### Additional Features
- 🎯 Multi-threaded scanning for improved performance
- 💾 Secure file deletion with recovery options
- 📱 User-friendly GUI interface
- 📈 Real-time progress monitoring
- 🔐 Built-in security features

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Virtual environment (recommended)

### Basic Installation
```bash
# Clone the repository
git clone https://github.com/yunmaoQu/file-cleaner-pro.git
cd file-cleaner-pro

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .

下面是一个详细的 README.md 文件：

```markdown
# File Cleaner Pro

An AI-powered file management and cleaning tool that helps you organize, optimize, and maintain your files efficiently.

## Features

### Core Features
- 🔍 **Intelligent File Scanning**
  - Deep learning-based duplicate file detection
  - Smart file classification
  - Large file identification
  - Garbage file detection

- 🤖 **AI-Powered Optimization**
  - Intelligent image compression
  - Smart format conversion
  - Content-aware file optimization
  - Automated file importance assessment

- 🔄 **Automated Backup**
  - Scheduled automatic backups
  - Incremental backup support
  - Backup encryption
  - Easy restore functionality

- 📊 **Advanced Analytics**
  - Detailed storage analysis
  - File usage patterns
  - Duplicate file reports
  - Space saving recommendations

### Additional Features
- 🎯 Multi-threaded scanning for improved performance
- 💾 Secure file deletion with recovery options
- 📱 User-friendly GUI interface
- 📈 Real-time progress monitoring
- 🔐 Built-in security features

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Virtual environment (recommended)

### Basic Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/file-cleaner-pro.git
cd file-cleaner-pro

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Development Installation
```bash
# Install development dependencies
pip install -r requirements/dev.txt
```

## Usage

### Quick Start
```bash
# Run the application
python -m src.main

# Or use the command-line interface
file-cleaner scan /path/to/directory
```

### GUI Interface
1. Launch the application
2. Select directory to scan
3. Choose scanning options
4. View and manage results
5. Apply recommended optimizations

### Command Line Interface
```bash
# Scan directory
file-cleaner scan /path/to/directory

# Optimize files
file-cleaner optimize /path/to/file

# Create backup
file-cleaner backup /path/to/backup

# Restore backup
file-cleaner restore backup_name
```

## Configuration

### Basic Configuration
Edit `config/settings.py` to customize:
- Scanning parameters
- AI model settings
- Backup preferences
- Performance options

### Environment Variables
```bash
# Set environment variables
export APP_DEBUG=True
export SCAN_MAX_WORKERS=4
export AI_USE_GPU=True
export BACKUP_ENABLED=True
```

## Development

### Project Structure
```
file_cleaner/
├── src/
│   ├── core/          # Core functionality
│   ├── ai/            # AI models and training
│   ├── gui/           # GUI interface
│   └── utils/         # Utility functions
├── tests/             # Test suite
├── config/            # Configuration files
└── data/              # Data directory
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_scanner.py

# Run with coverage
pytest --cov=src tests/
```

### Contributing
1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

## Performance Tips

### Optimization
- Enable multi-threading for faster scanning
- Use GPU acceleration when available
- Adjust chunk size for large file operations
- Configure appropriate memory limits

### Resource Usage
- Monitor memory usage with built-in tools
- Use batch processing for large directories
- Enable compression for backups
- Configure appropriate worker counts

## Troubleshooting

### Common Issues
1. **Slow Scanning**
   - Reduce worker count
   - Increase chunk size
   - Disable deep scanning

2. **High Memory Usage**
   - Adjust memory limits
   - Enable batch processing
   - Reduce worker count

3. **GPU Issues**
   - Verify GPU drivers
   - Check CUDA installation
   - Fall back to CPU processing

### Logs
- Check logs in `data/logs/`
- Enable debug mode for detailed logging
- Use built-in diagnostic tools

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- TensorFlow team for AI capabilities
- Python community for excellent libraries
- Contributors and testers

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

---

⭐ Star us on GitHub if you find this project useful!

