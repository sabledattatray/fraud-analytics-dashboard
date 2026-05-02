import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
import time

def train_fraud_model(data_path='../bfsi_fraud_data_10m.csv'):
    print(f"Loading data from {data_path}...")
    start_time = time.time()
    
    # Load a representative sample (1M rows) for training to ensure speed and performance
    # In a production environment, we'd use Spark or incremental learning
    df = pd.read_csv(data_path, nrows=1000000)
    
    print(f"Data loaded in {time.time() - start_time:.2f} seconds.")
    
    # 1. Feature Engineering
    print("Performing feature engineering...")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    
    # Encode categorical variables
    df = pd.get_dummies(df, columns=['merchant_category', 'location_region'], drop_first=True)
    
    # Select features
    features = [col for col in df.columns if col not in ['txn_id', 'timestamp', 'customer_id', 'merchant_id', 'is_fraud']]
    X = df[features]
    y = df['is_fraud']
    
    # 2. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 3. Train Model
    print(f"Training Random Forest Classifier on {len(X_train)} samples...")
    # Using fewer estimators for speed in this demo environment
    model = RandomForestClassifier(n_estimators=50, max_depth=10, n_jobs=-1, random_state=42)
    model.fit(X_train, y_train)
    
    # 4. Evaluate
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    print("\n--- Classification Report ---")
    print(classification_report(y_test, y_pred))
    
    print("\n--- Confusion Matrix ---")
    print(confusion_matrix(y_test, y_pred))
    
    auc = roc_auc_score(y_test, y_prob)
    print(f"\nROC-AUC Score: {auc:.4f}")
    
    # 5. Save Model
    print("Saving model and feature list...")
    joblib.dump(model, 'fraud_model.pkl')
    joblib.dump(features, 'model_features.joblib')
    
    print(f"\nTotal process completed in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    import os
    # Check if data exists in root or system folder
    if os.path.exists('bfsi_fraud_data_10m.csv'):
        train_fraud_model('bfsi_fraud_data_10m.csv')
    elif os.path.exists('../bfsi_fraud_data_10m.csv'):
        train_fraud_model('../bfsi_fraud_data_10m.csv')
    else:
        print("Error: Data file not found. Please run generate_data.py first.")
