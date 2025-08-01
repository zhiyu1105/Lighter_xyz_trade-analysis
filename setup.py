from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="trade-analysis",
    version="1.0.0",
    author="TradeAnalysis Team",
    author_email="your.email@example.com",
    description="一个功能强大、易于使用的交易数据分析工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhiyu1105/Lighter_xyz_trade-analysis",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "trade-analysis=example_analysis:main",
        ],
    },
    include_package_data=True,
    package_data={
        "trade_analyzer": ["*.py"],
    },
    keywords="trading, analysis, finance, cryptocurrency, backtesting, risk-management",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/trade-analysis/issues",
        "Source": "https://github.com/yourusername/trade-analysis",
        "Documentation": "https://github.com/yourusername/trade-analysis#readme",
    },
) 