import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

# Load frozen model
obj = joblib.load("models/rf_sqli.joblib")
rf = obj["model"]
feature_names = list(obj["feature_names"])

# Load dataset
df = pd.read_csv("data/updated_file.csv")
X = df[feature_names]
y = df["Label"]

# Recreate internal 80/20 split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Baseline F1
baseline_preds = rf.predict(X_test)
baseline_f1 = f1_score(y_test, baseline_preds)

print("Baseline Test F1:", baseline_f1)

# Impurity-based importance
impurity_importance = rf.feature_importances_

results = []

# Permutation importance
for i, feature in enumerate(feature_names):
    X_test_permuted = X_test.copy()
    X_test_permuted[feature] = np.random.permutation(X_test_permuted[feature])
    
    perm_preds = rf.predict(X_test_permuted)
    perm_f1 = f1_score(y_test, perm_preds)
    
    f1_drop = baseline_f1 - perm_f1
    
    results.append({
        "Feature": feature,
        "Impurity Importance": impurity_importance[i],
        "Permutation F1": perm_f1,
        "F1 Drop": f1_drop
    })

# Create results DataFrame
results_df = pd.DataFrame(results)

# Rank by F1 drop
results_df = results_df.sort_values(by="F1 Drop", ascending=False)

print("\nPermutation Importance Results:")
print(results_df)
