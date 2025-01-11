from setuptools import setup, find_packages

setup(
    name="stock-strategy",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.32.0",
        "pandas>=2.2.0",
        "numpy>=1.24.0",
        "plotly>=5.18.0",
        "akshare>=1.10.0",
        "ta>=0.10.0",
        "empyrical>=0.5.5",
        "psutil>=5.9.0"
    ],
    entry_points={
        'console_scripts': [
            'stock-strategy=app:main',
        ],
    }
) 