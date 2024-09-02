import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate portfolio performance
def portfolio_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns * weights) * 252
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    return returns, std

# Function to perform Monte Carlo Simulation
def monte_carlo_simulation(mean_returns, cov_matrix, num_portfolios=10000, risk_free_rate=0.0175):
    num_assets = len(mean_returns)
    results = np.zeros((3, num_portfolios))
    weights_record = np.zeros((num_portfolios, num_assets))
    
    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        portfolio_return, portfolio_std_dev = portfolio_performance(weights, mean_returns, cov_matrix)
        results[0,i] = portfolio_return
        results[1,i] = portfolio_std_dev
        results[2,i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
        weights_record[i, :] = weights
        
        # Update progress bar
        if i % (num_portfolios // 100) == 0:
            st.progress(i / num_portfolios)
    
    return results, weights_record

# Streamlit app
st.title('Portfolio Optimization with Monte Carlo Simulation')

tickers_input = st.text_input('Enter stock tickers separated by commas', 'AAPL,MSFT,GOOGL,AMZN,TSLA,FB')
tickers = [ticker.strip() for ticker in tickers_input.split(',')]

# Date input widgets
start_date = st.date_input('Start Date', pd.to_datetime('2000-01-01'))
end_date = st.date_input('End Date', pd.to_datetime('2023-06-30'))

if len(tickers) >= 2:  # Ensure there are at least two tickers
    st.write("Fetching data...")
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    
    if data.empty:
        st.error('No data found for the given tickers and date range.')
    else:
        returns = data.pct_change().dropna()
        mean_returns = returns.mean()
        cov_matrix = returns.cov()
        
        st.subheader('Monte Carlo Simulation Results')
        
        # Use 10,000 simulations
        num_portfolios = 10000
        
        st.write("Running Monte Carlo simulation...")
        results, weights_record = monte_carlo_simulation(mean_returns, cov_matrix, num_portfolios)
        
        max_sharpe_idx = np.argmax(results[2])
        max_sharpe_ratio = results[2,max_sharpe_idx]
        optimal_weights = weights_record[max_sharpe_idx]
        
        st.write(f'Optimal Portfolio Weights for Maximum Sharpe Ratio: {max_sharpe_ratio:.2f}')
        for i, ticker in enumerate(tickers):
            st.write(f'{ticker}: {optimal_weights[i]:.2%}')
        
        # Plotting Efficient Frontier
        fig, ax = plt.subplots()
        scatter = ax.scatter(results[1,:], results[0,:], c=results[2,:], cmap='YlGnBu', marker='o')
        ax.scatter(results[1,max_sharpe_idx], results[0,max_sharpe_idx], c='red', marker='*', s=200)
        ax.set_title('Efficient Frontier')
        ax.set_xlabel('Volatility')
        ax.set_ylabel('Return')
        cbar = plt.colorbar(scatter)
        cbar.set_label('Sharpe Ratio')
        st.pyplot(fig)
        
        # Additional plot - Capital Market Line (CML)
        sharpe_ratio = results[2,max_sharpe_idx]
        cml_x = np.linspace(0, results[1,max_sharpe_idx], 100)
        cml_y = risk_free_rate + cml_x * sharpe_ratio
        
        fig, ax = plt.subplots()
        ax.plot(cml_x, cml_y, label='Capital Market Line (CML)', color='r')
        ax.scatter(results[1,max_sharpe_idx], results[0,max_sharpe_idx], c='red', marker='*', s=200)
        ax.set_title('Capital Market Line')
        ax.set_xlabel('Volatility')
        ax.set_ylabel('Return')
        ax.legend()
        st.pyplot(fig)

else:
    st.error('Please enter at least two stock tickers.')
