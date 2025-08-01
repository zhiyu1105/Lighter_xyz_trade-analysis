"""
Trading Analysis Module
Responsible for various trading performance analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

class TradeAnalyzer:
    """Trading Analyzer"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.logger = logging.getLogger(__name__)
        
    def calculate_pnl_statistics(self) -> Dict:
        """Calculate P&L statistics"""
        if 'closed_pnl' not in self.data.columns:
            return {"error": "No P&L data available"}
        
        pnl_data = self.data['closed_pnl'].dropna()
        
        if len(pnl_data) == 0:
            return {"error": "No valid P&L data available"}
        
        stats = {
            "total_pnl": pnl_data.sum(),
            "average_pnl": pnl_data.mean(),
            "pnl_std": pnl_data.std(),
            "max_profit": pnl_data.max(),
            "max_loss": pnl_data.min(),
            "winning_trades": (pnl_data > 0).sum(),
            "losing_trades": (pnl_data < 0).sum(),
            "breakeven_trades": (pnl_data == 0).sum(),
            "total_trades": len(pnl_data),
            "win_rate": (pnl_data > 0).mean() * 100,  # Percentage
            "average_win": pnl_data[pnl_data > 0].mean() if (pnl_data > 0).any() else 0,
            "average_loss": pnl_data[pnl_data < 0].mean() if (pnl_data < 0).any() else 0,
        }
        
        # Calculate profit factor
        if stats["average_loss"] != 0:
            stats["profit_factor"] = abs(stats["average_win"] / stats["average_loss"])
        else:
            stats["profit_factor"] = float('inf') if stats["average_win"] > 0 else 0
        
        return stats
    
    def calculate_drawdown(self) -> Dict:
        """Calculate drawdown analysis"""
        if 'cumulative_pnl' not in self.data.columns:
            return {"error": "No cumulative P&L data available"}
        
        cumulative_pnl = self.data['cumulative_pnl'].dropna()
        
        if len(cumulative_pnl) == 0:
            return {"error": "No valid cumulative P&L data available"}
        
        # Calculate cumulative peak
        running_max = cumulative_pnl.expanding().max()
        
        # Calculate drawdown
        drawdown = cumulative_pnl - running_max
        drawdown_pct = (drawdown / running_max.replace(0, np.nan)) * 100
        
        stats = {
            "max_drawdown_amount": drawdown.min(),
            "max_drawdown_percentage": drawdown_pct.min(),
            "current_drawdown": drawdown.iloc[-1],
            "current_drawdown_percentage": drawdown_pct.iloc[-1],
            "peak_value": running_max.max(),
            "current_value": cumulative_pnl.iloc[-1],
            "drawdown_periods": len(drawdown[drawdown < 0]),
            "longest_drawdown_period": self._calculate_longest_drawdown_period(drawdown)
        }
        
        return stats
    
    def _calculate_longest_drawdown_period(self, drawdown: pd.Series) -> int:
        """Calculate longest drawdown period"""
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
        
        # Handle case where still in drawdown at the end
        if in_drawdown:
            max_period = max(max_period, current_period)
        
        return max_period
    
    def analyze_trading_frequency(self) -> Dict:
        """Analyze trading frequency"""
        if 'date' not in self.data.columns:
            return {"error": "No date data available"}
        
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
            "total_trading_days": len(daily_trades),
            "average_daily_trades": daily_trades.mean(),
            "max_daily_trades": daily_trades.max(),
            "hourly_trade_distribution": hourly_trades.to_dict(),
            "weekly_trade_distribution": weekly_trades.to_dict(),
            "most_active_hour": hourly_trades.idxmax(),
            "most_active_day": weekly_trades.idxmax()
        }
        
        return stats
    
    def analyze_position_changes(self) -> Dict:
        """Analyze position changes"""
        if 'position_change' not in self.data.columns:
            return {"error": "No position change data available"}
        
        position_counts = self.data['position_change'].value_counts()
        
        stats = {
            "position_change_distribution": position_counts.to_dict(),
            "total_operations": len(self.data),
            "long_operations": position_counts.get('Long', 0) + position_counts.get('Short_to_Long', 0),
            "short_operations": position_counts.get('Short', 0) + position_counts.get('Long_to_Short', 0),
            "direction_changes": position_counts.get('Short_to_Long', 0) + position_counts.get('Long_to_Short', 0)
        }
        
        return stats
    
    def calculate_risk_metrics(self) -> Dict:
        """Calculate risk metrics"""
        if 'closed_pnl' not in self.data.columns:
            return {"error": "No P&L data available"}
        
        pnl_data = self.data['closed_pnl'].dropna()
        
        if len(pnl_data) == 0:
            return {"error": "No valid P&L data available"}
        
        # Assume risk-free rate of 3% (annualized)
        risk_free_rate = 0.03
        
        # Calculate period
        if 'date' in self.data.columns:
            start_date = self.data['date'].min()
            end_date = self.data['date'].max()
            days = (end_date - start_date).days
            years = days / 365.25
        else:
            years = 1  # Default 1 year
        
        # Annualized return
        total_return = pnl_data.sum()
        annualized_return = (total_return / years) if years > 0 else 0
        
        # Annualized volatility
        daily_returns = pnl_data
        annualized_volatility = daily_returns.std() * np.sqrt(365.25)
        
        # Sharpe ratio
        sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility if annualized_volatility != 0 else 0
        
        # Calmar ratio (annualized return / max drawdown)
        drawdown_stats = self.calculate_drawdown()
        max_drawdown = abs(drawdown_stats.get("max_drawdown_amount", 1))
        calmar_ratio = annualized_return / max_drawdown if max_drawdown != 0 else 0
        
        # VaR (Value at Risk) - 95% confidence
        var_95 = np.percentile(pnl_data, 5)
        
        # CVaR (Conditional VaR) - 95% confidence conditional risk value
        cvar_95 = pnl_data[pnl_data <= var_95].mean()
        
        stats = {
            "annualized_return": annualized_return,
            "annualized_volatility": annualized_volatility,
            "sharpe_ratio": sharpe_ratio,
            "calmar_ratio": calmar_ratio,
            "var_95_percent": var_95,
            "cvar_95_percent": cvar_95,
            "analysis_period_days": days if 'date' in self.data.columns else "N/A",
            "analysis_period_years": years
        }
        
        return stats
    
    def analyze_trade_sizes(self) -> Dict:
        """Analyze trade sizes"""
        if 'size' not in self.data.columns and 'trade_value' not in self.data.columns:
            return {"error": "No trade size data available"}
        
        stats = {}
        
        # Analyze trade quantities
        if 'size' in self.data.columns:
            size_data = self.data['size'].dropna()
            stats.update({
                "average_trade_size": size_data.mean(),
                "trade_size_std": size_data.std(),
                "max_trade_size": size_data.max(),
                "min_trade_size": size_data.min(),
                "trade_size_median": size_data.median()
            })
        
        # Analyze trade values
        if 'trade_value' in self.data.columns:
            value_data = self.data['trade_value'].dropna()
            stats.update({
                "average_trade_value": value_data.mean(),
                "trade_value_std": value_data.std(),
                "max_trade_value": value_data.max(),
                "min_trade_value": value_data.min(),
                "trade_value_median": value_data.median(),
                "total_trade_value": value_data.sum()
            })
        
        return stats
    
    def generate_performance_report(self) -> Dict:
        """Generate comprehensive performance report"""
        report = {
            "report_generation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Data Overview": {
                "total_trades": len(self.data),
                "data_time_range": f"{self.data['date'].min()} to {self.data['date'].max()}" if 'date' in self.data.columns else "N/A"
            },
            "P&L Analysis": self.calculate_pnl_statistics(),
            "Drawdown Analysis": self.calculate_drawdown(),
            "Trading Frequency Analysis": self.analyze_trading_frequency(),
            "Position Analysis": self.analyze_position_changes(),
            "Risk Metrics": self.calculate_risk_metrics(),
            "Trade Size Analysis": self.analyze_trade_sizes()
        }
        
        return report
    
    def find_best_worst_trades(self, top_n: int = 10) -> Dict:
        """Find best and worst trades"""
        if 'closed_pnl' not in self.data.columns:
            return {"error": "No P&L data available"}
        
        # Best trades
        best_trades = self.data.nlargest(top_n, 'closed_pnl')[['date', 'side', 'closed_pnl', 'size', 'price']].to_dict('records')
        
        # Worst trades
        worst_trades = self.data.nsmallest(top_n, 'closed_pnl')[['date', 'side', 'closed_pnl', 'size', 'price']].to_dict('records')
        
        return {
            "best_trades": best_trades,
            "worst_trades": worst_trades
        }
    
    def calculate_monthly_performance(self) -> pd.DataFrame:
        """Calculate monthly performance"""
        if 'date' not in self.data.columns or 'closed_pnl' not in self.data.columns:
            return pd.DataFrame()
        
        # Group by month
        monthly_data = self.data.groupby(self.data['date'].dt.to_period('M')).agg({
            'closed_pnl': ['sum', 'count', 'mean'],
            'trade_value': 'sum' if 'trade_value' in self.data.columns else lambda x: 0
        }).round(4)
        
        # Calculate cumulative P&L
        monthly_data[('cumulative', 'pnl')] = monthly_data[('closed_pnl', 'sum')].cumsum()
        
        return monthly_data 