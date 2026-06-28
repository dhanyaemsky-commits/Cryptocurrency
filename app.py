import streamlit as st
import pandas as pd
import datetime
import time  
import plotly.graph_objects as go  # OPTION 1 REQUIRED IMPORT
import data_engine
from backtester import Backtester

st.set_page_config(page_title="Crypto Backtester", layout="wide")
st.title("📈 Algorithmic Trading Backtesting Engine")
st.markdown("Simulate automated execution models against real-time cryptocurrency historical structures.")

# --- Session State Memory (Crucial for Live Dashboards) ---
if 'run_sim' not in st.session_state:
    st.session_state.run_sim = False

# --- Sidebar Controls ---
st.sidebar.header("Simulation Parameters")
ticker = st.sidebar.text_input("Cryptocurrency Ticker", value="BTC-USD")

# OPTION 3 CODE: UI Strategy Choice Menu Selection Dropdown
strategy_mode = st.sidebar.selectbox(
    "Select Strategy Model",
    ["Moving Average Crossover", "RSI Momentum", "Pure AI Forecasting"]
)

start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2021-01-01"))
today = datetime.date.today()
end_date = st.sidebar.date_input("End Date", value=today)
initial_balance = st.sidebar.number_input("Starting Balance ($)", value=10000.0, step=1000.0)

# --- The Live Mode Toggle ---
st.sidebar.divider()
live_mode = st.sidebar.toggle("🔴 Enable Live Auto-Refresh (10s)")

if st.sidebar.button("Run Simulation"):
    st.session_state.run_sim = True

# --- Execution ---
if st.session_state.run_sim:
    
    with st.spinner(f"Fetching historical data for {ticker}..."):
        raw_data = data_engine.fetch_and_clean_data(ticker=ticker, start_date=start_date, end_date=end_date)
        
    # --- LIVE DATA & MACHINE LEARNING PREDICTION ---
    st.header("🔮 Live Market & AI Forecast")
    colA, colB = st.columns(2)
    
    with colA:
        live_price = data_engine.get_live_price(ticker)
        if live_price:
            st.metric(label=f"Current Live Price ({ticker})", value=f"${live_price:,.2f}")
        else:
            st.warning("Could not fetch live price data right now.")
    
    with colB:
        with st.spinner("Training Machine Learning Model..."):
            predictions = data_engine.predict_future_prices(raw_data, future_days=7)
            predictions.index = pd.to_datetime(predictions.index).strftime('%Y-%m-%d')
            st.dataframe(predictions.style.format("${:,.2f}"), use_container_width=True)
            
    st.line_chart(predictions['Predicted_Close'], color="#00ff00")
    st.divider()
    
    # --- BACKTESTING STRATEGY VIA MODULAR INPUT SELECTOR ---
    with st.spinner("Analyzing market signals..."):
        signals = data_engine.generate_signals(raw_data, strategy_choice=strategy_mode)

    with st.spinner("Running Backtest Simulation..."):
        engine = Backtester(initial_balance=initial_balance)
        engine.run_simulation(signals)
        metrics = engine.calculate_metrics()

    # --- Dashboard Visuals ---
    if metrics:
        st.header(f"📊 Performance Report — {strategy_mode}")
        
        # OPTION 2 CODE: Displaying the Risk profiles inside metrics row
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("Initial Balance", metrics["Initial Balance"])
        col2.metric("Final Balance", metrics["Final Balance"])
        col3.metric("Return on Investment", metrics["ROI"])
        col4.metric("Maximum Drawdown", metrics["Maximum Drawdown"])
        col5.metric("Sharpe Ratio (Risk Adj)", metrics["Sharpe Ratio"])
        col6.metric("Win/Loss Ratio", metrics["Win Ratio"])

        st.divider()

        # OPTION 1 CODE: Advanced Plotly Candlestick Interface with Buy/Sell Arrows
        st.subheader("Market Price Profile & Simulation Tracking Execution")
        
        portfolio_df = pd.DataFrame(engine.portfolio_values)
        portfolio_df.set_index('Date', inplace=True)
        
        # Merge execution contexts to capture prices mapped to dates
        chart_df = signals.copy()
        
        fig = go.Figure()
        
        # Draw market closing curve line
        fig.add_trace(go.Scatter(x=chart_df.index, y=chart_df['Close'], name='Market Price', line=dict(color='#4361ee', width=2)))
        
        # Isolate dates matching trade logs execution entries
        buys = chart_df[chart_df['Positions'] == 1.0]
        sells = chart_df[chart_df['Positions'] == -1.0]
        
        # Overlay buy points with upward green triangles
        fig.add_trace(go.Scatter(
            x=buys.index, y=buys['Close'], mode='markers', name='BUY Signal',
            marker=dict(symbol='triangle-up', size=13, color='#00ff00', line=dict(width=1, color='black'))
        ))
        
        # Overlay sell points with downward red triangles
        fig.add_trace(go.Scatter(
            x=sells.index, y=sells['Close'], mode='markers', name='SELL Signal',
            marker=dict(symbol='triangle-down', size=13, color='#ff007f', line=dict(width=1, color='black'))
        ))
        
        fig.update_layout(
            template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20), height=450, showlegend=True,
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#222')
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Portfolio Value Over Time ($)")
        st.line_chart(portfolio_df['Total Value'])

        # --- Cleaned Transaction Log ---
        st.subheader("Transaction Log")
        if engine.trade_history:
            trade_df = pd.DataFrame(engine.trade_history)
            
            if 'Action' in trade_df.columns:
                trade_df = trade_df.drop(columns=['Action'])
                
            if 'Date' in trade_df.columns:
                trade_df['Date'] = pd.to_datetime(trade_df['Date']).dt.strftime('%Y-%m-%d')
            
            st.dataframe(trade_df, use_container_width=True)
            
            csv_data = trade_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Transaction Log to CSV",
                data=csv_data,
                file_name=f"{ticker}_backtest_log.csv",
                mime="text/csv"
            )

    # --- THE AUTO-REFRESH LOOP ---
    if live_mode:
        time.sleep(10)
        st.rerun()