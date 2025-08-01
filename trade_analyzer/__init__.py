"""
交易数据分析框架
Trade Data Analysis Framework

主要功能：
- 交易数据导入和清洗
- 交易绩效分析
- 数据可视化
- 报告生成
"""

__version__ = "1.0.0"
__author__ = "Trade Analyzer Team"

from .data_processor import TradeDataProcessor
from .analyzer import TradeAnalyzer
from .visualizer import TradeVisualizer

__all__ = ['TradeDataProcessor', 'TradeAnalyzer', 'TradeVisualizer'] 