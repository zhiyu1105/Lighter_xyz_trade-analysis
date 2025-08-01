"""
Trading Analysis Web Application
Streamlit-based user interface
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

# Configure page
st.set_page_config(
    page_title="Trading Data Analysis Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set up logging
logging.basicConfig(level=logging.INFO)

def get_data_files():
    """Get available data files from data folder"""
    data_dir = "data"
    if not os.path.exists(data_dir):
        return []
    
    files = []
    # Find CSV files
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    files.extend(csv_files)
    
    # Find Excel files
    excel_files = glob.glob(os.path.join(data_dir, "*.xlsx"))
    excel_files.extend(glob.glob(os.path.join(data_dir, "*.xls")))
    files.extend(excel_files)
    
    return sorted(files)

def main():
    st.title("📈 Trading Data Analysis Platform")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("Function Menu")
        
        # Data selection
        st.subheader("📁 Data Selection")
        
        # Get files from data folder
        data_files = get_data_files()
        
        if data_files:
            st.write("📂 Files in data folder:")
            selected_file = st.selectbox(
                "Select data file",
                data_files,
                format_func=lambda x: os.path.basename(x)
            )
            
            if st.button("📊 Analyze selected file"):
                st.session_state['selected_file'] = selected_file
                st.session_state['analysis_ready'] = True
                st.rerun()
        else:
            st.warning("📁 No data files found in data folder")
            st.info("Please place your trading data files in the data folder")
        
        # File upload
        st.subheader("📤 Upload new file")
        uploaded_file = st.file_uploader(
            "Select trading data file",
            type=['csv', 'xlsx', 'xls'],
            help="Supports CSV and Excel formats"
        )
        
        if uploaded_file is not None:
            st.session_state['uploaded_file'] = uploaded_file
            st.session_state['analysis_ready'] = True
            st.rerun()
        
        # Analysis options
        st.subheader("📊 Analysis Options")
        analysis_type = st.selectbox(
            "Select analysis type",
            ["Overview Analysis", "P&L Analysis", "Risk Analysis", "Trading Frequency Analysis", "Position Analysis", "Visualization Analysis"]
        )
        
        # Chart options
        st.subheader("📈 Chart Options")
        chart_interactive = st.checkbox("Interactive charts", value=True, help="Use Plotly to generate interactive charts")
        
        # Data management
        st.subheader("🗂️ Data Management")
        if st.button("📂 Open data folder"):
            data_dir = os.path.abspath("data")
            st.info(f"Data folder path: {data_dir}")
            st.code(f"open {data_dir}")
    
    # Main content area
    if 'analysis_ready' in st.session_state and st.session_state['analysis_ready']:
        try:
            # Data processing
            processor = TradeDataProcessor()
            
            # Determine data source
            if 'selected_file' in st.session_state:
                # Use file from data folder
                file_path = st.session_state['selected_file']
                file_name = os.path.basename(file_path)
                st.success(f"📁 Analyzing file: {file_name}")
                
                if file_path.endswith('.csv'):
                    data = processor.load_csv(file_path)
                else:
                    data = processor.load_excel(file_path)
                    
            elif 'uploaded_file' in st.session_state:
                # Use uploaded file
                uploaded_file = st.session_state['uploaded_file']
                st.success(f"📤 Analyzing uploaded file: {uploaded_file.name}")
                
                # Save uploaded file to temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Load data
                if uploaded_file.name.endswith('.csv'):
                    data = processor.load_csv(tmp_file_path)
                else:
                    data = processor.load_excel(tmp_file_path)
                
                # Clean up temporary file
                os.unlink(tmp_file_path)
            else:
                st.error("No data file selected")
                return
            
            # Display data overview
            st.header("📋 Data Overview")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Trades", len(data))
            with col2:
                if 'closed_pnl' in data.columns:
                    total_pnl = data['closed_pnl'].sum()
                    st.metric("Total P&L", f"{total_pnl:.4f}")
                else:
                    st.metric("Total P&L", "N/A")
            with col3:
                if 'date' in data.columns:
                    date_range = (data['date'].max() - data['date'].min()).days
                    st.metric("Data Days", f"{date_range} days")
                else:
                    st.metric("Data Days", "N/A")
            
            # Display data sample
            st.subheader("Data Sample")
            st.dataframe(data.head(10), use_container_width=True)
            
            # Data summary
            summary = processor.get_data_summary()
            with st.expander("View detailed data summary"):
                st.json(summary)
            
            # Analyzer and visualizer
            analyzer = TradeAnalyzer(data)
            visualizer = TradeVisualizer(data)
            
            st.markdown("---")
            
            # Display content based on selected analysis type
            if analysis_type == "Overview Analysis":
                show_overview_analysis(analyzer, data)
                
            elif analysis_type == "P&L Analysis":
                show_pnl_analysis(analyzer, visualizer, chart_interactive)
                
            elif analysis_type == "Risk Analysis":
                show_risk_analysis(analyzer, visualizer, chart_interactive)
                
            elif analysis_type == "Trading Frequency Analysis":
                show_frequency_analysis(analyzer, visualizer, chart_interactive)
                
            elif analysis_type == "Position Analysis":
                show_position_analysis(analyzer, visualizer, chart_interactive)
                
            elif analysis_type == "Visualization Analysis":
                show_visualization_analysis(visualizer, chart_interactive)
            
            # Generate comprehensive report
            st.markdown("---")
            st.header("📑 Comprehensive Report")
            if st.button("Generate complete analysis report"):
                with st.spinner("Generating report..."):
                    report = analyzer.generate_performance_report()
                    
                    # Display report
                    st.subheader("Trading Performance Comprehensive Report")
                    
                    # Basic information
                    st.write("**Report Basic Information**")
                    st.json(report["Data Overview"])
                    
                    # Main metrics
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**P&L Analysis**")
                        st.json(report["P&L Analysis"])
                        
                        st.write("**Trading Frequency Analysis**")
                        st.json(report["Trading Frequency Analysis"])
                    
                    with col2:
                        st.write("**Drawdown Analysis**")
                        st.json(report["Drawdown Analysis"])
                        
                        st.write("**Risk Metrics**")
                        st.json(report["Risk Metrics"])
                    
                    # Download report
                    report_json = json.dumps(report, ensure_ascii=False, indent=2, default=str)
                    st.download_button(
                        label="📥 Download JSON Report",
                        data=report_json,
                        file_name=f"trade_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            
        except Exception as e:
            st.error(f"Data processing error: {e}")
            st.error("Please check if the file format is correct and contains necessary columns (such as Date, Closed PnL, etc.)")
    
    else:
        # Display usage instructions
        st.header("🚀 Usage Instructions")
        
        # Check data folder
        data_files = get_data_files()
        if data_files:
            st.success(f"✅ Found {len(data_files)} data files in data folder")
            st.write("**Available files:**")
            for file in data_files:
                st.write(f"- {os.path.basename(file)}")
        else:
            st.warning("⚠️ No data files found in data folder")
            st.info("Please place your trading data files in the data folder")
        
        st.markdown("""
        ### Welcome to the Trading Data Analysis Platform!
        
        #### 📊 Feature Highlights
        - **Data Import**: Supports CSV and Excel format trading data
        - **Comprehensive Analysis**: Provides P&L, risk, frequency, position and other multi-dimensional analysis
        - **Visualization**: Rich chart display with interactive chart support
        - **Report Generation**: One-click comprehensive analysis report generation
        
        #### 📁 Data Format Requirements
        Your trading data file should contain the following columns (column names are case-insensitive):
        
        | Column Name | Description | Required |
        |-------------|-------------|----------|
        | Market | Market/Instrument | Optional |
        | Side | Trade Direction | Optional |
        | Date | Trade Date/Time | **Required** |
        | Trade Value | Trade Value | Optional |
        | Size | Trade Size | Optional |
        | Price | Trade Price | Optional |
        | Closed PnL | Realized P&L | **Required** |
        | Fee | Transaction Fee | Optional |
        | Role | Role (Maker/Taker) | Optional |
        
        #### 🎯 Usage Steps
        1. **Place Data**: Put trading data files in the data folder
        2. **Select File**: Choose the data file to analyze from the left sidebar
        3. **Choose Analysis**: Select the analysis type you're interested in
        4. **View Results**: Browse analysis results and charts
        5. **Generate Report**: Click to generate complete analysis report
        
        #### 💡 Tips
        - Loading may take a few seconds for large datasets
        - Interactive charts support zoom, pan and other operations
        - You can download generated analysis reports for later use
        - Supports comparison analysis of multiple data files
        """)

def show_overview_analysis(analyzer, data):
    """Display overview analysis"""
    st.header("📋 Overview Analysis")
    
    # Basic statistics
    col1, col2, col3, col4 = st.columns(4)
    
    if 'closed_pnl' in data.columns:
        pnl_stats = analyzer.calculate_pnl_statistics()
        
        with col1:
            st.metric("Win Rate", f"{pnl_stats.get('win_rate', 0):.2f}%")
        with col2:
            st.metric("Profit Factor", f"{pnl_stats.get('profit_factor', 0):.2f}")
        with col3:
            st.metric("Max Profit", f"{pnl_stats.get('max_profit', 0):.4f}")
        with col4:
            st.metric("Max Loss", f"{pnl_stats.get('max_loss', 0):.4f}")
    
    # Best and worst trades
    best_worst = analyzer.find_best_worst_trades(5)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Best Trades (Top 5)")
        if "best_trades" in best_worst:
            st.dataframe(pd.DataFrame(best_worst["best_trades"]))
    
    with col2:
        st.subheader("😞 Worst Trades (Top 5)")
        if "worst_trades" in best_worst:
            st.dataframe(pd.DataFrame(best_worst["worst_trades"]))

def show_pnl_analysis(analyzer, visualizer, interactive):
    """Display P&L analysis"""
    st.header("💰 P&L Analysis")
    
    # P&L statistics
    pnl_stats = analyzer.calculate_pnl_statistics()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Basic Statistics")
        st.json(pnl_stats)
    
    with col2:
        st.subheader("Drawdown Analysis")
        drawdown_stats = analyzer.calculate_drawdown()
        st.json(drawdown_stats)
    
    with col3:
        st.subheader("Trade Size Analysis")
        size_stats = analyzer.analyze_trade_sizes()
        st.json(size_stats)
    
    # P&L curve chart
    st.subheader("📈 P&L Curve")
    fig = visualizer.plot_pnl_curve(interactive=interactive)
    if fig:
        if interactive:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.pyplot(fig)
    
    # P&L distribution chart
    st.subheader("📊 P&L Distribution")
    fig = visualizer.plot_pnl_distribution()
    if fig:
        st.pyplot(fig)

def show_risk_analysis(analyzer, visualizer, interactive):
    """Display risk analysis"""
    st.header("⚠️ Risk Analysis")
    
    risk_metrics = analyzer.calculate_risk_metrics()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Risk Metrics")
        st.json(risk_metrics)
    
    with col2:
        st.subheader("Risk Assessment")
        
        # Provide assessment based on metrics
        sharpe = risk_metrics.get("sharpe_ratio", 0)
        max_dd = risk_metrics.get("max_drawdown_percentage", 0)
        
        if sharpe > 1:
            st.success(f"Sharpe Ratio {sharpe:.2f} - Good risk-adjusted returns")
        elif sharpe > 0.5:
            st.warning(f"Sharpe Ratio {sharpe:.2f} - Average risk-adjusted returns")
        else:
            st.error(f"Sharpe Ratio {sharpe:.2f} - Poor risk-adjusted returns")
        
        if abs(max_dd) < 5:
            st.success(f"Max Drawdown {max_dd:.2f}% - Good drawdown control")
        elif abs(max_dd) < 15:
            st.warning(f"Max Drawdown {max_dd:.2f}% - Moderate drawdown")
        else:
            st.error(f"Max Drawdown {max_dd:.2f}% - Large drawdown, need to pay attention to risk control")

def show_frequency_analysis(analyzer, visualizer, interactive):
    """Display trading frequency analysis"""
    st.header("⏰ Trading Frequency Analysis")
    
    freq_stats = analyzer.analyze_trading_frequency()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Frequency Statistics")
        st.json(freq_stats)
    
    with col2:
        st.subheader("Time Distribution")
        if "hourly_trade_distribution" in freq_stats:
            hourly_data = freq_stats["hourly_trade_distribution"]
            hourly_df = pd.DataFrame(list(hourly_data.items()), columns=['Hour', 'Trade Count'])
            st.bar_chart(hourly_df.set_index('Hour'))
    
    # Trading frequency chart
    st.subheader("📅 Trading Frequency Chart")
    fig = visualizer.plot_trading_frequency()
    if fig:
        st.pyplot(fig)

def show_position_analysis(analyzer, visualizer, interactive):
    """Display position analysis"""
    st.header("📍 Position Analysis")
    
    position_stats = analyzer.analyze_position_changes()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Position Statistics")
        st.json(position_stats)
    
    with col2:
        st.subheader("Position Distribution")
        if "position_change_distribution" in position_stats:
            pos_data = position_stats["position_change_distribution"]
            pos_df = pd.DataFrame(list(pos_data.items()), columns=['Position Type', 'Count'])
            st.bar_chart(pos_df.set_index('Position Type'))
    
    # Position analysis chart
    st.subheader("📊 Position Analysis Chart")
    fig = visualizer.plot_position_analysis()
    if fig:
        st.pyplot(fig)

def show_visualization_analysis(visualizer, interactive):
    """Display visualization analysis"""
    st.header("📈 Visualization Analysis")
    
    # Price trend chart
    st.subheader("💹 Price Trend")
    fig = visualizer.plot_price_chart(interactive=interactive)
    if fig:
        if interactive:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.pyplot(fig)
    
    # Comprehensive dashboard
    st.subheader("🎛️ Comprehensive Dashboard")
    fig = visualizer.create_dashboard()
    if fig:
        st.pyplot(fig)

if __name__ == "__main__":
    main() 