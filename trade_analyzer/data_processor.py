"""
交易数据处理模块
负责数据导入、清洗和标准化
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Union
import logging

class TradeDataProcessor:
    """交易数据处理器"""
    
    def __init__(self):
        self.data = None
        self.raw_data = None
        self.logger = logging.getLogger(__name__)
        
    def load_csv(self, file_path: str, encoding: str = 'utf-8') -> pd.DataFrame:
        """
        加载CSV文件
        
        Args:
            file_path: 文件路径
            encoding: 文件编码
            
        Returns:
            处理后的DataFrame
        """
        try:
            # 读取CSV文件
            self.raw_data = pd.read_csv(file_path, encoding=encoding)
            self.logger.info(f"成功加载数据文件: {file_path}")
            self.logger.info(f"数据形状: {self.raw_data.shape}")
            
            # 标准化数据
            self.data = self._standardize_data(self.raw_data.copy())
            
            return self.data
            
        except Exception as e:
            self.logger.error(f"加载文件失败: {e}")
            raise
            
    def load_excel(self, file_path: str, sheet_name: Union[str, int] = 0) -> pd.DataFrame:
        """
        加载Excel文件
        
        Args:
            file_path: 文件路径
            sheet_name: 工作表名称或索引
            
        Returns:
            处理后的DataFrame
        """
        try:
            self.raw_data = pd.read_excel(file_path, sheet_name=sheet_name)
            self.logger.info(f"成功加载Excel文件: {file_path}")
            
            self.data = self._standardize_data(self.raw_data.copy())
            return self.data
            
        except Exception as e:
            self.logger.error(f"加载Excel文件失败: {e}")
            raise
    
    def _standardize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        标准化数据格式
        
        Args:
            df: 原始数据
            
        Returns:
            标准化后的数据
        """
        try:
            # 创建标准化副本
            standardized_df = df.copy()
            
            # 标准化列名（转换为小写，替换空格）
            standardized_df.columns = [col.lower().replace(' ', '_') for col in standardized_df.columns]
            
            # 处理日期列
            if 'date' in standardized_df.columns:
                standardized_df['date'] = pd.to_datetime(standardized_df['date'])
                standardized_df = standardized_df.sort_values('date').reset_index(drop=True)
            
            # 处理数值列
            numeric_columns = ['trade_value', 'size', 'price', 'closed_pnl', 'fee']
            for col in numeric_columns:
                if col in standardized_df.columns:
                    standardized_df[col] = pd.to_numeric(standardized_df[col], errors='coerce')
            
            # 处理交易方向
            if 'side' in standardized_df.columns:
                standardized_df['trade_type'] = standardized_df['side'].apply(self._categorize_trade_type)
                standardized_df['position_change'] = standardized_df['side'].apply(self._get_position_change)
            
            # 添加计算字段
            standardized_df = self._add_calculated_fields(standardized_df)
            
            self.logger.info("数据标准化完成")
            return standardized_df
            
        except Exception as e:
            self.logger.error(f"数据标准化失败: {e}")
            raise
    
    def _categorize_trade_type(self, side: str) -> str:
        """分类交易类型"""
        if pd.isna(side):
            return 'Unknown'
        
        side_lower = side.lower()
        if 'open' in side_lower:
            return 'Open'
        elif 'close' in side_lower:
            return 'Close'
        elif '>' in side_lower:
            return 'Flip'  # 翻转方向
        else:
            return 'Other'
    
    def _get_position_change(self, side: str) -> str:
        """获取持仓变化"""
        if pd.isna(side):
            return 'Unknown'
        
        side_lower = side.lower()
        if 'long' in side_lower and 'short' not in side_lower:
            return 'Long'
        elif 'short' in side_lower and 'long' not in side_lower:
            return 'Short'
        elif 'short > long' in side_lower:
            return 'Short_to_Long'
        elif 'long > short' in side_lower:
            return 'Long_to_Short'
        else:
            return 'Other'
    
    def _add_calculated_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """添加计算字段"""
        # 累积盈亏
        if 'closed_pnl' in df.columns:
            df['cumulative_pnl'] = df['closed_pnl'].fillna(0).cumsum()
        
        # 交易时间相关
        if 'date' in df.columns:
            df['hour'] = df['date'].dt.hour
            df['day_of_week'] = df['date'].dt.day_name()
            df['is_weekend'] = df['date'].dt.weekday >= 5
        
        # 价格变化
        if 'price' in df.columns:
            df['price_change'] = df['price'].pct_change()
            df['price_ma_10'] = df['price'].rolling(window=10).mean()
        
        return df
    
    def get_data_summary(self) -> Dict:
        """获取数据摘要"""
        if self.data is None:
            return {"error": "没有加载数据"}
        
        summary = {
            "总交易笔数": len(self.data),
            "数据时间范围": {
                "开始": self.data['date'].min() if 'date' in self.data.columns else "N/A",
                "结束": self.data['date'].max() if 'date' in self.data.columns else "N/A"
            },
            "总盈亏": self.data['closed_pnl'].sum() if 'closed_pnl' in self.data.columns else "N/A",
            "总手续费": self.data['fee'].sum() if 'fee' in self.data.columns else "N/A",
            "平均交易价值": self.data['trade_value'].mean() if 'trade_value' in self.data.columns else "N/A",
            "交易类型分布": self.data['trade_type'].value_counts().to_dict() if 'trade_type' in self.data.columns else {},
            "数据质量": {
                "缺失值": self.data.isnull().sum().to_dict(),
                "重复行": self.data.duplicated().sum()
            }
        }
        
        return summary
    
    def filter_data(self, 
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None,
                   trade_type: Optional[str] = None,
                   min_size: Optional[float] = None,
                   max_size: Optional[float] = None) -> pd.DataFrame:
        """
        过滤数据
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            trade_type: 交易类型
            min_size: 最小交易量
            max_size: 最大交易量
            
        Returns:
            过滤后的数据
        """
        if self.data is None:
            raise ValueError("没有可用数据")
        
        filtered_data = self.data.copy()
        
        # 日期过滤
        if start_date and 'date' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['date'] >= start_date]
        
        if end_date and 'date' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['date'] <= end_date]
        
        # 交易类型过滤
        if trade_type and 'trade_type' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['trade_type'] == trade_type]
        
        # 交易量过滤
        if min_size and 'size' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['size'] >= min_size]
        
        if max_size and 'size' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['size'] <= max_size]
        
        return filtered_data
    
    def export_data(self, file_path: str, format: str = 'csv') -> None:
        """
        导出数据
        
        Args:
            file_path: 导出路径
            format: 导出格式 ('csv', 'excel')
        """
        if self.data is None:
            raise ValueError("没有可用数据")
        
        if format.lower() == 'csv':
            self.data.to_csv(file_path, index=False, encoding='utf-8-sig')
        elif format.lower() == 'excel':
            self.data.to_excel(file_path, index=False)
        else:
            raise ValueError("不支持的导出格式")
        
        self.logger.info(f"数据已导出到: {file_path}") 