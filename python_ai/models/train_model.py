# python/models/train.py
"""
Example training script to build a RandomForestClassifier and scaler.
Requires: training_events.csv with numeric features and 'label' column.
Produces model.pkl and scaler.pkl in python/models/
"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from joblib import dump
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODEL_DIR, exist_ok=True)

CSV = os.path.join(os.path.dirname(__file__), "..", "training_events.csv")

if not os.path.exists(CSV):
    print("No training_events.csv found at", CSV)
    print("Create a CSV with numeric columns and a 'label' column to train.")
else:
    df = pd.read_csv(CSV)
    if "label" not in df.columns:
        raise SystemExit("training_events.csv must contain a 'label' column.")
    X = df.drop(columns=["label"])
    y = df["label"]
    scaler = StandardScaler().fit(X)
    Xs = scaler.transform(X)
    X_train, X_test, y_train, y_test = train_test_split(Xs, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)
    print("Train score:", clf.score(X_train, y_train))
    print("Test score:", clf.score(X_test, y_test))
    dump(clf, os.path.join(MODEL_DIR, "model.pkl"))
    dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))
    print("Saved model and scaler to", MODEL_DIR)
