from setuptools import setup, find_packages
import os

def read_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def read_file(filename):
    with open(filename) as f:
        return f.read()

setup(
    name='file-cleaner-pro',
    version='1.0.0',
    description='AI-powered file management and cleaning tool',
    author='ymqu823',
    author_email='ymqu823@gmail.com',
    url='https://github.com/yunmaoQu/file-cleaner-pro',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'tensorflow>=2.0.0',
        'pillow>=8.0.0',
        'matplotlib>=3.0.0',
        'numpy>=1.19.0',
        'pandas>=1.1.0',
        'psutil>=5.8.0',
        'xxhash>=2.0.0',
        'schedule>=1.1.0',
        'PyQt5>=5.15.0',
        'python-magic>=0.4.0',
    ],
    entry_points={
        'console_scripts': [
            'file-cleaner=file_cleaner_pro.main:main',
        ],
    },
    python_requires='>=3.10',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
)
