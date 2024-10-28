from setuptools import setup, find_packages
import os

def read_requirements(filename):
    """读取requirements文件"""
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def read_file(filename):
    """读取文件内容"""
    with open(filename) as f:
        return f.read()

setup(
    name="ai_file_cleaner",
    version="1.0.0",
    author="ymqu823",
    author_email="ymqu823@gmail.com",
    description="An AI-powered file cleaning and management tool",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/file_cleaner",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements('requirements/base.txt'),
    extras_require={
        'dev': read_requirements('requirements/dev.txt'),
        'prod': read_requirements('requirements/prod.txt'),
    },
    entry_points={
        'console_scripts': [
            'file-cleaner=src.main:main',
        ],
    },
    include_package_data=True,
    package_data={
        'file_cleaner': [
            'config/*.py',
            'data/models/*.h5',
            'data/logs/.gitkeep',
            'data/backups/.gitkeep',
        ],
    },
    data_files=[
        ('config', ['config/settings.py', 'config/logging_config.py']),
    ],
    zip_safe=False,
)