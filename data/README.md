# 📁 数据文件夹

这个文件夹用于存放你的交易数据文件。

## 📋 支持的文件格式

- **CSV文件** (.csv) - 推荐格式
- **Excel文件** (.xlsx, .xls)

## 📊 数据格式要求

你的交易数据文件应包含以下列（列名不区分大小写）：

| 列名 | 说明 | 必需性 | 示例 |
|------|------|--------|------|
| Market | 市场/品种 | 可选 | BTC, ETH, AAPL |
| Side | 交易方向 | 可选 | Long, Short, Long > Short |
| Date | 交易日期时间 | **必需** | 2025-01-01 10:30:00 |
| Trade Value | 交易价值 | 可选 | 1000.50 |
| Size | 交易数量 | 可选 | 0.001 |
| Price | 交易价格 | 可选 | 50000.0 |
| Closed PnL | 已实现盈亏 | **必需** | 15.25, -8.50 |
| Fee | 手续费 | 可选 | 2.0 |
| Role | 角色 | 可选 | Maker, Taker |

## 📝 数据示例

```csv
Market,Side,Date,Trade Value,Size,Price,Closed PnL,Fee,Role,Type
BTC,Long > Short,2025-01-01 10:30:00,1000.5,0.001,50000,15.25,2.0,Taker,trade
BTC,Short > Long,2025-01-01 11:15:00,980.3,0.001,49015,-8.50,2.0,Taker,trade
```

## 🎯 使用方法

### 1. 放置数据文件
将你的交易数据文件放在这个文件夹中：
```
data/
├── your_trade_data.csv
├── another_trade_data.xlsx
└── historical_data.csv
```

### 2. 启动分析
```bash
# 网页界面
streamlit run app.py

# 命令行分析
python3 example_analysis.py data/your_trade_data.csv
```

## 💡 提示

- 建议使用有意义的文件名，如 `BTC_trades_2025.csv`
- 确保文件使用UTF-8编码
- 重要数据建议备份到其他位置
- 可以放置多个数据文件进行对比分析

## 📂 当前文件

- `lighter-trade-export-2025-08-01T03_15_40.421Z-UTC.csv` - 示例数据文件 