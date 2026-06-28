import pandas as pd
import numpy as np

class Backtester:
    def __init__(self, initial_balance=10000.0, transaction_fee=0.001):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.crypto_held = 0.0
        self.transaction_fee = transaction_fee
        self.trade_history = []
        self.portfolio_values = []

    def execute_trade(self, action, current_price, date):
        """Updates portfolio state safely based on buy/sell commands."""
        if action == 'BUY' and self.current_balance > 0:
            cash_to_spend = self.current_balance * (1 - self.transaction_fee)
            self.crypto_held = cash_to_spend / current_price
            self.current_balance = 0.0
            self.trade_history.append({'Date': date, 'Type': 'BUY', 'Price': current_price, 'Crypto': self.crypto_held})
            
        elif action == 'SELL' and self.crypto_held > 0:
            gross_cash = self.crypto_held * current_price
            self.current_balance = gross_cash * (1 - self.transaction_fee)
            self.trade_history.append({'Date': date, 'Type': 'SELL', 'Price': current_price, 'Gross Cash': gross_cash})
            self.crypto_held = 0.0

    def run_simulation(self, signals_df):
        """Advances time and executes the state machine."""
        for date, row in signals_df.iterrows():
            current_price = row['Close']
            position = row['Positions']
            
            if position == 1.0:
                self.execute_trade('BUY', current_price, date)
            elif position == -1.0:
                self.execute_trade('SELL', current_price, date)
                
            total_value = self.current_balance + (self.crypto_held * current_price)
            self.portfolio_values.append({'Date': date, 'Total Value': total_value})

    def calculate_metrics(self):
        """Generates advanced financial ROI, Win/Loss, and Sharpe metrics."""
        if not self.portfolio_values: return None
        
        final_portfolio_value = self.portfolio_values[-1]['Total Value']
        roi = ((final_portfolio_value - self.initial_balance) / self.initial_balance) * 100
        
        # Drawdown calculations
        df_portfolio = pd.DataFrame(self.portfolio_values)
        df_portfolio['Peak'] = df_portfolio['Total Value'].cummax()
        df_portfolio['Drawdown'] = (df_portfolio['Total Value'] - df_portfolio['Peak']) / df_portfolio['Peak']
        max_drawdown = df_portfolio['Drawdown'].min() * 100
        
        # OPTION 2 CODE: Sharpe Ratio Calculation (Risk-Adjusted Return)
        df_portfolio['Daily_Return'] = df_portfolio['Total Value'].pct_change()
        daily_volatility = df_portfolio['Daily_Return'].std()
        
        if daily_volatility > 0:
            # Assuming an annualized Risk-Free Rate of 0% for simple crypto calculations
            sharpe_ratio = (df_portfolio['Daily_Return'].mean() / daily_volatility) * np.sqrt(252)
        else:
            sharpe_ratio = 0.0

        # OPTION 2 CODE: Win/Loss Ratio Calculation
        win_count = 0
        loss_count = 0
        
        # Group buy and sell segments to evaluate individual closed trade cycles
        if len(self.trade_history) >= 2:
            for i in range(1, len(self.trade_history), 2):
                if i < len(self.trade_history):
                    buy_price = self.trade_history[i-1]['Price']
                    sell_price = self.trade_history[i]['Price']
                    if sell_price > buy_price:
                        win_count += 1
                    else:
                        loss_count += 1
                        
        total_trades = win_count + loss_count
        win_ratio = (win_count / total_trades * 100) if total_trades > 0 else 0.0

        return {
            "Initial Balance": f"${self.initial_balance:,.2f}",
            "Final Balance": f"${final_portfolio_value:,.2f}",
            "ROI": f"{roi:.2f}%",
            "Maximum Drawdown": f"{max_drawdown:.2f}%",
            "Sharpe Ratio": f"{sharpe_ratio:.2f}",
            "Win Ratio": f"{win_ratio:.1f}% ({win_count}/{total_trades})"
        }