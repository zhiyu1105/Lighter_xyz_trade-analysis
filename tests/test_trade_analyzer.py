"""
交易分析器测试模块
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 导入被测试的模块
try:
    from trade_analyzer.data_processor import TradeDataProcessor
    from trade_analyzer.analyzer import TradeAnalyzer
    from trade_analyzer.visualizer import TradeVisualizer
except ImportError:
    # 如果模块不存在，跳过测试
    pytest.skip("trade_analyzer module not available", allow_module_level=True)


class TestTradeDataProcessor:
    """测试数据处理模块"""
    
    def setup_method(self):
        """设置测试数据"""
        self.sample_data = pd.DataFrame({
            'Date': [
                '2025-01-01 10:00:00',
                '2025-01-01 11:00:00',
                '2025-01-01 12:00:00',
                '2025-01-01 13:00:00',
                '2025-01-01 14:00:00'
            ],
            'Closed PnL': [10.5, -5.2, 15.8, -8.1, 12.3],
            'Market': ['BTC', 'BTC', 'ETH', 'ETH', 'BTC'],
            'Side': ['Long', 'Short', 'Long', 'Short', 'Long'],
            'Trade Value': [1000, 800, 1200, 900, 1100],
            'Size': [0.001, 0.001, 0.002, 0.002, 0.001],
            'Price': [50000, 48000, 3000, 2900, 52000],
            'Fee': [2.0, 2.0, 1.5, 1.5, 2.0]
        })
    
    def test_data_processor_initialization(self):
        """测试数据处理器初始化"""
        processor = TradeDataProcessor()
        assert processor is not None
    
    def test_data_cleaning(self):
        """测试数据清洗功能"""
        processor = TradeDataProcessor()
        # 使用 _standardize_data 方法（内部方法）
        cleaned_data = processor._standardize_data(self.sample_data)
        
        # 检查数据类型
        assert isinstance(cleaned_data, pd.DataFrame)
        assert 'date' in cleaned_data.columns  # 标准化后列名变为小写
        assert 'closed_pnl' in cleaned_data.columns
        
        # 检查日期格式
        assert pd.api.types.is_datetime64_any_dtype(cleaned_data['date'])
        
        # 检查数值类型
        assert pd.api.types.is_numeric_dtype(cleaned_data['closed_pnl'])


class TestTradeAnalyzer:
    """测试分析模块"""
    
    def setup_method(self):
        """设置测试数据"""
        self.sample_data = pd.DataFrame({
            'Date': pd.date_range('2025-01-01', periods=100, freq='h'),
            'Closed PnL': np.random.normal(10, 20, 100),
            'Market': ['BTC'] * 100,
            'Side': np.random.choice(['Long', 'Short'], 100),
            'Trade Value': np.random.uniform(500, 2000, 100),
            'Size': np.random.uniform(0.001, 0.01, 100),
            'Price': np.random.uniform(40000, 60000, 100),
            'Fee': np.random.uniform(1, 5, 100)
        })
        
        # 确保有正负盈亏
        self.sample_data.loc[0:49, 'Closed PnL'] = np.random.uniform(5, 50, 50)
        self.sample_data.loc[50:99, 'Closed PnL'] = np.random.uniform(-50, -5, 50)
    
    def test_analyzer_initialization(self):
        """测试分析器初始化"""
        analyzer = TradeAnalyzer(self.sample_data)
        assert analyzer is not None
        assert len(analyzer.data) == 100
    
    def test_pnl_statistics(self):
        """测试盈亏统计"""
        # 先标准化数据
        processor = TradeDataProcessor()
        standardized_data = processor._standardize_data(self.sample_data)
        analyzer = TradeAnalyzer(standardized_data)
        stats = analyzer.calculate_pnl_statistics()
        
        # 检查返回的统计信息（使用中文键名）
        assert '总盈亏' in stats
        assert '胜率' in stats
        assert '盈亏比' in stats
        assert '最大单笔盈利' in stats
        assert '最大单笔亏损' in stats
        
        # 检查数据类型
        assert isinstance(stats['总盈亏'], (int, float))
        assert isinstance(stats['胜率'], (int, float))
        assert 0 <= stats['胜率'] <= 100
    
    def test_risk_metrics(self):
        """测试风险指标"""
        # 先标准化数据
        processor = TradeDataProcessor()
        standardized_data = processor._standardize_data(self.sample_data)
        analyzer = TradeAnalyzer(standardized_data)
        risk_metrics = analyzer.calculate_risk_metrics()
        
        # 检查风险指标（使用中文键名）
        assert '夏普比率' in risk_metrics
        assert '最大回撤' in risk_metrics
        assert 'VaR_95' in risk_metrics
        assert 'CVaR_95' in risk_metrics
        
        # 检查数据类型
        assert isinstance(risk_metrics['夏普比率'], (int, float))
        assert isinstance(risk_metrics['最大回撤'], (int, float))


class TestTradeVisualizer:
    """测试可视化模块"""
    
    def setup_method(self):
        """设置测试数据"""
        self.sample_data = pd.DataFrame({
            'Date': pd.date_range('2025-01-01', periods=50, freq='h'),
            'Closed PnL': np.random.normal(10, 15, 50),
            'Market': ['BTC'] * 50,
            'Side': np.random.choice(['Long', 'Short'], 50),
            'Trade Value': np.random.uniform(500, 2000, 50),
            'Size': np.random.uniform(0.001, 0.01, 50),
            'Price': np.random.uniform(40000, 60000, 50),
            'Fee': np.random.uniform(1, 5, 50)
        })
    
    def test_visualizer_initialization(self):
        """测试可视化器初始化"""
        visualizer = TradeVisualizer(self.sample_data)
        assert visualizer is not None
        assert len(visualizer.data) == 50
    
    def test_plot_pnl_curve(self):
        """测试盈亏曲线图"""
        # 添加累积盈亏列
        test_data = self.sample_data.copy()
        test_data['cumulative_pnl'] = test_data['Closed PnL'].cumsum()
        
        visualizer = TradeVisualizer(test_data)
        fig = visualizer.plot_pnl_curve()
        
        # 检查返回的图表对象
        assert fig is not None
        # 这里可以添加更多具体的图表检查


def test_integration():
    """集成测试"""
    # 创建测试数据
    test_data = pd.DataFrame({
        'Date': pd.date_range('2025-01-01', periods=20, freq='h'),
        'Closed PnL': [10, -5, 15, -8, 12, -3, 20, -10, 8, -6,
                       15, -7, 12, -4, 18, -9, 11, -5, 14, -8],
        'Market': ['BTC'] * 20,
        'Side': ['Long', 'Short'] * 10,
        'Trade Value': np.random.uniform(500, 2000, 20),
        'Size': np.random.uniform(0.001, 0.01, 20),
        'Price': np.random.uniform(40000, 60000, 20),
        'Fee': np.random.uniform(1, 5, 20)
    })
    
    # 测试完整流程
    try:
        # 数据处理
        processor = TradeDataProcessor()
        cleaned_data = processor._standardize_data(test_data)
        
        # 数据分析
        analyzer = TradeAnalyzer(cleaned_data)
        pnl_stats = analyzer.calculate_pnl_statistics()
        risk_metrics = analyzer.calculate_risk_metrics()
        
        # 数据可视化（添加累积盈亏列）
        viz_data = cleaned_data.copy()
        viz_data['cumulative_pnl'] = cleaned_data['closed_pnl'].cumsum()
        visualizer = TradeVisualizer(viz_data)
        fig = visualizer.plot_pnl_curve()
        
        # 基本断言
        assert len(cleaned_data) == 20
        assert '总盈亏' in pnl_stats
        assert '夏普比率' in risk_metrics
        assert fig is not None
        
    except Exception as e:
        pytest.fail(f"集成测试失败: {e}")


if __name__ == "__main__":
    pytest.main([__file__]) 