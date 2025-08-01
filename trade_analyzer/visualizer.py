"""
交易数据可视化模块
负责生成各种图表和可视化分析
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

# 设置中文字体（仅在非测试环境中）
import os
if not os.environ.get('TESTING'):
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

class TradeVisualizer:
    """交易数据可视化器"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.logger = logging.getLogger(__name__)
        
        # 设置绘图样式
        sns.set_style("whitegrid")
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def plot_pnl_curve(self, save_path: Optional[str] = None, interactive: bool = False):
        """绘制盈亏曲线"""
        if 'cumulative_pnl' not in self.data.columns:
            self.logger.error("没有累积盈亏数据")
            return None
        
        if interactive:
            return self._plot_pnl_curve_plotly()
        else:
            return self._plot_pnl_curve_matplotlib(save_path)
    
    def _plot_pnl_curve_matplotlib(self, save_path: Optional[str] = None):
        """使用matplotlib绘制盈亏曲线"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # 累积盈亏曲线
        if 'date' in self.data.columns:
            ax1.plot(self.data['date'], self.data['cumulative_pnl'], linewidth=2, color='blue')
            ax1.set_xlabel('日期')
        else:
            ax1.plot(self.data.index, self.data['cumulative_pnl'], linewidth=2, color='blue')
            ax1.set_xlabel('交易序号')
        
        ax1.set_ylabel('累积盈亏')
        ax1.set_title('累积盈亏曲线', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # 回撤图
        if 'cumulative_pnl' in self.data.columns:
            running_max = self.data['cumulative_pnl'].expanding().max()
            drawdown = self.data['cumulative_pnl'] - running_max
            
            if 'date' in self.data.columns:
                ax2.fill_between(self.data['date'], drawdown, 0, alpha=0.3, color='red')
                ax2.plot(self.data['date'], drawdown, color='red', linewidth=1)
                ax2.set_xlabel('日期')
            else:
                ax2.fill_between(self.data.index, drawdown, 0, alpha=0.3, color='red')
                ax2.plot(self.data.index, drawdown, color='red', linewidth=1)
                ax2.set_xlabel('交易序号')
            
            ax2.set_ylabel('回撤')
            ax2.set_title('回撤图', fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"图表已保存到: {save_path}")
        
        return fig
    
    def _plot_pnl_curve_plotly(self):
        """使用plotly绘制交互式盈亏曲线"""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('累积盈亏曲线', '回撤图'),
            vertical_spacing=0.08
        )
        
        # 准备x轴数据
        x_data = self.data['date'] if 'date' in self.data.columns else self.data.index
        
        # 累积盈亏曲线
        fig.add_trace(
            go.Scatter(
                x=x_data,
                y=self.data['cumulative_pnl'],
                mode='lines',
                name='累积盈亏',
                line=dict(color='blue', width=2)
            ),
            row=1, col=1
        )
        
        # 回撤图
        if 'cumulative_pnl' in self.data.columns:
            running_max = self.data['cumulative_pnl'].expanding().max()
            drawdown = self.data['cumulative_pnl'] - running_max
            
            fig.add_trace(
                go.Scatter(
                    x=x_data,
                    y=drawdown,
                    mode='lines',
                    name='回撤',
                    fill='tonexty',
                    line=dict(color='red', width=1),
                    fillcolor='rgba(255,0,0,0.3)'
                ),
                row=2, col=1
            )
        
        fig.update_layout(
            title='交易盈亏分析',
            height=700,
            showlegend=True
        )
        
        return fig
    
    def plot_price_chart(self, save_path: Optional[str] = None, interactive: bool = False):
        """绘制价格走势图"""
        if 'price' not in self.data.columns:
            self.logger.error("没有价格数据")
            return None
        
        if interactive:
            return self._plot_price_chart_plotly()
        else:
            return self._plot_price_chart_matplotlib(save_path)
    
    def _plot_price_chart_matplotlib(self, save_path: Optional[str] = None):
        """使用matplotlib绘制价格走势图"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x_data = self.data['date'] if 'date' in self.data.columns else self.data.index
        
        # 价格曲线
        ax.plot(x_data, self.data['price'], linewidth=1, color='black', alpha=0.7, label='价格')
        
        # 移动平均线
        if 'price_ma_10' in self.data.columns:
            ax.plot(x_data, self.data['price_ma_10'], linewidth=2, color='orange', label='10期移动平均')
        
        # 标记交易点
        if 'trade_type' in self.data.columns:
            open_trades = self.data[self.data['trade_type'] == 'Open']
            close_trades = self.data[self.data['trade_type'] == 'Close']
            
            if len(open_trades) > 0:
                open_x = open_trades['date'] if 'date' in self.data.columns else open_trades.index
                ax.scatter(open_x, open_trades['price'], color='green', marker='^', s=50, label='开仓', alpha=0.8)
            
            if len(close_trades) > 0:
                close_x = close_trades['date'] if 'date' in self.data.columns else close_trades.index
                ax.scatter(close_x, close_trades['price'], color='red', marker='v', s=50, label='平仓', alpha=0.8)
        
        ax.set_xlabel('时间')
        ax.set_ylabel('价格')
        ax.set_title('价格走势与交易点', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"图表已保存到: {save_path}")
        
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
        """绘制盈亏分布图"""
        if 'closed_pnl' not in self.data.columns:
            self.logger.error("没有盈亏数据")
            return None
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        pnl_data = self.data['closed_pnl'].dropna()
        
        # 盈亏直方图
        ax1.hist(pnl_data, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.axvline(pnl_data.mean(), color='red', linestyle='--', label=f'均值: {pnl_data.mean():.4f}')
        ax1.axvline(pnl_data.median(), color='green', linestyle='--', label=f'中位数: {pnl_data.median():.4f}')
        ax1.set_xlabel('盈亏')
        ax1.set_ylabel('频次')
        ax1.set_title('盈亏分布直方图')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 盈亏箱型图
        ax2.boxplot(pnl_data, vert=True)
        ax2.set_ylabel('盈亏')
        ax2.set_title('盈亏箱型图')
        ax2.grid(True, alpha=0.3)
        
        # 累积盈亏按时间分布
        if 'hour' in self.data.columns:
            hourly_pnl = self.data.groupby('hour')['closed_pnl'].sum()
            ax3.bar(hourly_pnl.index, hourly_pnl.values, alpha=0.7, color='lightcoral')
            ax3.set_xlabel('小时')
            ax3.set_ylabel('累积盈亏')
            ax3.set_title('按小时累积盈亏分布')
            ax3.grid(True, alpha=0.3)
        
        # 胜负交易对比
        win_trades = pnl_data[pnl_data > 0]
        loss_trades = pnl_data[pnl_data < 0]
        
        categories = ['盈利交易', '亏损交易']
        values = [len(win_trades), len(loss_trades)]
        colors = ['green', 'red']
        
        ax4.pie(values, labels=categories, colors=colors, autopct='%1.1f%%', startangle=90)
        ax4.set_title('盈亏交易占比')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"图表已保存到: {save_path}")
        
        return fig
    
    def plot_trading_frequency(self, save_path: Optional[str] = None):
        """绘制交易频率分析图"""
        if 'date' not in self.data.columns:
            self.logger.error("没有日期数据")
            return None
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 按小时分布
        if 'hour' in self.data.columns:
            hourly_counts = self.data['hour'].value_counts().sort_index()
        else:
            hourly_counts = self.data['date'].dt.hour.value_counts().sort_index()
        
        ax1.bar(hourly_counts.index, hourly_counts.values, alpha=0.7, color='skyblue')
        ax1.set_xlabel('小时')
        ax1.set_ylabel('交易次数')
        ax1.set_title('按小时交易频率分布')
        ax1.grid(True, alpha=0.3)
        
        # 按星期分布
        if 'day_of_week' in self.data.columns:
            weekly_counts = self.data['day_of_week'].value_counts()
        else:
            weekly_counts = self.data['date'].dt.day_name().value_counts()
        
        ax2.bar(weekly_counts.index, weekly_counts.values, alpha=0.7, color='lightgreen')
        ax2.set_xlabel('星期')
        ax2.set_ylabel('交易次数')
        ax2.set_title('按星期交易频率分布')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)
        
        # 按日期交易次数
        daily_counts = self.data['date'].dt.date.value_counts().sort_index()
        ax3.plot(daily_counts.index, daily_counts.values, marker='o', markersize=3, alpha=0.7)
        ax3.set_xlabel('日期')
        ax3.set_ylabel('交易次数')
        ax3.set_title('每日交易次数趋势')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)
        
        # 交易类型分布
        if 'trade_type' in self.data.columns:
            type_counts = self.data['trade_type'].value_counts()
            ax4.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%', startangle=90)
            ax4.set_title('交易类型分布')
        
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
        
        # 持仓变化分布
        position_counts = self.data['position_change'].value_counts()
        ax1.bar(position_counts.index, position_counts.values, alpha=0.7, color='orange')
        ax1.set_xlabel('持仓变化类型')
        ax1.set_ylabel('次数')
        ax1.set_title('持仓变化分布')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3)
        
        # 持仓方向盈亏对比
        if 'closed_pnl' in self.data.columns:
            position_pnl = self.data.groupby('position_change')['closed_pnl'].sum()
            colors = ['green' if x > 0 else 'red' for x in position_pnl.values]
            ax2.bar(position_pnl.index, position_pnl.values, alpha=0.7, color=colors)
            ax2.set_xlabel('持仓变化类型')
            ax2.set_ylabel('累积盈亏')
            ax2.set_title('各持仓方向累积盈亏')
            ax2.tick_params(axis='x', rotation=45)
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"图表已保存到: {save_path}")
        
        return fig
    
    def create_dashboard(self, save_path: Optional[str] = None):
        """创建综合仪表板"""
        fig, axes = plt.subplots(3, 2, figsize=(20, 15))
        fig.suptitle('交易分析综合仪表板', fontsize=16, fontweight='bold')
        
        # 1. 累积盈亏曲线
        ax = axes[0, 0]
        if 'cumulative_pnl' in self.data.columns:
            x_data = self.data['date'] if 'date' in self.data.columns else self.data.index
            ax.plot(x_data, self.data['cumulative_pnl'], linewidth=2, color='blue')
            ax.set_title('累积盈亏曲线')
            ax.set_ylabel('累积盈亏')
            ax.grid(True, alpha=0.3)
        
        # 2. 盈亏分布直方图
        ax = axes[0, 1]
        if 'closed_pnl' in self.data.columns:
            pnl_data = self.data['closed_pnl'].dropna()
            ax.hist(pnl_data, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            ax.axvline(pnl_data.mean(), color='red', linestyle='--', label=f'均值: {pnl_data.mean():.4f}')
            ax.set_title('盈亏分布')
            ax.set_xlabel('盈亏')
            ax.set_ylabel('频次')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        # 3. 价格走势
        ax = axes[1, 0]
        if 'price' in self.data.columns:
            x_data = self.data['date'] if 'date' in self.data.columns else self.data.index
            ax.plot(x_data, self.data['price'], linewidth=1, color='black', alpha=0.7)
            ax.set_title('价格走势')
            ax.set_ylabel('价格')
            ax.grid(True, alpha=0.3)
        
        # 4. 交易频率（按小时）
        ax = axes[1, 1]
        if 'hour' in self.data.columns:
            hourly_counts = self.data['hour'].value_counts().sort_index()
            ax.bar(hourly_counts.index, hourly_counts.values, alpha=0.7, color='lightgreen')
            ax.set_title('按小时交易频率')
            ax.set_xlabel('小时')
            ax.set_ylabel('交易次数')
            ax.grid(True, alpha=0.3)
        
        # 5. 持仓分布
        ax = axes[2, 0]
        if 'position_change' in self.data.columns:
            position_counts = self.data['position_change'].value_counts()
            ax.pie(position_counts.values, labels=position_counts.index, autopct='%1.1f%%', startangle=90)
            ax.set_title('持仓变化分布')
        
        # 6. 胜负交易对比
        ax = axes[2, 1]
        if 'closed_pnl' in self.data.columns:
            pnl_data = self.data['closed_pnl'].dropna()
            win_trades = len(pnl_data[pnl_data > 0])
            loss_trades = len(pnl_data[pnl_data < 0])
            equal_trades = len(pnl_data[pnl_data == 0])
            
            categories = ['盈利', '亏损', '平局']
            values = [win_trades, loss_trades, equal_trades]
            colors = ['green', 'red', 'gray']
            
            ax.pie(values, labels=categories, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.set_title('盈亏交易占比')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"仪表板已保存到: {save_path}")
        
        return fig
    
    def save_all_charts(self, output_dir: str = "charts"):
        """保存所有图表到指定目录"""
        import os
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        charts = {
            "盈亏曲线": self.plot_pnl_curve,
            "价格走势": self.plot_price_chart,
            "盈亏分布": self.plot_pnl_distribution,
            "交易频率": self.plot_trading_frequency,
            "持仓分析": self.plot_position_analysis,
            "综合仪表板": self.create_dashboard
        }
        
        for name, func in charts.items():
            try:
                save_path = os.path.join(output_dir, f"{name}.png")
                func(save_path=save_path)
                self.logger.info(f"已生成图表: {name}")
            except Exception as e:
                self.logger.error(f"生成图表失败 {name}: {e}")
        
        self.logger.info(f"所有图表已保存到目录: {output_dir}") 