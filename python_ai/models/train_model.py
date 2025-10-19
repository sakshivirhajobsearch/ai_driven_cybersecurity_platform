import os
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

models_dir = os.path.dirname(__file__)
os.makedirs(models_dir, exist_ok=True)

print("==== Training ML model ====")

# Simulated dataset
X, y = make_classification(n_samples=1000, n_features=20, n_informative=15, n_classes=2, random_state=42)

# Preprocessing
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("✅ Data scaled using StandardScaler.")

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_scaled, y)
print("✅ RandomForestClassifier trained.")

# Save scaler
scaler_path = os.path.join(models_dir, "scaler.pkl")
with open(scaler_path, "wb") as f:
    pickle.dump(scaler, f)
print(f"✅ Scaler saved at: {scaler_path}")

# Save model
model_path = os.path.join(models_dir, "model.pkl")
with open(model_path, "wb") as f:
    pickle.dump(model, f)
print(f"✅ Model saved at: {model_path}")

print("==== ML training complete ====")
