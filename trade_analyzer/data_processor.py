"""
Trading Data Processing Module
Responsible for data import, cleaning and standardization
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Union
import logging

class TradeDataProcessor:
    """Trading Data Processor"""
    
    def __init__(self):
        self.data = None
        self.raw_data = None
        self.logger = logging.getLogger(__name__)
        
    def load_csv(self, file_path: str, encoding: str = 'utf-8') -> pd.DataFrame:
        """
        Load CSV file
        
        Args:
            file_path: File path
            encoding: File encoding
            
        Returns:
            Processed DataFrame
        """
        try:
            # Read CSV file
            self.raw_data = pd.read_csv(file_path, encoding=encoding)
            self.logger.info(f"Successfully loaded data file: {file_path}")
            self.logger.info(f"Data shape: {self.raw_data.shape}")
            
            # Standardize data
            self.data = self._standardize_data(self.raw_data.copy())
            
            return self.data
            
        except Exception as e:
            self.logger.error(f"Failed to load file: {e}")
            raise
            
    def load_excel(self, file_path: str, sheet_name: Union[str, int] = 0) -> pd.DataFrame:
        """
        Load Excel file
        
        Args:
            file_path: File path
            sheet_name: Worksheet name or index
            
        Returns:
            Processed DataFrame
        """
        try:
            self.raw_data = pd.read_excel(file_path, sheet_name=sheet_name)
            self.logger.info(f"Successfully loaded Excel file: {file_path}")
            
            self.data = self._standardize_data(self.raw_data.copy())
            return self.data
            
        except Exception as e:
            self.logger.error(f"Failed to load Excel file: {e}")
            raise
    
    def _standardize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize data format
        
        Args:
            df: Raw data
            
        Returns:
            Standardized data
        """
        try:
            # Create standardized copy
            standardized_df = df.copy()
            
            # Standardize column names (convert to lowercase, replace spaces)
            standardized_df.columns = [col.lower().replace(' ', '_') for col in standardized_df.columns]
            
            # Process date column
            if 'date' in standardized_df.columns:
                standardized_df['date'] = pd.to_datetime(standardized_df['date'])
                standardized_df = standardized_df.sort_values('date').reset_index(drop=True)
            
            # Process numeric columns
            numeric_columns = ['trade_value', 'size', 'price', 'closed_pnl', 'fee']
            for col in numeric_columns:
                if col in standardized_df.columns:
                    standardized_df[col] = pd.to_numeric(standardized_df[col], errors='coerce')
            
            # Process trade direction
            if 'side' in standardized_df.columns:
                standardized_df['trade_type'] = standardized_df['side'].apply(self._categorize_trade_type)
                standardized_df['position_change'] = standardized_df['side'].apply(self._get_position_change)
            
            # Add calculated fields
            standardized_df = self._add_calculated_fields(standardized_df)
            
            self.logger.info("Data standardization completed")
            return standardized_df
            
        except Exception as e:
            self.logger.error(f"Data standardization failed: {e}")
            raise
    
    def _categorize_trade_type(self, side: str) -> str:
        """Categorize trade type"""
        if pd.isna(side):
            return 'Unknown'
        
        side_lower = side.lower()
        if 'open' in side_lower:
            return 'Open'
        elif 'close' in side_lower:
            return 'Close'
        elif '>' in side_lower:
            return 'Flip'  # Direction flip
        else:
            return 'Other'
    
    def _get_position_change(self, side: str) -> str:
        """Get position change"""
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
        """Add calculated fields"""
        # Cumulative P&L
        if 'closed_pnl' in df.columns:
            df['cumulative_pnl'] = df['closed_pnl'].fillna(0).cumsum()
        
        # Trading time related
        if 'date' in df.columns:
            df['hour'] = df['date'].dt.hour
            df['day_of_week'] = df['date'].dt.day_name()
            df['is_weekend'] = df['date'].dt.weekday >= 5
        
        # Price changes
        if 'price' in df.columns:
            df['price_change'] = df['price'].pct_change()
            df['price_ma_10'] = df['price'].rolling(window=10).mean()
        
        return df
    
    def get_data_summary(self) -> Dict:
        """Get data summary"""
        if self.data is None:
            return {"error": "No data loaded"}
        
        summary = {
            "total_trades": len(self.data),
            "data_time_range": {
                "start": self.data['date'].min() if 'date' in self.data.columns else "N/A",
                "end": self.data['date'].max() if 'date' in self.data.columns else "N/A"
            },
            "total_pnl": self.data['closed_pnl'].sum() if 'closed_pnl' in self.data.columns else "N/A",
            "total_fees": self.data['fee'].sum() if 'fee' in self.data.columns else "N/A",
            "average_trade_value": self.data['trade_value'].mean() if 'trade_value' in self.data.columns else "N/A",
            "trade_type_distribution": self.data['trade_type'].value_counts().to_dict() if 'trade_type' in self.data.columns else {},
            "data_quality": {
                "missing_values": self.data.isnull().sum().to_dict(),
                "duplicate_rows": self.data.duplicated().sum()
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
        Filter data
        
        Args:
            start_date: Start date
            end_date: End date
            trade_type: Trade type
            min_size: Minimum trade size
            max_size: Maximum trade size
            
        Returns:
            Filtered data
        """
        if self.data is None:
            raise ValueError("No data available")
        
        filtered_data = self.data.copy()
        
        # Date filtering
        if start_date and 'date' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['date'] >= start_date]
        
        if end_date and 'date' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['date'] <= end_date]
        
        # Trade type filtering
        if trade_type and 'trade_type' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['trade_type'] == trade_type]
        
        # Trade size filtering
        if min_size and 'size' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['size'] >= min_size]
        
        if max_size and 'size' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['size'] <= max_size]
        
        return filtered_data
    
    def export_data(self, file_path: str, format: str = 'csv') -> None:
        """
        Export data
        
        Args:
            file_path: Export path
            format: Export format ('csv', 'excel')
        """
        if self.data is None:
            raise ValueError("No data available")
        
        if format.lower() == 'csv':
            self.data.to_csv(file_path, index=False, encoding='utf-8-sig')
        elif format.lower() == 'excel':
            self.data.to_excel(file_path, index=False)
        else:
            raise ValueError("Unsupported export format")
        
        self.logger.info(f"Data exported to: {file_path}") 