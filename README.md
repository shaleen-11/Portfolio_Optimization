# Portfolio_Optimization

## Overview

This project presents a portfolio optimization app built using Streamlit and Python, designed to help users optimize their investment portfolios based on historical stock data. The app leverages Monte Carlo simulations and the Markowitz Efficient Frontier to determine the optimal allocation of assets in a portfolio to maximize the Sharpe ratio.

## Features

- **Monte Carlo Simulation:** Executes up to 50,000 Monte Carlo simulations to construct the Markowitz Efficient Frontier, analyzing risk-return trade-offs.
- **Optimal Portfolio Weights:** Calculates the optimal portfolio weights by maximizing the Sharpe ratio, providing an expected annual return and volatility.
- **Capital Market Line (CML):** Plots the Capital Market Line to visualize the portfolio’s optimal position relative to other portfolios.
- **Interactive App:** Allows users to input any number of stock tickers and date ranges to get personalized investment ratios.

## Project Details

### Portfolio Optimization

- **Historical Data:** Utilizes 23 years of historical data from Yahoo Finance to calculate optimal portfolio weights.
- **Return and Volatility:** Achieves an expected annual return of 32% with a volatility of 1%.
- **Sharpe Ratio:** Maximizes the Sharpe ratio to determine the optimal portfolio allocation.

### Monte Carlo Simulation

- **Simulations:** Conducts 50,000 simulations to build the Efficient Frontier, providing a comprehensive analysis of various portfolio configurations.
- **Risk-Return Analysis:** Evaluates the risk-return trade-offs of different portfolio allocations.

### Capital Market Line (CML)

- **Visualization:** Plots the CML to show the optimal risk-return trade-off relative to other portfolios, enhancing decision-making for investors.
