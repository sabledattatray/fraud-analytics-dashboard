# Power BI Integration Guide

To visualize the 10M rows of fraud data and the model results in Power BI, follow these steps:

## 1. Data Connection
- Open Power BI Desktop.
- Select **Get Data** > **Text/CSV**.
- Select `bfsi_fraud_data_10m.csv`.
- Use **Transform Data** to ensure data types are correct (especially `timestamp` as DateTime and `is_fraud` as a Whole Number).

## 2. Recommended Visualizations

### Executive Overview
- **Fraud Rate (%) Card**: `COUNT(is_fraud) where is_fraud = 1 / COUNT(txn_id)`
- **Total Amount at Risk**: `SUM(amount) where is_fraud = 1`
- **Fraud Over Time**: Line chart with `timestamp` on X-axis and `is_fraud` count on Y-axis.

### Geographic Risk Map
- Map visualization using `location_region` (or lat/long if generated).
- Color intensity based on `Fraud Rate`.

### Merchant Category Analysis
- Bar chart showing `is_fraud` count by `merchant_category`.
- Identifies high-risk sectors like Travel or Online Retail.

## 3. Python Script Integration (Advanced)
You can run the `train_model.py` logic directly inside Power BI:
- Go to **Transform Data** > **Run Python Script**.
- Paste the logic to generate feature importance or predictions.

## 4. DAX Measures for Fraud Detection
```dax
Fraud Prevalence = DIVIDE(CALCULATE(COUNT('Data'[is_fraud]), 'Data'[is_fraud] = 1), COUNT('Data'[txn_id]))

Total Potential Loss = CALCULATE(SUM('Data'[amount]), 'Data'[is_fraud] = 1)
```
