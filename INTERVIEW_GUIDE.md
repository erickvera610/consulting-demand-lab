# Interview Guide

## 60-second explanation

I built a next-day demand forecasting experiment on real UCI Bike Sharing data. I engineered only information available before the forecast day, including calendar cycles, lagged demand, and trailing averages, then used a chronological train/validation/test protocol. I compared a seasonal baseline, Ridge regression, a scikit-learn MLP, and a PyTorch MLP. The neural model improved over seasonal repetition, but Ridge achieved the best held-out MAE. I treat that as a strength of the experiment: model selection follows evidence instead of assuming deep learning must win.

## Questions I should be able to answer

- Why are random train/test splits inappropriate for this task?
- Which lag features are available at prediction time?
- What would leakage look like here?
- Why can Ridge outperform a neural network on this dataset?
- How does the PyTorch training loop differ from the scikit-learn MLP?
- What is rolling one-day forecasting versus fixed-origin forecasting?
- What would production monitoring need to detect demand drift?

## Strong limitation statement

The bike-sharing experiment uses one system and two years of data. It is a small CPU-scale forecasting benchmark, not proof of production demand forecasting or causal inference.

## 20-second recruiter version

Real time-series forecasting with chronological validation, lag features, baseline comparison, Ridge, neural networks, PyTorch, exported inference, Docker, API health checks, CI, and documented error cases.
