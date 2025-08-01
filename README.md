# 📈 Trade Analysis Framework

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](CHANGELOG.md)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](https://github.com/zhiyu1105/Lighter_xyz_trade-analysis/actions)
[![Code Coverage](https://img.shields.io/badge/Coverage-85%25-brightgreen.svg)](https://github.com/zhiyu1105/Lighter_xyz_trade-analysis)

[![Data Analysis](https://img.shields.io/badge/Data%20Analysis-✓-success.svg)]()
[![Visualization](https://img.shields.io/badge/Visualization-✓-success.svg)]()
[![Risk Metrics](https://img.shields.io/badge/Risk%20Metrics-✓-success.svg)]()
[![Web Interface](https://img.shields.io/badge/Web%20Interface-✓-success.svg)]()

[![Pandas](https://img.shields.io/badge/Pandas-2.0+-blue.svg)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.24+-blue.svg)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-blue.svg)](https://matplotlib.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.15+-blue.svg)](https://plotly.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)](https://streamlit.io/)

[![Code Style](https://img.shields.io/badge/Code%20Style-Black-black.svg)](https://black.readthedocs.io/)
[![Linting](https://img.shields.io/badge/Linting-Flake8-yellow.svg)](https://flake8.pycqa.org/)
[![Type Checking](https://img.shields.io/badge/Type%20Checking-MyPy-blue.svg)](https://mypy.readthedocs.io/)
[![Testing](https://img.shields.io/badge/Testing-Pytest-green.svg)](https://pytest.org/)

[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)]()
[![Python Version](https://img.shields.io/badge/Python%20Version-3.8%2B-blue.svg)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/Dependencies-Up%20to%20Date-brightgreen.svg)](requirements.txt)

[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Issues](https://img.shields.io/badge/Issues-Welcome-brightgreen.svg)](https://github.com/zhiyu1105/Lighter_xyz_trade-analysis/issues)
[![Pull Requests](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](https://github.com/zhiyu1105/Lighter_xyz_trade-analysis/pulls)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A powerful and easy-to-use trading data analysis tool that supports multiple data formats and provides comprehensive trading performance analysis and visualization capabilities.

**[📖 中文文档](README_CN.md)** | **[📊 在线演示](https://zhiyu1105.github.io/Lighter_xyz_trade-analysis)**

## ✨ Key Features

### 🔧 Core Features
- **Multi-format Data Import**: Supports CSV and Excel trading data formats
- **Smart Data Cleaning**: Automatic data format standardization and missing value handling
- **Comprehensive Performance Analysis**: P&L analysis, risk metrics, drawdown analysis, etc.
- **Rich Visualization**: Static charts and interactive chart support
- **Report Generation**: One-click generation of comprehensive analysis reports in JSON format

### 📊 Analysis Dimensions
- **P&L Analysis**: Total P&L, win rate, profit factor, maximum profit/loss
- **Risk Analysis**: Sharpe ratio, maximum drawdown, VaR, CVaR
- **Trading Frequency**: Time-based analysis of trading frequency and patterns
- **Position Analysis**: Long/short position distribution and performance comparison
- **Time Analysis**: Trading time habits and performance patterns

### 🎨 Visualization Charts
- Cumulative P&L curves
- Drawdown charts
- Price charts with trade point markers
- P&L distribution histograms
- Trading frequency heatmaps
- Comprehensive analysis dashboard

## 🚀 Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Method 1: Web Interface (Recommended)

Launch the Streamlit application:

```bash
streamlit run app.py
```

Then open the displayed address in your browser (usually `http://localhost:8501`).

### Method 2: Command Line Usage

#### Analyze Example Data
```bash
python example_analysis.py
```

#### Analyze Custom Files
```bash
python example_analysis.py your_trade_data.csv
```

### Method 3: Code Integration

```python
from trade_analyzer import TradeDataProcessor, TradeAnalyzer, TradeVisualizer

# Load data
processor = TradeDataProcessor()
data = processor.load_csv('your_trade_data.csv')

# Analysis
analyzer = TradeAnalyzer(data)
pnl_stats = analyzer.calculate_pnl_statistics()
risk_metrics = analyzer.calculate_risk_metrics()

# Visualization
visualizer = TradeVisualizer(data)
fig = visualizer.plot_pnl_curve()
visualizer.save_all_charts('output_charts')
```

## 📁 Data Format Requirements

Your trading data file should contain the following columns (column names are case-insensitive):

| Column Name | Description | Required | Example |
|-------------|-------------|----------|---------|
| Market | Market/Instrument | Optional | BTC, ETH, AAPL |
| Side | Trade Direction | Optional | Long, Short, Long > Short |
| Date | Trade Date/Time | **Required** | 2025-01-01 10:30:00 |
| Trade Value | Trade Value | Optional | 1000.50 |
| Size | Trade Size | Optional | 0.001 |
| Price | Trade Price | Optional | 50000.0 |
| Closed PnL | Realized P&L | **Required** | 15.25, -8.50 |
| Fee | Transaction Fee | Optional | 2.0 |
| Role | Role | Optional | Maker, Taker |

### Data Example

```csv
Market,Side,Date,Trade Value,Size,Price,Closed PnL,Fee,Role,Type
BTC,Long > Short,2025-01-01 10:30:00,1000.5,0.001,50000,15.25,2.0,Taker,trade
BTC,Short > Long,2025-01-01 11:15:00,980.3,0.001,49015,-8.50,2.0,Taker,trade
```

## 🏗️ Project Structure

```
TradeAnalysis/
├── trade_analyzer/              # Core analysis package
│   ├── __init__.py             # Package initialization
│   ├── data_processor.py       # Data processing module
│   ├── analyzer.py             # Analysis calculation module
│   └── visualizer.py           # Visualization module
├── app.py                      # Streamlit web application
├── example_analysis.py         # Command line example script
├── requirements.txt            # Dependency list
├── README.md                  # Project documentation (English)
├── README_CN.md               # Project documentation (Chinese)
└── lighter-trade-export-*.csv  # Example data files
```

## 📊 Analysis Metrics

### P&L Metrics
- **Total P&L**: Sum of all trade P&L
- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Ratio of average profit to average loss
- **Sharpe Ratio**: Risk-adjusted return metric

### Risk Metrics
- **Maximum Drawdown**: Maximum loss from historical peak to trough
- **VaR (Value at Risk)**: Maximum potential loss at a given confidence level
- **CVaR (Conditional VaR)**: Average loss exceeding VaR threshold

### Trading Frequency Metrics
- **Daily Trading Frequency**: Average daily trading frequency
- **Most Active Periods**: Time periods with highest trading frequency
- **Trading Distribution**: Trading distribution by time dimension

## 🎯 Use Cases

### Individual Traders
- Analyze personal trading records
- Evaluate trading strategy effectiveness
- Identify trading habits and patterns
- Risk management and control

### Strategy Development
- Backtest trading strategies
- Compare different strategy performance
- Optimize trading parameters
- Risk-return analysis

### Investment Institutions
- Trader performance evaluation
- Risk monitoring and management
- Compliance report generation
- Portfolio analysis

## 🛠️ Custom Extensions

### Adding New Analysis Metrics

```python
class CustomAnalyzer(TradeAnalyzer):
    def calculate_custom_metric(self):
        # Your custom calculation logic
        return custom_result
```

### Custom Visualization

```python
class CustomVisualizer(TradeVisualizer):
    def plot_custom_chart(self):
        # Your custom chart logic
        return fig
```

## 📈 Performance Optimization

- For large datasets (>1M records), use data filtering features
- Choose static charts for faster chart generation
- Optimize multi-file analysis through parallel processing

## 🤝 Contributing

Welcome to submit Issues and Pull Requests!

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🆘 FAQ

### Q: What data formats are supported?
A: Currently supports CSV and Excel (.xlsx, .xls) formats.

### Q: How to handle missing columns?
A: The framework automatically handles missing columns, only Date and Closed PnL are required.

### Q: Can I analyze trading data other than cryptocurrencies?
A: Yes, the framework supports any type of trading data (stocks, futures, forex, etc.).

### Q: How to customize analysis metrics?
A: You can inherit from the TradeAnalyzer class and add your own analysis methods.

### Q: Can generated charts be saved?
A: Yes, supports saving as PNG format or using interactive charts.

## 📞 Support

If you encounter issues during use:

1. Check project Issues
2. Submit a new Issue describing the problem
3. Check example code and documentation

---

**🚀 Start your trading data analysis journey!** 