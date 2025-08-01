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
        
        print(f"✅ 成功加载数据: {len(data)} 行记录")
        print(f"📊 数据列: {list(data.columns)}")
        
        # 显示数据摘要
        print("\n📋 数据摘要:")
        summary = processor.get_data_summary()
        for key, value in summary.items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for sub_key, sub_value in value.items():
                    print(f"    {sub_key}: {sub_value}")
            else:
                print(f"  {key}: {value}")
        
        # 2. 交易分析
        print("\n📈 步骤2: 交易绩效分析")
        analyzer = TradeAnalyzer(data)
        
        # 盈亏分析
        print("\n💰 盈亏分析:")
        pnl_stats = analyzer.calculate_pnl_statistics()
        for key, value in pnl_stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")
        
        # 回撤分析
        print("\n📉 回撤分析:")
        drawdown_stats = analyzer.calculate_drawdown()
        for key, value in drawdown_stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")
        
        # 风险指标
        print("\n⚠️ 风险指标:")
        risk_metrics = analyzer.calculate_risk_metrics()
        for key, value in risk_metrics.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")
        
        # 交易频率分析
        print("\n⏰ 交易频率分析:")
        freq_stats = analyzer.analyze_trading_frequency()
        for key, value in freq_stats.items():
            if not isinstance(value, dict):
                print(f"  {key}: {value}")
        
        # 最佳和最差交易
        print("\n🏆 最佳和最差交易:")
        best_worst = analyzer.find_best_worst_trades(3)
        
        print("  最佳交易:")
        for i, trade in enumerate(best_worst.get("最佳交易", []), 1):
            print(f"    {i}. 日期: {trade.get('date')}, 盈亏: {trade.get('closed_pnl'):.4f}")
        
        print("  最差交易:")
        for i, trade in enumerate(best_worst.get("最差交易", []), 1):
            print(f"    {i}. 日期: {trade.get('date')}, 盈亏: {trade.get('closed_pnl'):.4f}")
        
        # 3. 可视化分析
        print("\n📊 步骤3: 生成可视化图表")
        visualizer = TradeVisualizer(data)
        
        # 创建图表输出目录
        charts_dir = "analysis_charts"
        os.makedirs(charts_dir, exist_ok=True)
        
        # 生成所有图表
        print(f"  正在生成图表到目录: {charts_dir}")
        visualizer.save_all_charts(charts_dir)
        
        # 4. 生成综合报告
        print("\n📑 步骤4: 生成综合报告")
        report = analyzer.generate_performance_report()
        
        # 保存JSON报告
        report_filename = f"trade_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"✅ 综合报告已保存: {report_filename}")
        
        # 5. 显示关键结论
        print("\n🎯 关键结论:")
        print("=" * 30)
        
        # 绩效总结
        total_pnl = pnl_stats.get("总盈亏", 0)
        win_rate = pnl_stats.get("胜率", 0)
        profit_loss_ratio = pnl_stats.get("盈亏比", 0)
        max_drawdown = drawdown_stats.get("最大回撤金额", 0)
        sharpe_ratio = risk_metrics.get("夏普比率", 0)
        
        print(f"📊 交易绩效:")
        print(f"  • 总盈亏: {total_pnl:.4f}")
        print(f"  • 胜率: {win_rate:.2f}%")
        print(f"  • 盈亏比: {profit_loss_ratio:.2f}")
        print(f"  • 最大回撤: {max_drawdown:.4f}")
        print(f"  • 夏普比率: {sharpe_ratio:.4f}")
        
        # 绩效评估
        print(f"\n🏅 绩效评估:")
        if total_pnl > 0:
            print("  ✅ 总体盈利")
        else:
            print("  ❌ 总体亏损")
        
        if win_rate > 50:
            print("  ✅ 胜率超过50%")
        else:
            print("  ⚠️ 胜率低于50%")
        
        if profit_loss_ratio > 1:
            print("  ✅ 盈亏比大于1")
        else:
            print("  ⚠️ 盈亏比小于1")
        
        if sharpe_ratio > 1:
            print("  ✅ 夏普比率优秀")
        elif sharpe_ratio > 0.5:
            print("  🔶 夏普比率良好")
        else:
            print("  ⚠️ 夏普比率需要改善")
        
        # 交易建议
        print(f"\n💡 交易建议:")
        if win_rate < 40:
            print("  • 考虑改进交易策略，提高胜率")
        if profit_loss_ratio < 1:
            print("  • 建议优化止盈止损比例，提高盈亏比")
        if abs(max_drawdown) > total_pnl * 0.2:
            print("  • 注意风险控制，回撤过大")
        if freq_stats.get("平均每日交易次数", 0) > 20:
            print("  • 交易频率较高，注意交易成本")
        
        print(f"\n🎉 分析完成！")
        print(f"📁 图表文件夹: {charts_dir}")
        print(f"📄 报告文件: {report_filename}")
        print(f"📝 日志文件: trade_analysis.log")
        
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
        
        print(f"✅ 文件分析完成")
        print(f"📊 交易笔数: {summary.get('总交易笔数', 'N/A')}")
        print(f"💰 总盈亏: {summary.get('总盈亏', 'N/A')}")
        print(f"🎯 胜率: {pnl_stats.get('胜率', 'N/A'):.2f}%")
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")

if __name__ == "__main__":
    main() 