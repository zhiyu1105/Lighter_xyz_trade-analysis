"""
Trading Data Visualization Module
Responsible for generating various charts and visualization analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Tuple
import logging

# Set font (only in non-testing environment)
import os
if not os.environ.get('TESTING'):
    try:
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    except:
        # If font setting fails, use default font
        pass

class TradeVisualizer:
    """Trading Data Visualizer"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.logger = logging.getLogger(__name__)
        
        # Set plotting style
        sns.set_style("whitegrid")
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def plot_pnl_curve(self, save_path: Optional[str] = None, interactive: bool = False):
        """Plot P&L curve"""
        if 'cumulative_pnl' not in self.data.columns:
            self.logger.error("No cumulative P&L data available")
            return None
        
        if interactive:
            return self._plot_pnl_curve_plotly()
        else:
            return self._plot_pnl_curve_matplotlib(save_path)
    
    def _plot_pnl_curve_matplotlib(self, save_path: Optional[str] = None):
        """Plot P&L curve using matplotlib"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Cumulative P&L curve
        if 'date' in self.data.columns:
            ax1.plot(self.data['date'], self.data['cumulative_pnl'], linewidth=2, color='blue')
            ax1.set_xlabel('Date')
        else:
            ax1.plot(self.data.index, self.data['cumulative_pnl'], linewidth=2, color='blue')
            ax1.set_xlabel('Trade Sequence')
        
        ax1.set_ylabel('Cumulative P&L')
        ax1.set_title('Cumulative P&L Curve', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Drawdown chart
        if 'cumulative_pnl' in self.data.columns:
            running_max = self.data['cumulative_pnl'].expanding().max()
            drawdown = self.data['cumulative_pnl'] - running_max
            
            if 'date' in self.data.columns:
                ax2.fill_between(self.data['date'], drawdown, 0, alpha=0.3, color='red')
                ax2.plot(self.data['date'], drawdown, color='red', linewidth=1)
                ax2.set_xlabel('Date')
            else:
                ax2.fill_between(self.data.index, drawdown, 0, alpha=0.3, color='red')
                ax2.plot(self.data.index, drawdown, color='red', linewidth=1)
                ax2.set_xlabel('Trade Sequence')
            
            ax2.set_ylabel('Drawdown')
            ax2.set_title('Drawdown Chart', fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Chart saved to: {save_path}")
        
        return fig
    
    def _plot_pnl_curve_plotly(self):
        """Plot interactive P&L curve using plotly"""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Cumulative P&L Curve', 'Drawdown Chart'),
            vertical_spacing=0.08
        )
        
        # Prepare x-axis data
        x_data = self.data['date'] if 'date' in self.data.columns else self.data.index
        
        # Cumulative P&L curve
        fig.add_trace(
            go.Scatter(
                x=x_data,
                y=self.data['cumulative_pnl'],
                mode='lines',
                name='Cumulative P&L',
                line=dict(color='blue', width=2)
            ),
            row=1, col=1
        )
        
        # Drawdown chart
        if 'cumulative_pnl' in self.data.columns:
            running_max = self.data['cumulative_pnl'].expanding().max()
            drawdown = self.data['cumulative_pnl'] - running_max
            
            fig.add_trace(
                go.Scatter(
                    x=x_data,
                    y=drawdown,
                    mode='lines',
                    name='Drawdown',
                    fill='tonexty',
                    line=dict(color='red', width=1),
                    fillcolor='rgba(255,0,0,0.3)'
                ),
                row=2, col=1
            )
        
        fig.update_layout(
            title='Trading P&L Analysis',
            height=700,
            showlegend=True
        )
        
        return fig
    
    def plot_price_chart(self, save_path: Optional[str] = None, interactive: bool = False):
        """Plot price trend chart"""
        if 'price' not in self.data.columns:
            self.logger.error("No price data available")
            return None
        
        if interactive:
            return self._plot_price_chart_plotly()
        else:
            return self._plot_price_chart_matplotlib(save_path)
    
    def _plot_price_chart_matplotlib(self, save_path: Optional[str] = None):
        """Plot price trend chart using matplotlib"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x_data = self.data['date'] if 'date' in self.data.columns else self.data.index
        
        # Price curve
        ax.plot(x_data, self.data['price'], linewidth=1, color='black', alpha=0.7, label='Price')
        
        # Moving average
        if 'price_ma_10' in self.data.columns:
            ax.plot(x_data, self.data['price_ma_10'], linewidth=2, color='orange', label='10-period MA')
        
        # Mark trade points
        if 'trade_type' in self.data.columns:
            open_trades = self.data[self.data['trade_type'] == 'Open']
            close_trades = self.data[self.data['trade_type'] == 'Close']
            
            if len(open_trades) > 0:
                open_x = open_trades['date'] if 'date' in self.data.columns else open_trades.index
                ax.scatter(open_x, open_trades['price'], color='green', marker='^', s=50, label='Open', alpha=0.8)
            
            if len(close_trades) > 0:
                close_x = close_trades['date'] if 'date' in self.data.columns else close_trades.index
                ax.scatter(close_x, close_trades['price'], color='red', marker='v', s=50, label='Close', alpha=0.8)
        
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
        ax.set_title('Price Trend with Trade Points', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Chart saved to: {save_path}")
        
        return fig
    
    def _plot_price_chart_plotly(self):
        """使用plotly绘制交互式价格走势图"""
        fig = go.Figure()
        
        x_data = self.data['date'] if 'date' in self.data.columns else self.data.index
        
        # 价格曲线
        fig.add_trace(go.Scatter(
            x=x_data,
            y=self.data['price'],
            mode='lines',
            name='价格',
            line=dict(color='black', width=1)
        ))
        
        # 移动平均线
        if 'price_ma_10' in self.data.columns:
            fig.add_trace(go.Scatter(
                x=x_data,
                y=self.data['price_ma_10'],
                mode='lines',
                name='10期移动平均',
                line=dict(color='orange', width=2)
            ))
        
        # 标记交易点
        if 'trade_type' in self.data.columns:
            open_trades = self.data[self.data['trade_type'] == 'Open']
            close_trades = self.data[self.data['trade_type'] == 'Close']
            
            if len(open_trades) > 0:
                open_x = open_trades['date'] if 'date' in self.data.columns else open_trades.index
                fig.add_trace(go.Scatter(
                    x=open_x,
                    y=open_trades['price'],
                    mode='markers',
                    name='开仓',
                    marker=dict(color='green', symbol='triangle-up', size=8)
                ))
            
            if len(close_trades) > 0:
                close_x = close_trades['date'] if 'date' in self.data.columns else close_trades.index
                fig.add_trace(go.Scatter(
                    x=close_x,
                    y=close_trades['price'],
                    mode='markers',
                    name='平仓',
                    marker=dict(color='red', symbol='triangle-down', size=8)
                ))
        
        fig.update_layout(
            title='价格走势与交易点',
            xaxis_title='时间',
            yaxis_title='价格',
            height=600
        )
        
        return fig
    
    def plot_pnl_distribution(self, save_path: Optional[str] = None):
        """Plot P&L distribution chart"""
        if 'closed_pnl' not in self.data.columns:
            self.logger.error("No P&L data available")
            return None
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        pnl_data = self.data['closed_pnl'].dropna()
        
        # P&L histogram
        ax1.hist(pnl_data, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.axvline(pnl_data.mean(), color='red', linestyle='--', label=f'Mean: {pnl_data.mean():.4f}')
        ax1.axvline(pnl_data.median(), color='green', linestyle='--', label=f'Median: {pnl_data.median():.4f}')
        ax1.set_xlabel('P&L')
        ax1.set_ylabel('Frequency')
        ax1.set_title('P&L Distribution Histogram')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # P&L box plot
        ax2.boxplot(pnl_data, vert=True)
        ax2.set_ylabel('P&L')
        ax2.set_title('P&L Box Plot')
        ax2.grid(True, alpha=0.3)
        
        # Cumulative P&L by time distribution
        if 'hour' in self.data.columns:
            hourly_pnl = self.data.groupby('hour')['closed_pnl'].sum()
            ax3.bar(hourly_pnl.index, hourly_pnl.values, alpha=0.7, color='lightcoral')
            ax3.set_xlabel('Hour')
            ax3.set_ylabel('Cumulative P&L')
            ax3.set_title('Cumulative P&L by Hour')
            ax3.grid(True, alpha=0.3)
        
        # Win/Loss trade comparison
        win_trades = pnl_data[pnl_data > 0]
        loss_trades = pnl_data[pnl_data < 0]
        
        categories = ['Profit Trades', 'Loss Trades']
        values = [len(win_trades), len(loss_trades)]
        colors = ['green', 'red']
        
        ax4.pie(values, labels=categories, colors=colors, autopct='%1.1f%%', startangle=90)
        ax4.set_title('Win/Loss Trade Ratio')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Chart saved to: {save_path}")
        
        return fig
    
    def plot_trading_frequency(self, save_path: Optional[str] = None):
        """Plot trading frequency analysis chart"""
        if 'date' not in self.data.columns:
            self.logger.error("No date data available")
            return None
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # By hour distribution
        if 'hour' in self.data.columns:
            hourly_counts = self.data['hour'].value_counts().sort_index()
        else:
            hourly_counts = self.data['date'].dt.hour.value_counts().sort_index()
        
        ax1.bar(hourly_counts.index, hourly_counts.values, alpha=0.7, color='skyblue')
        ax1.set_xlabel('Hour')
        ax1.set_ylabel('Trade Count')
        ax1.set_title('Trading Frequency by Hour')
        ax1.grid(True, alpha=0.3)
        
        # By week distribution
        if 'day_of_week' in self.data.columns:
            weekly_counts = self.data['day_of_week'].value_counts()
        else:
            weekly_counts = self.data['date'].dt.day_name().value_counts()
        
        ax2.bar(weekly_counts.index, weekly_counts.values, alpha=0.7, color='lightgreen')
        ax2.set_xlabel('Day of Week')
        ax2.set_ylabel('Trade Count')
        ax2.set_title('Trading Frequency by Day of Week')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)
        
        # Daily trade count
        daily_counts = self.data['date'].dt.date.value_counts().sort_index()
        ax3.plot(daily_counts.index, daily_counts.values, marker='o', markersize=3, alpha=0.7)
        ax3.set_xlabel('Date')
        ax3.set_ylabel('Trade Count')
        ax3.set_title('Daily Trade Count Trend')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)
        
        # Trade type distribution
        if 'trade_type' in self.data.columns:
            type_counts = self.data['trade_type'].value_counts()
            ax4.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%', startangle=90)
            ax4.set_title('Trade Type Distribution')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"图表已保存到: {save_path}")
        
        return fig
    
    def plot_position_analysis(self, save_path: Optional[str] = None):
        """绘制持仓分析图"""
        if 'position_change' not in self.data.columns:
            self.logger.error("没有持仓变化数据")
            return None
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Position change distribution
        position_counts = self.data['position_change'].value_counts()
        ax1.bar(position_counts.index, position_counts.values, alpha=0.7, color='orange')
        ax1.set_xlabel('Position Change Type')
        ax1.set_ylabel('Count')
        ax1.set_title('Position Change Distribution')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3)
        
        # 持仓方向盈亏对比
        if 'closed_pnl' in self.data.columns:
            position_pnl = self.data.groupby('position_change')['closed_pnl'].sum()
            colors = ['green' if x > 0 else 'red' for x in position_pnl.values]
            ax2.bar(position_pnl.index, position_pnl.values, alpha=0.7, color=colors)
            ax2.set_xlabel('Position Change Type')
            ax2.set_ylabel('Cumulative P&L')
            ax2.set_title('Cumulative P&L by Position Direction')
            ax2.tick_params(axis='x', rotation=45)
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"图表已保存到: {save_path}")
        
        return fig
    
    def create_dashboard(self, save_path: Optional[str] = None):
        """Create comprehensive dashboard"""
        fig, axes = plt.subplots(3, 2, figsize=(20, 15))
        fig.suptitle('Trading Analysis Comprehensive Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Cumulative P&L curve
        ax = axes[0, 0]
        if 'cumulative_pnl' in self.data.columns:
            x_data = self.data['date'] if 'date' in self.data.columns else self.data.index
            ax.plot(x_data, self.data['cumulative_pnl'], linewidth=2, color='blue')
            ax.set_title('Cumulative P&L Curve')
            ax.set_ylabel('Cumulative P&L')
            ax.grid(True, alpha=0.3)
        
        # 2. P&L distribution histogram
        ax = axes[0, 1]
        if 'closed_pnl' in self.data.columns:
            pnl_data = self.data['closed_pnl'].dropna()
            ax.hist(pnl_data, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            ax.axvline(pnl_data.mean(), color='red', linestyle='--', label=f'Mean: {pnl_data.mean():.4f}')
            ax.set_title('P&L Distribution')
            ax.set_xlabel('P&L')
            ax.set_ylabel('Frequency')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        # 3. Price trend
        ax = axes[1, 0]
        if 'price' in self.data.columns:
            x_data = self.data['date'] if 'date' in self.data.columns else self.data.index
            ax.plot(x_data, self.data['price'], linewidth=1, color='black', alpha=0.7)
            ax.set_title('Price Trend')
            ax.set_ylabel('Price')
            ax.grid(True, alpha=0.3)
        
        # 4. Trading frequency (by hour)
        ax = axes[1, 1]
        if 'hour' in self.data.columns:
            hourly_counts = self.data['hour'].value_counts().sort_index()
            ax.bar(hourly_counts.index, hourly_counts.values, alpha=0.7, color='lightgreen')
            ax.set_title('Trading Frequency by Hour')
            ax.set_xlabel('Hour')
            ax.set_ylabel('Trade Count')
            ax.grid(True, alpha=0.3)
        
        # 5. Position distribution
        ax = axes[2, 0]
        if 'position_change' in self.data.columns:
            position_counts = self.data['position_change'].value_counts()
            ax.pie(position_counts.values, labels=position_counts.index, autopct='%1.1f%%', startangle=90)
            ax.set_title('Position Change Distribution')
        
        # 6. Win/Loss trade comparison
        ax = axes[2, 1]
        if 'closed_pnl' in self.data.columns:
            pnl_data = self.data['closed_pnl'].dropna()
            win_trades = len(pnl_data[pnl_data > 0])
            loss_trades = len(pnl_data[pnl_data < 0])
            equal_trades = len(pnl_data[pnl_data == 0])
            
            categories = ['Profit', 'Loss', 'Break-even']
            values = [win_trades, loss_trades, equal_trades]
            colors = ['green', 'red', 'gray']
            
            ax.pie(values, labels=categories, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.set_title('Win/Loss Trade Ratio')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Dashboard saved to: {save_path}")
        
        return fig
    
    def save_all_charts(self, output_dir: str = "charts"):
        """Save all charts to specified directory"""
        import os
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        charts = {
            "P&L Curve": self.plot_pnl_curve,
            "Price Trend": self.plot_price_chart,
            "P&L Distribution": self.plot_pnl_distribution,
            "Trading Frequency": self.plot_trading_frequency,
            "Position Analysis": self.plot_position_analysis,
            "Comprehensive Dashboard": self.create_dashboard
        }
        
        for name, func in charts.items():
            try:
                save_path = os.path.join(output_dir, f"{name}.png")
                func(save_path=save_path)
                self.logger.info(f"Generated chart: {name}")
            except Exception as e:
                self.logger.error(f"Failed to generate chart {name}: {e}")
        
        self.logger.info(f"All charts saved to directory: {output_dir}") 