from setuptools import setup, find_packages

setup(
    name="stock-strategy",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A quantitative trading strategy platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/stock-strategy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.32.0",
        "streamlit-option-menu>=0.3.2",
        "streamlit-echarts>=0.4.0",
        "pandas>=2.2.0",
        "numpy>=1.24.0",
        "plotly>=5.18.0",
        "scipy>=1.10.0",
        "akshare>=1.10.0",
        "ta>=0.10.0",
        "empyrical>=0.5.5",
        "psutil>=5.9.0"
    ],
    entry_points={
        'console_scripts': [
            'stock-strategy=src.ui.app:main',
        ],
    }
) 