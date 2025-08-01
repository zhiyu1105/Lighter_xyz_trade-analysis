"""
交易分析示例脚本
演示如何使用交易分析框架
"""

import os
import json
from datetime import datetime
import logging
import glob
import sys

from trade_analyzer import TradeDataProcessor, TradeAnalyzer, TradeVisualizer

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('trade_analysis.log', encoding='utf-8')
    ]
)

def get_data_files():
    """获取data文件夹中的可用数据文件"""
    data_dir = "data"
    if not os.path.exists(data_dir):
        return []
    
    files = []
    # 查找CSV文件
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    files.extend(csv_files)
    
    # 查找Excel文件
    excel_files = glob.glob(os.path.join(data_dir, "*.xlsx"))
    excel_files.extend(glob.glob(os.path.join(data_dir, "*.xls")))
    files.extend(excel_files)
    
    return sorted(files)

def list_data_files():
    """列出data文件夹中的文件"""
    files = get_data_files()
    if not files:
        print("❌ data文件夹中没有找到数据文件")
        print("请将你的交易数据文件放入data文件夹中")
        return None
    
    print("📁 data文件夹中的可用文件：")
    for i, file in enumerate(files, 1):
        print(f"  {i}. {os.path.basename(file)}")
    
    return files

def select_data_file():
    """让用户选择数据文件"""
    files = get_data_files()
    if not files:
        return None
    
    if len(files) == 1:
        print(f"📊 自动选择唯一文件：{os.path.basename(files[0])}")
        return files[0]
    
    print("\n请选择要分析的文件：")
    for i, file in enumerate(files, 1):
        print(f"  {i}. {os.path.basename(file)}")
    
    while True:
        try:
            choice = input(f"\n请输入文件编号 (1-{len(files)}) 或按回车选择第一个文件: ").strip()
            if not choice:
                return files[0]
            
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(files):
                return files[choice_idx]
            else:
                print(f"❌ 无效选择，请输入 1-{len(files)} 之间的数字")
        except ValueError:
            print("❌ 请输入有效的数字")
        except KeyboardInterrupt:
            print("\n👋 再见！")
            sys.exit(0)

def main():
    """主函数"""
    print("🚀 交易数据分析框架示例")
    print("=" * 50)
    
    # 检查data文件夹
    if not os.path.exists("data"):
        print("📁 创建data文件夹...")
        os.makedirs("data", exist_ok=True)
        print("✅ data文件夹已创建")
        print("请将你的交易数据文件放入data文件夹中")
        return
    
    # 获取数据文件
    if len(sys.argv) > 1:
        # 如果提供了文件路径参数，分析指定文件
        custom_file = sys.argv[1]
        if not os.path.exists(custom_file):
            print(f"❌ 文件不存在: {custom_file}")
            return
        data_file = custom_file
        print(f"📊 分析指定文件: {os.path.basename(data_file)}")
    else:
        # 让用户选择文件
        data_file = select_data_file()
        if not data_file:
            return
    
    try:
        # 1. 数据处理
        print(f"\n📁 步骤1: 加载和处理数据")
        processor = TradeDataProcessor()
        
        # 根据文件扩展名选择加载方法
        if data_file.endswith('.csv'):
            data = processor.load_csv(data_file)
        elif data_file.endswith(('.xlsx', '.xls')):
            data = processor.load_excel(data_file)
        else:
            print("❌ 不支持的文件格式，请使用CSV或Excel文件")
            return
        
        print(f"✅ Successfully loaded data: {len(data)} rows")
        print(f"📊 Data columns: {list(data.columns)}")
        
        # Display data summary
        print("\n📋 Data Summary:")
        summary = processor.get_data_summary()
        for key, value in summary.items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for sub_key, sub_value in value.items():
                    print(f"    {sub_key}: {sub_value}")
            else:
                print(f"  {key}: {value}")
        
        # 2. Trading analysis
        print("\n📈 Step 2: Trading Performance Analysis")
        analyzer = TradeAnalyzer(data)
        
        # P&L analysis
        print("\n💰 P&L Analysis:")
        pnl_stats = analyzer.calculate_pnl_statistics()
        for key, value in pnl_stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")
        
        # Drawdown analysis
        print("\n📉 Drawdown Analysis:")
        drawdown_stats = analyzer.calculate_drawdown()
        for key, value in drawdown_stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")
        
        # Risk metrics
        print("\n⚠️ Risk Metrics:")
        risk_metrics = analyzer.calculate_risk_metrics()
        for key, value in risk_metrics.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")
        
        # Trading frequency analysis
        print("\n⏰ Trading Frequency Analysis:")
        freq_stats = analyzer.analyze_trading_frequency()
        for key, value in freq_stats.items():
            if not isinstance(value, dict):
                print(f"  {key}: {value}")
        
        # Best and worst trades
        print("\n🏆 Best and Worst Trades:")
        best_worst = analyzer.find_best_worst_trades(3)
        
        print("  Best trades:")
        for i, trade in enumerate(best_worst.get("best_trades", []), 1):
            print(f"    {i}. Date: {trade.get('date')}, P&L: {trade.get('closed_pnl'):.4f}")
        
        print("  Worst trades:")
        for i, trade in enumerate(best_worst.get("worst_trades", []), 1):
            print(f"    {i}. Date: {trade.get('date')}, P&L: {trade.get('closed_pnl'):.4f}")
        
        # 3. Visualization analysis
        print("\n📊 Step 3: Generate Visualization Charts")
        visualizer = TradeVisualizer(data)
        
        # Create charts output directory
        charts_dir = "analysis_charts"
        os.makedirs(charts_dir, exist_ok=True)
        
        # Generate all charts
        print(f"  Generating charts to directory: {charts_dir}")
        visualizer.save_all_charts(charts_dir)
        
        # 4. Generate comprehensive report
        print("\n📑 Step 4: Generate Comprehensive Report")
        report = analyzer.generate_performance_report()
        
        # Save JSON report
        report_filename = f"trade_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"✅ Comprehensive report saved: {report_filename}")
        
        # 5. Display key conclusions
        print("\n🎯 Key Conclusions:")
        print("=" * 30)
        
        # Performance summary
        total_pnl = pnl_stats.get("total_pnl", 0)
        win_rate = pnl_stats.get("win_rate", 0)
        profit_loss_ratio = pnl_stats.get("profit_factor", 0)
        max_drawdown = drawdown_stats.get("max_drawdown_amount", 0)
        sharpe_ratio = risk_metrics.get("sharpe_ratio", 0)
        
        print(f"📊 Trading Performance:")
        print(f"  • Total P&L: {total_pnl:.4f}")
        print(f"  • Win Rate: {win_rate:.2f}%")
        print(f"  • Profit Factor: {profit_loss_ratio:.2f}")
        print(f"  • Max Drawdown: {max_drawdown:.4f}")
        print(f"  • Sharpe Ratio: {sharpe_ratio:.4f}")
        
        # Performance assessment
        print(f"\n🏅 Performance Assessment:")
        if total_pnl > 0:
            print("  ✅ Overall profitable")
        else:
            print("  ❌ Overall loss")
        
        if win_rate > 50:
            print("  ✅ Win rate above 50%")
        else:
            print("  ⚠️ Win rate below 50%")
        
        if profit_loss_ratio > 1:
            print("  ✅ Profit factor above 1")
        else:
            print("  ⚠️ Profit factor below 1")
        
        if sharpe_ratio > 1:
            print("  ✅ Excellent Sharpe ratio")
        elif sharpe_ratio > 0.5:
            print("  🔶 Good Sharpe ratio")
        else:
            print("  ⚠️ Sharpe ratio needs improvement")
        
        # Trading recommendations
        print(f"\n💡 Trading Recommendations:")
        if win_rate < 40:
            print("  • Consider improving trading strategy to increase win rate")
        if profit_loss_ratio < 1:
            print("  • Suggest optimizing profit/loss ratio to improve profit factor")
        if abs(max_drawdown) > total_pnl * 0.2:
            print("  • Pay attention to risk control, drawdown is too large")
        if freq_stats.get("average_daily_trades", 0) > 20:
            print("  • High trading frequency, pay attention to trading costs")
        
        print(f"\n🎉 Analysis completed!")
        print(f"📁 Charts folder: {charts_dir}")
        print(f"📄 Report file: {report_filename}")
        print(f"📝 Log file: trade_analysis.log")
        
    except Exception as e:
        print(f"❌ 分析过程中发生错误: {e}")
        logging.error(f"分析失败: {e}", exc_info=True)

def analyze_custom_file(file_path: str):
    """分析自定义文件"""
    print(f"🔍 分析文件: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return
    
    try:
        processor = TradeDataProcessor()
        
        # 根据文件扩展名选择加载方法
        if file_path.endswith('.csv'):
            data = processor.load_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            data = processor.load_excel(file_path)
        else:
            print("❌ 不支持的文件格式，请使用CSV或Excel文件")
            return
        
        # 快速分析
        analyzer = TradeAnalyzer(data)
        summary = processor.get_data_summary()
        pnl_stats = analyzer.calculate_pnl_statistics()
        
        print(f"✅ File analysis completed")
        print(f"📊 Trade count: {summary.get('total_trades', 'N/A')}")
        print(f"💰 Total P&L: {summary.get('total_pnl', 'N/A')}")
        print(f"🎯 Win rate: {pnl_stats.get('win_rate', 'N/A'):.2f}%")
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")

if __name__ == "__main__":
    main() 