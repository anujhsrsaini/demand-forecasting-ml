import os
import pandas as pd
import numpy as np

def build_features(df_raw):
    """
    Builds weekly category-level features for demand forecasting.
    Maintains strict temporal hygiene to prevent data leakage.
    
    Parameters:
    df_raw (pd.DataFrame): Raw transaction data containing:
                           - created_at: order timestamp
                           - qty: ordered quantity
                           - unit_price: unit price
                           - category_name: product category
    
    Returns:
    pd.DataFrame: Feature DataFrame with one row per (week_start x category_name)
    """
    # 1. Convert timestamp and extract Monday-based week start
    df = df_raw.copy()
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['week_start'] = df['created_at'].dt.to_period('W').dt.start_time
    
    # 2. Aggregate to weekly category-level
    weekly = df.groupby(['week_start', 'category_name']).agg(
        qty=('qty', 'sum'),
        avg_price=('unit_price', 'mean')
    ).reset_index()
    
    # 3. Sort by category and week to ensure time-series order
    weekly = weekly.sort_values(by=['category_name', 'week_start']).reset_index(drop=True)
    
    # 4. Generate features per category group
    # All demand/price variables are shifted by at least 1 week BEFORE any aggregation to prevent leakage
    grouped = weekly.groupby('category_name')
    
    # Lags
    weekly['qty_lag_1'] = grouped['qty'].shift(1)
    weekly['qty_lag_2'] = grouped['qty'].shift(2)
    weekly['qty_lag_3'] = grouped['qty'].shift(3)
    weekly['qty_lag_4'] = grouped['qty'].shift(4)
    
    # Rolling stats (note: we shift first, then roll, to avoid leakage)
    weekly['qty_roll_mean_2'] = grouped['qty'].transform(lambda x: x.shift(1).rolling(2).mean())
    weekly['qty_roll_std_2'] = grouped['qty'].transform(lambda x: x.shift(1).rolling(2).std())
    weekly['qty_roll_mean_4'] = grouped['qty'].transform(lambda x: x.shift(1).rolling(4).mean())
    weekly['qty_roll_std_4'] = grouped['qty'].transform(lambda x: x.shift(1).rolling(4).std())
    
    # Lagged pricing
    weekly['price_lag_1'] = grouped['avg_price'].shift(1)
    
    # Category target encoding (expanding mean of prior demand)
    weekly['category_expanding_mean'] = grouped['qty'].transform(lambda x: x.shift(1).expanding().mean())
    
    # Time index feature (weeks elapsed since the start of the dataset)
    min_week = weekly['week_start'].min()
    weekly['time_idx'] = ((weekly['week_start'] - min_week).dt.days / 7).astype(int)
    
    # 5. Clean up: Drop rows with NaN values (the first 4 weeks, due to lag_4 and roll_4)
    features_df = weekly.dropna().reset_index(drop=True)
    
    return features_df
