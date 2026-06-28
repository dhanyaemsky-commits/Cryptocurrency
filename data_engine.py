import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime

def fetch_and_clean_data(ticker="BTC-USD", start_date="2021-01-01", end_date=None):
    """Fetches historical crypto data up to a specified end date (defaults to today)."""
    print(f"Downloading data for {ticker}...")
    
    if end_date is None:
        end_date = datetime.date.today().strftime('%Y-%m-%d')
        
    df = yf.download(ticker, start=start_date, end=end_date)
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        
    df = df[['Close']].dropna()
    return df

# OPTION 3 CODE: Multi-Strategy Engine Handler Logic
def generate_signals(df, strategy_choice="Moving Average Crossover", short_window=20, long_window=50):
    """Generates trading metrics matching choice parameters."""
    signals = pd.DataFrame(index=df.index)
    signals['Close'] = df['Close']
    
    if strategy_choice == "Moving Average Crossover":
        signals['SMA_Short'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
        signals['SMA_Long'] = df['Close'].rolling(window=long_window, min_periods=1).mean()
        signals['Signal'] = np.where(signals['SMA_Short'] > signals['SMA_Long'], 1.0, 0.0)
        
    elif strategy_choice == "RSI Momentum":
        # Calculate Relative Strength Index
        change = df['Close'].diff()
        gain = np.where(change > 0, change, 0.0)
        loss = np.where(change < 0, -change, 0.0)
        
        avg_gain = pd.Series(gain, index=df.index).rolling(window=14, min_periods=1).mean()
        avg_loss = pd.Series(loss, index=df.index).rolling(window=14, min_periods=1).mean()
        
        rs = avg_gain / (avg_loss + 1e-10)
        signals['RSI'] = 100 - (100 / (1 + rs))
        
        # Basic state initialization
        sig = []
        current_state = 0.0 # 0 = cash out, 1 = holding crypto
        for rsi_val in signals['RSI']:
            if rsi_val < 30: # Oversold -> Buy
                current_state = 1.0
            elif rsi_val > 70: # Overbought -> Sell
                current_state = 0.0
            sig.append(current_state)
        signals['Signal'] = sig
        
    elif strategy_choice == "Pure AI Forecasting":
        # Predictive execution model 
        df_ml = df.copy()
        df_ml['Days'] = np.arange(len(df_ml))
        
        model = LinearRegression()
        model.fit(df_ml[['Days']], df_ml['Close'])
        
        # Calculate daily projections on current indices
        predictions = model.predict(df_ml[['Days']])
        signals['Pred_Trend'] = pd.Series(predictions, index=df.index).pct_change()
        signals['Signal'] = np.where(signals['Pred_Trend'] > 0, 1.0, 0.0)

    # Compute execution state transitions (1 for Buy, -1 for Sell)
    signals['Positions'] = signals['Signal'].diff().fillna(0.0)
    return signals

def get_live_price(ticker="BTC-USD"):
    """Fetches the current live market price."""
    ticker_data = yf.Ticker(ticker)
    todays_data = ticker_data.history(period='1d', interval='1m')
    if not todays_data.empty:
        return todays_data['Close'].iloc[-1]
    return None

def predict_future_prices(df, future_days=30, lookback_window=60):
    """Uses Rolling Windows and Intercept Anchoring to align forecasts with real market values."""
    df_ml = df.tail(lookback_window).copy()
    df_ml['Days'] = np.arange(len(df_ml))
    
    X = df_ml[['Days']]
    y = df_ml['Close']
    
    model = LinearRegression()
    model.fit(X, y)
    
    last_date = df.index[-1]
    future_dates = [last_date + datetime.timedelta(days=i) for i in range(1, future_days + 1)]
    
    future_X = np.arange(len(df_ml), len(df_ml) + future_days).reshape(-1, 1)
    raw_predictions = model.predict(future_X)
    
    actual_last_price = df['Close'].iloc[-1]
    price_difference = actual_last_price - raw_predictions[0]
    adjusted_predictions = raw_predictions + price_difference
    
    predictions_df = pd.DataFrame(index=future_dates, data={'Predicted_Close': adjusted_predictions})
    return predictions_df