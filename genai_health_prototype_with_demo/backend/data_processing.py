"""Data processing and simple model prototype using pandas and scikit-learn.
This file contains placeholder functions you can adapt to your dataset.
"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import joblib
from typing import Dict

MODEL_FILE = 'model.joblib'

def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    # Basic preprocessing: drop duplicates, simple imputation for numeric cols
    df = df.copy()
    df = df.drop_duplicates()
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    imputer = SimpleImputer(strategy='median')
    if num_cols:
        df[num_cols] = imputer.fit_transform(df[num_cols])
    # Add simple rolling features or time-based features here
    return df

def train_dummy_model(df: pd.DataFrame, label_col: str = 'label') -> Dict:
    # Basic example: train a RandomForest on provided dataframe.
    # The dataset must have a 'label' column (0/1) for supervised training.
    df = preprocess(df)
    if label_col not in df.columns:
        raise ValueError(f"Label column '{label_col}' not found in dataframe.")
    X = df.drop(columns=[label_col])
    y = df[label_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train.select_dtypes(include=['number']))
    X_test_s = scaler.transform(X_test.select_dtypes(include=['number']))
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train_s, y_train)
    joblib.dump({'model': model, 'scaler': scaler}, MODEL_FILE)
    score = model.score(X_test_s, y_test)
    return {'accuracy': score}

def load_model():
    try:
        data = joblib.load(MODEL_FILE)
        return data['model'], data['scaler']
    except Exception:
        return None, None

def generate_insights(patient_row: pd.Series) -> Dict:
    # Placeholder logic for generating simple rule-based insights.
    insights = []
    # Example: check for high heart rate, high glucose, low SpO2
    if 'heart_rate' in patient_row and patient_row['heart_rate'] > 100:
        insights.append('Elevated heart rate detected. Consider contacting provider.')
    if 'glucose_mg_dl' in patient_row and patient_row['glucose_mg_dl'] > 180:
        insights.append('High blood glucose reading — follow diabetes action plan.')
    if 'systolic_bp' in patient_row and 'diastolic_bp' in patient_row and (patient_row['systolic_bp'] > 140 or patient_row['diastolic_bp'] > 90):
        insights.append('Hypertensive-range blood pressure detected. Re-check and consult physician.')
    return {'insights': insights}
