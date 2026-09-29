# import pandas as pd
# import numpy as np  # <-- Added this line
# import pickle
# import os
# from sklearn.ensemble import RandomForestClassifier
# from src.extractor import extract_features

# print("Loading data...")
# df = pd.read_csv("data/training_data.csv")

# print("Extracting features (this takes a few seconds)...")
# # Apply extractor to each prompt and stack into a 2D array
# X = np.vstack(df['prompt'].apply(extract_features).values)
# y = df['tier'].values

# print("Training Random Forest Classifier...")
# clf = RandomForestClassifier(n_estimators=50, random_state=42)
# clf.fit(X, y)

# os.makedirs("models", exist_ok=True)
# with open("models/router.pkl", "wb") as f:
#     pickle.dump(clf, f)

# print(f"✅ Model trained with {clf.score(X, y):.2%} accuracy and saved to models/router.pkl!")

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import mlflow
import mlflow.sklearn
from src.extractor import extract_features

print("Loading data...")
df = pd.read_csv("data/training_data.csv")

print("Extracting features (this takes a few seconds)...")
# Apply extractor to each prompt and stack into a 2D array
X = np.vstack(df['prompt'].apply(extract_features).values)
y = df['tier'].values

# Split data so we can calculate real metrics for MLflow
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize MLflow tracking
mlflow.set_experiment("llm-prompt-router")

with mlflow.start_run():
    # 1. Log Hyperparameters
    n_trees = 50
    mlflow.log_param("n_estimators", n_trees)
    mlflow.log_param("random_state", 42)

    print("Training Random Forest Classifier...")
    clf = RandomForestClassifier(n_estimators=n_trees, random_state=42)
    clf.fit(X_train, y_train)

    # 2. Evaluate Model
    y_pred = clf.predict(X_test)
    macro_f1 = f1_score(y_test, y_pred, average="macro")
    accuracy = clf.score(X_test, y_test)

    # 3. Log Metrics & Model to MLflow
    mlflow.log_metric("macro_f1", macro_f1)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(
        clf, 
        "random_forest_router", 
        skops_trusted_types=["sklearn.tree._tree.Tree"]
    )

    # 4. Save the standard .pkl file for the live FastAPI server
    os.makedirs("models", exist_ok=True)
    with open("models/router.pkl", "wb") as f:
        pickle.dump(clf, f)

    print(f"✅ Model trained! Accuracy: {accuracy:.2%}, F1: {macro_f1:.2f}")
    print("✅ Successfully logged to MLflow and saved to models/router.pkl")