"""
交易分析模块
负责各种交易绩效分析
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

class TradeAnalyzer:
    """交易分析器"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.logger = logging.getLogger(__name__)
        
    def calculate_pnl_statistics(self) -> Dict:
        """计算盈亏统计"""
        if 'closed_pnl' not in self.data.columns:
            return {"error": "没有盈亏数据"}
        
        pnl_data = self.data['closed_pnl'].dropna()
        
        if len(pnl_data) == 0:
            return {"error": "没有有效的盈亏数据"}
        
        stats = {
            "总盈亏": pnl_data.sum(),
            "平均盈亏": pnl_data.mean(),
            "盈亏标准差": pnl_data.std(),
            "最大单笔盈利": pnl_data.max(),
            "最大单笔亏损": pnl_data.min(),
            "盈利交易数": (pnl_data > 0).sum(),
            "亏损交易数": (pnl_data < 0).sum(),
            "平局交易数": (pnl_data == 0).sum(),
            "总交易数": len(pnl_data),
            "胜率": (pnl_data > 0).mean() * 100,  # 百分比
            "平均盈利": pnl_data[pnl_data > 0].mean() if (pnl_data > 0).any() else 0,
            "平均亏损": pnl_data[pnl_data < 0].mean() if (pnl_data < 0).any() else 0,
        }
        
        # 计算盈亏比
        if stats["平均亏损"] != 0:
            stats["盈亏比"] = abs(stats["平均盈利"] / stats["平均亏损"])
        else:
            stats["盈亏比"] = float('inf') if stats["平均盈利"] > 0 else 0
        
        return stats
    
    def calculate_drawdown(self) -> Dict:
        """计算回撤分析"""
        if 'cumulative_pnl' not in self.data.columns:
            return {"error": "没有累积盈亏数据"}
        
        cumulative_pnl = self.data['cumulative_pnl'].dropna()
        
        if len(cumulative_pnl) == 0:
            return {"error": "没有有效的累积盈亏数据"}
        
        # 计算累积最高点
        running_max = cumulative_pnl.expanding().max()
        
        # 计算回撤
        drawdown = cumulative_pnl - running_max
        drawdown_pct = (drawdown / running_max.replace(0, np.nan)) * 100
        
        stats = {
            "最大回撤金额": drawdown.min(),
            "最大回撤百分比": drawdown_pct.min(),
            "当前回撤": drawdown.iloc[-1],
            "当前回撤百分比": drawdown_pct.iloc[-1],
            "最高净值": running_max.max(),
            "当前净值": cumulative_pnl.iloc[-1],
            "回撤期数": len(drawdown[drawdown < 0]),
            "最长回撤期": self._calculate_longest_drawdown_period(drawdown)
        }
        
        return stats
    
    def _calculate_longest_drawdown_period(self, drawdown: pd.Series) -> int:
        """计算最长回撤期"""
        in_drawdown = False
        current_period = 0
        max_period = 0
        
        for dd in drawdown:
            if dd < 0:
                if not in_drawdown:
                    in_drawdown = True
                    current_period = 1
                else:
                    current_period += 1
            else:
                if in_drawdown:
                    max_period = max(max_period, current_period)
                    in_drawdown = False
                    current_period = 0
        
        # 处理最后还在回撤的情况
        if in_drawdown:
            max_period = max(max_period, current_period)
        
        return max_period
    
    def analyze_trading_frequency(self) -> Dict:
        """分析交易频率"""
        if 'date' not in self.data.columns:
            return {"error": "没有日期数据"}
        
        dates = self.data['date'].dt.date
        
        # 按日统计
        daily_trades = dates.value_counts().sort_index()
        
        # 按小时统计
        if 'hour' in self.data.columns:
            hourly_trades = self.data['hour'].value_counts().sort_index()
        else:
            hourly_trades = self.data['date'].dt.hour.value_counts().sort_index()
        
        # 按星期统计
        if 'day_of_week' in self.data.columns:
            weekly_trades = self.data['day_of_week'].value_counts()
        else:
            weekly_trades = self.data['date'].dt.day_name().value_counts()
        
        stats = {
            "总交易天数": len(daily_trades),
            "平均每日交易次数": daily_trades.mean(),
            "最高单日交易次数": daily_trades.max(),
            "每小时交易分布": hourly_trades.to_dict(),
            "每周交易分布": weekly_trades.to_dict(),
            "最活跃交易时间": hourly_trades.idxmax(),
            "最活跃交易日": weekly_trades.idxmax()
        }
        
        return stats
    
    def analyze_position_changes(self) -> Dict:
        """分析持仓变化"""
        if 'position_change' not in self.data.columns:
            return {"error": "没有持仓变化数据"}
        
        position_counts = self.data['position_change'].value_counts()
        
        stats = {
            "持仓变化分布": position_counts.to_dict(),
            "总操作次数": len(self.data),
            "做多操作": position_counts.get('Long', 0) + position_counts.get('Short_to_Long', 0),
            "做空操作": position_counts.get('Short', 0) + position_counts.get('Long_to_Short', 0),
            "方向转换次数": position_counts.get('Short_to_Long', 0) + position_counts.get('Long_to_Short', 0)
        }
        
        return stats
    
    def calculate_risk_metrics(self) -> Dict:
        """计算风险指标"""
        if 'closed_pnl' not in self.data.columns:
            return {"error": "没有盈亏数据"}
        
        pnl_data = self.data['closed_pnl'].dropna()
        
        if len(pnl_data) == 0:
            return {"error": "没有有效的盈亏数据"}
        
        # 假设无风险利率为3%（年化）
        risk_free_rate = 0.03
        
        # 计算期间
        if 'date' in self.data.columns:
            start_date = self.data['date'].min()
            end_date = self.data['date'].max()
            days = (end_date - start_date).days
            years = days / 365.25
        else:
            years = 1  # 默认1年
        
        # 年化收益率
        total_return = pnl_data.sum()
        annualized_return = (total_return / years) if years > 0 else 0
        
        # 年化波动率
        daily_returns = pnl_data
        annualized_volatility = daily_returns.std() * np.sqrt(365.25)
        
        # 夏普比率
        sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility if annualized_volatility != 0 else 0
        
        # Calmar比率（年化收益率/最大回撤）
        drawdown_stats = self.calculate_drawdown()
        max_drawdown = abs(drawdown_stats.get("最大回撤金额", 1))
        calmar_ratio = annualized_return / max_drawdown if max_drawdown != 0 else 0
        
        # VaR (Value at Risk) - 95%置信度
        var_95 = np.percentile(pnl_data, 5)
        
        # CVaR (Conditional VaR) - 95%置信度的条件风险价值
        cvar_95 = pnl_data[pnl_data <= var_95].mean()
        
        stats = {
            "年化收益率": annualized_return,
            "年化波动率": annualized_volatility,
            "夏普比率": sharpe_ratio,
            "Calmar比率": calmar_ratio,
            "VaR_95%": var_95,
            "CVaR_95%": cvar_95,
            "分析期间_天数": days if 'date' in self.data.columns else "N/A",
            "分析期间_年数": years
        }
        
        return stats
    
    def analyze_trade_sizes(self) -> Dict:
        """分析交易规模"""
        if 'size' not in self.data.columns and 'trade_value' not in self.data.columns:
            return {"error": "没有交易规模数据"}
        
        stats = {}
        
        # 分析交易数量
        if 'size' in self.data.columns:
            size_data = self.data['size'].dropna()
            stats.update({
                "平均交易数量": size_data.mean(),
                "交易数量标准差": size_data.std(),
                "最大交易数量": size_data.max(),
                "最小交易数量": size_data.min(),
                "交易数量中位数": size_data.median()
            })
        
        # 分析交易价值
        if 'trade_value' in self.data.columns:
            value_data = self.data['trade_value'].dropna()
            stats.update({
                "平均交易价值": value_data.mean(),
                "交易价值标准差": value_data.std(),
                "最大交易价值": value_data.max(),
                "最小交易价值": value_data.min(),
                "交易价值中位数": value_data.median(),
                "总交易价值": value_data.sum()
            })
        
        return stats
    
    def generate_performance_report(self) -> Dict:
        """生成综合绩效报告"""
        report = {
            "报告生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "数据概览": {
                "总交易数": len(self.data),
                "数据时间范围": f"{self.data['date'].min()} 至 {self.data['date'].max()}" if 'date' in self.data.columns else "N/A"
            },
            "盈亏分析": self.calculate_pnl_statistics(),
            "回撤分析": self.calculate_drawdown(),
            "交易频率分析": self.analyze_trading_frequency(),
            "持仓分析": self.analyze_position_changes(),
            "风险指标": self.calculate_risk_metrics(),
            "交易规模分析": self.analyze_trade_sizes()
        }
        
        return report
    
    def find_best_worst_trades(self, top_n: int = 10) -> Dict:
        """找出最佳和最差交易"""
        if 'closed_pnl' not in self.data.columns:
            return {"error": "没有盈亏数据"}
        
        # 最佳交易
        best_trades = self.data.nlargest(top_n, 'closed_pnl')[['date', 'side', 'closed_pnl', 'size', 'price']].to_dict('records')
        
        # 最差交易
        worst_trades = self.data.nsmallest(top_n, 'closed_pnl')[['date', 'side', 'closed_pnl', 'size', 'price']].to_dict('records')
        
        return {
            "最佳交易": best_trades,
            "最差交易": worst_trades
        }
    
    def calculate_monthly_performance(self) -> pd.DataFrame:
        """计算月度绩效"""
        if 'date' not in self.data.columns or 'closed_pnl' not in self.data.columns:
            return pd.DataFrame()
        
        # 按月分组
        monthly_data = self.data.groupby(self.data['date'].dt.to_period('M')).agg({
            'closed_pnl': ['sum', 'count', 'mean'],
            'trade_value': 'sum' if 'trade_value' in self.data.columns else lambda x: 0
        }).round(4)
        
        # 计算累积盈亏
        monthly_data[('cumulative', 'pnl')] = monthly_data[('closed_pnl', 'sum')].cumsum()
        
        return monthly_data 