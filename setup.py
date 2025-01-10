from setuptools import setup, find_packages

setup(
    name="stock-strategy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.32.0",
        "pandas>=2.2.0",
        "numpy>=1.24.0",
        "plotly>=5.18.0",
        "psutil>=5.9.0"
    ],
    python_requires=">=3.8",
) 