import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from pathlib import Path

# Build paths relative to this script's location
BASE_DIR = Path(__file__).parent

# Load ASV abundance table
asv = pd.read_excel(BASE_DIR / "seqtab_nochim_export.xlsx")

# Load metadata (labels)
meta = pd.read_csv(BASE_DIR / "metadata.csv", sep=";")

# Merge on SampleID (adjust if column names differ)
df = asv.merge(meta[["SampleID", "DiseaseStatus"]], on="SampleID")

# Filter only CRC vs Healthy (remove Adenomatous Polyps)
df = df[df["DiseaseStatus"].isin(["CRC", "Healthy"])]

# Define target and features
y = df["DiseaseStatus"]
X = df.drop(columns=["DiseaseStatus", "SampleID"])

# Split data: 50 train, 10 test, rest validation
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, train_size=50, random_state=42, stratify=y
)

X_test, X_val, y_test, y_val = train_test_split(
    X_temp, y_temp, test_size=10, random_state=42, stratify=y_temp
)

# Train model
model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X_train, y_train)

# Evaluate on test set
test_preds = model.predict(X_test)
test_probs = model.predict_proba(X_test)[:, 1]

print("=== Test Set Performance ===")
print("Accuracy:", accuracy_score(y_test, test_preds))
print("ROC-AUC:", roc_auc_score(y_test.map({"Healthy":0, "CRC":1}), test_probs))

# Evaluate on validation set
val_preds = model.predict(X_val)
val_probs = model.predict_proba(X_val)[:, 1]

print("\n=== Validation Set Performance ===")
print("Accuracy:", accuracy_score(y_val, val_preds))
print("ROC-AUC:", roc_auc_score(y_val.map({"Healthy":0, "CRC":1}), val_probs))
