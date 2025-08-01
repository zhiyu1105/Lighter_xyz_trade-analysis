"""
交易分析网页应用
基于Streamlit的用户界面
streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import logging
import os
import tempfile
import glob

from trade_analyzer import TradeDataProcessor, TradeAnalyzer, TradeVisualizer

# 配置页面
st.set_page_config(
    page_title="交易数据分析平台",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 设置日志
logging.basicConfig(level=logging.INFO)

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

def main():
    st.title("📈 交易数据分析平台")
    st.markdown("---")
    
    # 侧边栏
    with st.sidebar:
        st.header("功能菜单")
        
        # 数据选择
        st.subheader("📁 数据选择")
        
        # 获取data文件夹中的文件
        data_files = get_data_files()
        
        if data_files:
            st.write("📂 数据文件夹中的文件：")
            selected_file = st.selectbox(
                "选择数据文件",
                data_files,
                format_func=lambda x: os.path.basename(x)
            )
            
            if st.button("📊 分析选中文件"):
                st.session_state['selected_file'] = selected_file
                st.session_state['analysis_ready'] = True
                st.rerun()
        else:
            st.warning("📁 data文件夹中没有找到数据文件")
            st.info("请将你的交易数据文件放入data文件夹中")
        
        # 文件上传
        st.subheader("📤 上传新文件")
        uploaded_file = st.file_uploader(
            "选择交易数据文件",
            type=['csv', 'xlsx', 'xls'],
            help="支持CSV和Excel格式"
        )
        
        if uploaded_file is not None:
            st.session_state['uploaded_file'] = uploaded_file
            st.session_state['analysis_ready'] = True
            st.rerun()
        
        # 分析选项
        st.subheader("📊 分析选项")
        analysis_type = st.selectbox(
            "选择分析类型",
            ["概览分析", "盈亏分析", "风险分析", "交易频率分析", "持仓分析", "可视化分析"]
        )
        
        # 图表选项
        st.subheader("📈 图表选项")
        chart_interactive = st.checkbox("交互式图表", value=True, help="使用Plotly生成交互式图表")
        
        # 数据管理
        st.subheader("🗂️ 数据管理")
        if st.button("📂 打开数据文件夹"):
            data_dir = os.path.abspath("data")
            st.info(f"数据文件夹路径：{data_dir}")
            st.code(f"open {data_dir}")
    
    # 主内容区
    if 'analysis_ready' in st.session_state and st.session_state['analysis_ready']:
        try:
            # 数据处理
            processor = TradeDataProcessor()
            
            # 确定数据源
            if 'selected_file' in st.session_state:
                # 使用data文件夹中的文件
                file_path = st.session_state['selected_file']
                file_name = os.path.basename(file_path)
                st.success(f"📁 正在分析文件：{file_name}")
                
                if file_path.endswith('.csv'):
                    data = processor.load_csv(file_path)
                else:
                    data = processor.load_excel(file_path)
                    
            elif 'uploaded_file' in st.session_state:
                # 使用上传的文件
                uploaded_file = st.session_state['uploaded_file']
                st.success(f"📤 正在分析上传文件：{uploaded_file.name}")
                
                # 保存上传的文件到临时位置
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # 加载数据
                if uploaded_file.name.endswith('.csv'):
                    data = processor.load_csv(tmp_file_path)
                else:
                    data = processor.load_excel(tmp_file_path)
                
                # 清理临时文件
                os.unlink(tmp_file_path)
            else:
                st.error("没有选择数据文件")
                return
            
            # 显示数据概览
            st.header("📋 数据概览")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("总交易笔数", len(data))
            with col2:
                if 'closed_pnl' in data.columns:
                    total_pnl = data['closed_pnl'].sum()
                    st.metric("总盈亏", f"{total_pnl:.4f}")
                else:
                    st.metric("总盈亏", "N/A")
            with col3:
                if 'date' in data.columns:
                    date_range = (data['date'].max() - data['date'].min()).days
                    st.metric("数据天数", f"{date_range}天")
                else:
                    st.metric("数据天数", "N/A")
            
            # 显示数据样本
            st.subheader("数据样本")
            st.dataframe(data.head(10), use_container_width=True)
            
            # 数据摘要
            summary = processor.get_data_summary()
            with st.expander("查看详细数据摘要"):
                st.json(summary)
            
            # 分析器和可视化器
            analyzer = TradeAnalyzer(data)
            visualizer = TradeVisualizer(data)
            
            st.markdown("---")
            
            # 根据选择的分析类型显示内容
            if analysis_type == "概览分析":
                show_overview_analysis(analyzer, data)
                
            elif analysis_type == "盈亏分析":
                show_pnl_analysis(analyzer, visualizer, chart_interactive)
                
            elif analysis_type == "风险分析":
                show_risk_analysis(analyzer, visualizer, chart_interactive)
                
            elif analysis_type == "交易频率分析":
                show_frequency_analysis(analyzer, visualizer, chart_interactive)
                
            elif analysis_type == "持仓分析":
                show_position_analysis(analyzer, visualizer, chart_interactive)
                
            elif analysis_type == "可视化分析":
                show_visualization_analysis(visualizer, chart_interactive)
            
            # 生成综合报告
            st.markdown("---")
            st.header("📑 综合报告")
            if st.button("生成完整分析报告"):
                with st.spinner("正在生成报告..."):
                    report = analyzer.generate_performance_report()
                    
                    # 显示报告
                    st.subheader("交易绩效综合报告")
                    
                    # 基本信息
                    st.write("**报告基本信息**")
                    st.json(report["数据概览"])
                    
                    # 主要指标
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**盈亏分析**")
                        st.json(report["盈亏分析"])
                        
                        st.write("**交易频率分析**")
                        st.json(report["交易频率分析"])
                    
                    with col2:
                        st.write("**回撤分析**")
                        st.json(report["回撤分析"])
                        
                        st.write("**风险指标**")
                        st.json(report["风险指标"])
                    
                    # 下载报告
                    report_json = json.dumps(report, ensure_ascii=False, indent=2, default=str)
                    st.download_button(
                        label="📥 下载JSON报告",
                        data=report_json,
                        file_name=f"trade_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            
        except Exception as e:
            st.error(f"数据处理错误: {e}")
            st.error("请检查文件格式是否正确，确保包含必要的列（如Date, Closed PnL等）")
    
    else:
        # 显示使用说明
        st.header("🚀 使用说明")
        
        # 检查data文件夹
        data_files = get_data_files()
        if data_files:
            st.success(f"✅ 在data文件夹中找到 {len(data_files)} 个数据文件")
            st.write("**可用文件：**")
            for file in data_files:
                st.write(f"- {os.path.basename(file)}")
        else:
            st.warning("⚠️ data文件夹中没有找到数据文件")
            st.info("请将你的交易数据文件放入data文件夹中")
        
        st.markdown("""
        ### 欢迎使用交易数据分析平台！
        
        #### 📊 功能特色
        - **数据导入**: 支持CSV和Excel格式的交易数据
        - **全面分析**: 提供盈亏、风险、频率、持仓等多维度分析
        - **可视化**: 丰富的图表展示，支持交互式图表
        - **报告生成**: 一键生成综合分析报告
        
        #### 📁 数据格式要求
        你的交易数据文件应包含以下列（列名不区分大小写）：
        
        | 列名 | 说明 | 必需 |
        |------|------|------|
        | Market | 市场/品种 | 可选 |
        | Side | 交易方向 | 可选 |
        | Date | 交易日期时间 | **必需** |
        | Trade Value | 交易价值 | 可选 |
        | Size | 交易数量 | 可选 |
        | Price | 交易价格 | 可选 |
        | Closed PnL | 已实现盈亏 | **必需** |
        | Fee | 手续费 | 可选 |
        | Role | 角色(Maker/Taker) | 可选 |
        
        #### 🎯 使用步骤
        1. **放置数据**: 将交易数据文件放入data文件夹
        2. **选择文件**: 在左侧选择要分析的数据文件
        3. **选择分析**: 选择你感兴趣的分析类型
        4. **查看结果**: 浏览分析结果和图表
        5. **生成报告**: 点击生成完整分析报告
        
        #### 💡 提示
        - 数据量大时加载可能需要几秒钟
        - 交互式图表支持缩放、平移等操作
        - 可以下载生成的分析报告供后续使用
        - 支持多个数据文件进行对比分析
        """)

def show_overview_analysis(analyzer, data):
    """显示概览分析"""
    st.header("📋 概览分析")
    
    # 基本统计
    col1, col2, col3, col4 = st.columns(4)
    
    if 'closed_pnl' in data.columns:
        pnl_stats = analyzer.calculate_pnl_statistics()
        
        with col1:
            st.metric("胜率", f"{pnl_stats.get('胜率', 0):.2f}%")
        with col2:
            st.metric("盈亏比", f"{pnl_stats.get('盈亏比', 0):.2f}")
        with col3:
            st.metric("最大盈利", f"{pnl_stats.get('最大单笔盈利', 0):.4f}")
        with col4:
            st.metric("最大亏损", f"{pnl_stats.get('最大单笔亏损', 0):.4f}")
    
    # 最佳和最差交易
    best_worst = analyzer.find_best_worst_trades(5)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 最佳交易（前5）")
        if "最佳交易" in best_worst:
            st.dataframe(pd.DataFrame(best_worst["最佳交易"]))
    
    with col2:
        st.subheader("😞 最差交易（前5）")
        if "最差交易" in best_worst:
            st.dataframe(pd.DataFrame(best_worst["最差交易"]))

def show_pnl_analysis(analyzer, visualizer, interactive):
    """显示盈亏分析"""
    st.header("💰 盈亏分析")
    
    # 盈亏统计
    pnl_stats = analyzer.calculate_pnl_statistics()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("基本统计")
        st.json(pnl_stats)
    
    with col2:
        st.subheader("回撤分析")
        drawdown_stats = analyzer.calculate_drawdown()
        st.json(drawdown_stats)
    
    with col3:
        st.subheader("交易规模")
        size_stats = analyzer.analyze_trade_sizes()
        st.json(size_stats)
    
    # 盈亏曲线图
    st.subheader("📈 盈亏曲线")
    fig = visualizer.plot_pnl_curve(interactive=interactive)
    if fig:
        if interactive:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.pyplot(fig)
    
    # 盈亏分布图
    st.subheader("📊 盈亏分布")
    fig = visualizer.plot_pnl_distribution()
    if fig:
        st.pyplot(fig)

def show_risk_analysis(analyzer, visualizer, interactive):
    """显示风险分析"""
    st.header("⚠️ 风险分析")
    
    risk_metrics = analyzer.calculate_risk_metrics()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("风险指标")
        st.json(risk_metrics)
    
    with col2:
        st.subheader("风险评估")
        
        # 根据指标给出评估
        sharpe = risk_metrics.get("夏普比率", 0)
        max_dd = risk_metrics.get("最大回撤百分比", 0)
        
        if sharpe > 1:
            st.success(f"夏普比率 {sharpe:.2f} - 风险调整后收益良好")
        elif sharpe > 0.5:
            st.warning(f"夏普比率 {sharpe:.2f} - 风险调整后收益一般")
        else:
            st.error(f"夏普比率 {sharpe:.2f} - 风险调整后收益较差")
        
        if abs(max_dd) < 5:
            st.success(f"最大回撤 {max_dd:.2f}% - 回撤控制良好")
        elif abs(max_dd) < 15:
            st.warning(f"最大回撤 {max_dd:.2f}% - 回撤适中")
        else:
            st.error(f"最大回撤 {max_dd:.2f}% - 回撤较大，需要注意风险控制")

def show_frequency_analysis(analyzer, visualizer, interactive):
    """显示交易频率分析"""
    st.header("⏰ 交易频率分析")
    
    freq_stats = analyzer.analyze_trading_frequency()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("频率统计")
        st.json(freq_stats)
    
    with col2:
        st.subheader("时间分布")
        if "每小时交易分布" in freq_stats:
            hourly_data = freq_stats["每小时交易分布"]
            hourly_df = pd.DataFrame(list(hourly_data.items()), columns=['小时', '交易次数'])
            st.bar_chart(hourly_df.set_index('小时'))
    
    # 交易频率图表
    st.subheader("📅 交易频率图表")
    fig = visualizer.plot_trading_frequency()
    if fig:
        st.pyplot(fig)

def show_position_analysis(analyzer, visualizer, interactive):
    """显示持仓分析"""
    st.header("📍 持仓分析")
    
    position_stats = analyzer.analyze_position_changes()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("持仓统计")
        st.json(position_stats)
    
    with col2:
        st.subheader("持仓分布")
        if "持仓变化分布" in position_stats:
            pos_data = position_stats["持仓变化分布"]
            pos_df = pd.DataFrame(list(pos_data.items()), columns=['持仓类型', '次数'])
            st.bar_chart(pos_df.set_index('持仓类型'))
    
    # 持仓分析图表
    st.subheader("📊 持仓分析图表")
    fig = visualizer.plot_position_analysis()
    if fig:
        st.pyplot(fig)

def show_visualization_analysis(visualizer, interactive):
    """显示可视化分析"""
    st.header("📈 可视化分析")
    
    # 价格走势图
    st.subheader("💹 价格走势")
    fig = visualizer.plot_price_chart(interactive=interactive)
    if fig:
        if interactive:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.pyplot(fig)
    
    # 综合仪表板
    st.subheader("🎛️ 综合仪表板")
    fig = visualizer.create_dashboard()
    if fig:
        st.pyplot(fig)

if __name__ == "__main__":
    main() 