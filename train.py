import pandas as pd
import numpy as np  # <-- Added this line
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from src.extractor import extract_features

print("Loading data...")
df = pd.read_csv("data/training_data.csv")

print("Extracting features (this takes a few seconds)...")
# Apply extractor to each prompt and stack into a 2D array
X = np.vstack(df['prompt'].apply(extract_features).values)
y = df['tier'].values

print("Training Random Forest Classifier...")
clf = RandomForestClassifier(n_estimators=50, random_state=42)
clf.fit(X, y)

os.makedirs("models", exist_ok=True)
with open("models/router.pkl", "wb") as f:
    pickle.dump(clf, f)

print(f"✅ Model trained with {clf.score(X, y):.2%} accuracy and saved to models/router.pkl!")