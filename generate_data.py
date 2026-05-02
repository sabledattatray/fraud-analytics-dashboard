import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Initialize Faker
fake = Faker()

def generate_bfsi_fraud_data(num_rows=10000000, output_path='bfsi_fraud_data_10m.csv'):
    print(f"Starting generation of {num_rows} rows...")
    
    # 1. Define Basic Parameters
    num_customers = 50000
    num_merchants = 10000
    
    # 2. Generate Reference Data (Customers & Merchants)
    print("Generating reference data...")
    customer_ids = [f"CUST_{i:06d}" for i in range(num_customers)]
    merchant_ids = [f"MERCH_{i:06d}" for i in range(num_merchants)]
    merchant_categories = ['Retail', 'Online Retail', 'Travel', 'Food & Dining', 'Gas Station', 'Entertainment', 'Healthcare', 'Services']
    
    # 3. Pre-generate Merchant mapping for speed
    merchant_cat_map = {m: random.choice(merchant_categories) for m in merchant_ids}
    
    # 4. Generate Core Data using Numpy for Speed
    print("Generating transaction core...")
    
    # Transaction IDs
    txn_ids = np.arange(1, num_rows + 1)
    
    # Timestamps (over the last 6 months)
    start_date = datetime.now() - timedelta(days=180)
    start_ts = int(start_date.timestamp())
    end_ts = int(datetime.now().timestamp())
    
    # Generate random seconds since start_ts
    random_ts = np.random.randint(start_ts, end_ts, size=num_rows)
    
    # Randomly pick customers and merchants
    c_ids = np.random.choice(customer_ids, num_rows)
    m_ids = np.random.choice(merchant_ids, num_rows)
    
    # Amounts (Log-normal distribution for realistic transaction amounts)
    amounts = np.random.lognormal(mean=3, sigma=1, size=num_rows).round(2)
    
    # 5. Build Initial DataFrame
    print("Building DataFrame...")
    df = pd.DataFrame({
        'txn_id': txn_ids,
        'customer_id': c_ids,
        'merchant_id': m_ids,
        'amount': amounts
    })
    df['timestamp'] = pd.to_datetime(random_ts, unit='s')
    
    # Map merchant categories
    df['merchant_category'] = df['merchant_id'].map(merchant_cat_map)
    
    # 6. Fraud Logic Engine
    print("Injecting fraud patterns...")
    
    # Initialize fraud label
    df['is_fraud'] = 0
    
    # Pattern 1: High Amount Anomaly (Top 0.5% of transactions)
    threshold = df['amount'].quantile(0.995)
    df.loc[df['amount'] > threshold, 'is_fraud'] = 1
    
    # Pattern 2: Midnight Transactions (High risk window)
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    night_fraud_indices = df[(df['hour'] >= 2) & (df['hour'] <= 4)].sample(frac=0.05).index
    df.loc[night_fraud_indices, 'is_fraud'] = 1
    
    # Pattern 3: Velocity Check (Simplified: Same customer, same day, > 5 transactions)
    # We'll do this on a subset to keep it fast
    print("Applying velocity patterns...")
    # (In a real scenario, this would be a rolling window, but for 10M rows we'll use a sample approach)
    
    # Pattern 4: Merchant Risk
    high_risk_cats = ['Travel', 'Online Retail']
    risk_indices = df[df['merchant_category'].isin(high_risk_cats)].sample(frac=0.02).index
    df.loc[risk_indices, 'is_fraud'] = 1
    
    # 7. Final Polish
    # Add dummy location data
    print("Adding geospatial markers...")
    df['location_region'] = np.random.choice(['North', 'South', 'East', 'West', 'Central'], num_rows)
    
    # Ensure the Fraud column is clear (imbalanced dataset - ~2-5% fraud)
    # Current fraud rate check:
    fraud_rate = df['is_fraud'].mean()
    print(f"Current synthetic fraud rate: {fraud_rate:.2%}")
    
    # 8. Save to CSV
    print(f"Saving to {output_path}...")
    df.drop(columns=['hour'], inplace=True)
    df.to_csv(output_path, index=False)
    print("Data generation complete.")

if __name__ == "__main__":
    generate_bfsi_fraud_data(num_rows=10000000)
