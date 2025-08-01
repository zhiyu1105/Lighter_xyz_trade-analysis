# 📈 交易数据分析框架

一个功能强大、易于使用的交易数据分析工具，支持多种数据格式，提供全面的交易绩效分析和可视化功能。

## ✨ 主要功能

### 🔧 核心功能
- **多格式数据导入**: 支持 CSV、Excel 格式的交易数据
- **智能数据清洗**: 自动标准化数据格式，处理缺失值
- **全面绩效分析**: 盈亏分析、风险指标、回撤分析等
- **丰富可视化**: 静态图表和交互式图表支持
- **报告生成**: 一键生成 JSON 格式的综合分析报告

### 📊 分析维度
- **盈亏分析**: 总盈亏、胜率、盈亏比、最大盈利/亏损
- **风险分析**: 夏普比率、最大回撤、VaR、CVaR
- **交易频率**: 按时间段分析交易频率和模式
- **持仓分析**: 多空持仓分布和绩效对比
- **时间分析**: 交易时间习惯和绩效表现

### 🎨 可视化图表
- 累积盈亏曲线
- 回撤走势图
- 价格走势与交易点标记
- 盈亏分布直方图
- 交易频率热力图
- 综合分析仪表板

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 方法一：网页界面 (推荐)

启动 Streamlit 应用：

```bash
streamlit run app.py
```

然后在浏览器中打开显示的地址（通常是 `http://localhost:8501`）。

### 方法二：命令行使用

#### 分析示例数据
```bash
python example_analysis.py
```

#### 分析自定义文件
```bash
python example_analysis.py your_trade_data.csv
```

### 方法三：代码集成

```python
from trade_analyzer import TradeDataProcessor, TradeAnalyzer, TradeVisualizer

# 加载数据
processor = TradeDataProcessor()
data = processor.load_csv('your_trade_data.csv')

# 分析
analyzer = TradeAnalyzer(data)
pnl_stats = analyzer.calculate_pnl_statistics()
risk_metrics = analyzer.calculate_risk_metrics()

# 可视化
visualizer = TradeVisualizer(data)
fig = visualizer.plot_pnl_curve()
visualizer.save_all_charts('output_charts')
```

## 📁 数据格式要求

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

### 数据示例

```csv
Market,Side,Date,Trade Value,Size,Price,Closed PnL,Fee,Role,Type
BTC,Long > Short,2025-01-01 10:30:00,1000.5,0.001,50000,15.25,2.0,Taker,trade
BTC,Short > Long,2025-01-01 11:15:00,980.3,0.001,49015,-8.50,2.0,Taker,trade
```

## 🏗️ 项目结构

```
TradeAnalysis/
├── trade_analyzer/              # 核心分析包
│   ├── __init__.py             # 包初始化
│   ├── data_processor.py       # 数据处理模块
│   ├── analyzer.py             # 分析计算模块
│   └── visualizer.py           # 可视化模块
├── app.py                      # Streamlit 网页应用
├── example_analysis.py         # 命令行示例脚本
├── requirements.txt            # 依赖列表
├── README.md                  # 项目文档
└── lighter-trade-export-*.csv  # 示例数据文件
```

## 📊 分析指标说明

### 盈亏指标
- **总盈亏**: 所有交易的盈亏总和
- **胜率**: 盈利交易占总交易的百分比
- **盈亏比**: 平均盈利与平均亏损的比值
- **夏普比率**: 风险调整后的收益率指标

### 风险指标
- **最大回撤**: 从历史最高点到最低点的最大损失
- **VaR (Value at Risk)**: 在一定置信度下的最大可能损失
- **CVaR (条件VaR)**: 超过VaR阈值的平均损失

### 交易频率指标
- **日均交易次数**: 平均每天的交易频率
- **最活跃时段**: 交易最频繁的时间段
- **交易分布**: 按时间维度的交易分布情况

## 🎯 使用场景

### 个人交易者
- 分析个人交易记录
- 评估交易策略效果
- 识别交易习惯和模式
- 风险管理和控制

### 策略开发
- 回测交易策略
- 比较不同策略表现
- 优化交易参数
- 风险收益分析

### 投资机构
- 交易员绩效评估
- 风险监控和管理
- 合规报告生成
- 投资组合分析

## 🛠️ 自定义扩展

### 添加新的分析指标

```python
class CustomAnalyzer(TradeAnalyzer):
    def calculate_custom_metric(self):
        # 你的自定义计算逻辑
        return custom_result
```

### 自定义可视化

```python
class CustomVisualizer(TradeVisualizer):
    def plot_custom_chart(self):
        # 你的自定义图表逻辑
        return fig
```

## 📈 性能优化

- 对于大数据集（>100万条记录），建议使用数据过滤功能
- 生成图表时可选择静态图表以提高速度
- 可通过并行处理优化多文件分析

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🆘 常见问题

### Q: 支持哪些数据格式？
A: 目前支持 CSV 和 Excel (.xlsx, .xls) 格式。

### Q: 如何处理缺失的列？
A: 框架会自动处理缺失列，只有 Date 和 Closed PnL 是必需的。

### Q: 可以分析加密货币以外的交易数据吗？
A: 可以，框架支持任何类型的交易数据（股票、期货、外汇等）。

### Q: 如何自定义分析指标？
A: 可以继承 TradeAnalyzer 类并添加自己的分析方法。

### Q: 生成的图表可以保存吗？
A: 可以，支持保存为 PNG 格式，或使用交互式图表。

## 📞 支持

如果你在使用过程中遇到问题，可以：

1. 查看项目 Issues
2. 提交新的 Issue 描述问题
3. 查看示例代码和文档

---

**�� 开始你的交易数据分析之旅吧！** 