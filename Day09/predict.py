import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.feature_selection import VarianceThreshold
from sklearn.pipeline import Pipeline
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.metrics import accuracy_score
 
#Taxa mapping file = get the common bacteria display names
taxa = pd.read_excel("taxa_species.xlsx").rename(columns={"Unnamed: 0": "sequence"})
 
def best_name(row):
    if pd.notna(row["Genus"]):
        return f"{row['Genus']} sp."
    for col in ["Family", "Order", "Class", "Phylum", "Genus"]:
        if pd.notna(row[col]):
            return str(row[col])
    return "Unknown"
 
seq_to_name = dict(zip(taxa["sequence"], taxa.apply(best_name, axis=1)))
def make_unique_columns(names):
    seen, result = {}, []
    for name in names:
        count = seen.get(name, 0) + 1
        seen[name] = count
        result.append(name if count == 1 else f"{name}_{count}")
    return result
 
#Load & split by disease group
asv  = pd.read_excel("seqtab.xlsx").rename(columns={"Unnamed: 0": "host_disease"})
meta = pd.read_csv("metadata.csv", sep=";")
df   = asv.merge(meta[["host_disease", "DiseaseStatus"]], on="host_disease")

# Build unique column names once, shared by both train and polyp sets
asv_cols     = [c for c in df.columns if c not in ["host_disease", "DiseaseStatus"]]
raw_names    = [seq_to_name.get(c, "Unknown") for c in asv_cols]
unique_names = make_unique_columns(raw_names)
col_map      = dict(zip(asv_cols, unique_names))
 
def to_X(d):
    X = d.drop(columns=["host_disease", "DiseaseStatus"]).select_dtypes(include=[float, int]).fillna(0)
    mapped = [seq_to_name.get(c, "Unknown") for c in X.columns]
    unique = make_unique_columns(mapped)
    X.columns = unique
    return X

 
df_train = df[df["DiseaseStatus"].isin(["Colorectal cancer", "Healthy"])].copy()
df_poly  = df[df["DiseaseStatus"] == "Adenomatous Polyps"].copy()
 
X_tr = to_X(df_train)
X_po = to_X(df_poly)
 
le   = LabelEncoder()  # Colorectal cancer=0, Healthy=1
y_tr = le.fit_transform(df_train["DiseaseStatus"])
crc_mask = y_tr == 0
hlt_mask = y_tr == 1
 
#AI addition - Pipeline: zero-variance filter → scale → PCA(30) → Random Forest
pipe = Pipeline([
    ("vt",  VarianceThreshold(0.0)),
    ("sc",  StandardScaler()),
    ("pca", PCA(n_components=30, random_state=42)),
    ("clf", RandomForestClassifier(500, class_weight="balanced", random_state=42, n_jobs=-1)),
])
pipe.fit(X_tr, y_tr)
 
#Predict the polyp patients
y_pred  = pipe.predict(X_po.values)
y_proba = pipe.predict_proba(X_po.values)
poly_names = df_poly["host_disease"].values
 
#Ranking the top 20 bacteria with % in CRC and Healthy patients 
vt         = VarianceThreshold(0.0).fit(X_tr)
X_vt       = vt.transform(X_tr)
feat_names = np.array(X_tr.columns)[vt.get_support()]

crc_pcts = []
hlt_pcts = []
bact_labels = []

for i, bact in enumerate(feat_names):
    col = X_vt[:, i]
    crc_pct = (col[crc_mask] > 0).mean()
    hlt_pct = (col[hlt_mask] > 0).mean()
    crc_pcts.append(crc_pct)
    hlt_pcts.append(hlt_pct)
    bact_labels.append(bact)
 
idx = np.argsort(crc_pcts)[-20:]
bact_labels = [bact_labels[i] for i in idx]
crc_pcts    = [crc_pcts[i] for i in idx]
hlt_pcts    = [hlt_pcts[i] for i in idx]
 
#LOO-CV accuracy on training set (CRC vs Healthy)
loo_acc = cross_val_score(pipe, X_tr.values, y_tr, cv=LeaveOneOut(), scoring="accuracy", n_jobs=-1).mean()
 
#Print the results
print(f"\n{'='*65}")
print(f"  Polyp Patient Risk Prediction")
print(f"  (trained on {sum(crc_mask)} CRC + {sum(hlt_mask)} Healthy patients)")
print(f"  LOO-CV Accuracy: {loo_acc:.1%}")
print(f"{'='*65}")
print(f"  {'Patient':<12} {'Resembles':<22} {'Confidence':>10}  {'Risk'}")
print(f"  {'-'*60}")
for name, pred, prob in zip(poly_names, y_pred, y_proba):
    label = le.classes_[pred]
    risk  = "[!] HIGH RISK" if pred == 0 else "[OK] LOW RISK"
    print(f"  {name:<12} {label:<22} {max(prob):>9.0%}  {risk}")
 
n_high = sum(y_pred == 0)
n_low  = sum(y_pred == 1)
print(f"\n  Summary: {n_high} polyp patients resemble CRC (high risk)")
print(f"           {n_low} polyp patients resemble Healthy (low risk)")
 
#Plotting the results 
CRC_COL  = "#e74c3c"
H_COL    = "#2ecc71"
RISK_COL = "#e67e22"
 
fig = plt.figure(figsize=(20, 11))
fig.patch.set_facecolor("#f8f9fa")
fig.suptitle("CRC Gut Microbiome — Polyp Patient Risk Prediction",
             fontsize=16, fontweight="bold", y=0.99)
 
#Panel A: Training composition pie
ax1 = fig.add_axes([0.03, 0.54, 0.20, 0.38])
counts = [sum(crc_mask), sum(hlt_mask)]
wedges, _, autotexts = ax1.pie(
    counts,
    labels=[f"CRC\n(n={counts[0]})", f"Healthy\n(n={counts[1]})"],
    colors=[CRC_COL, H_COL], autopct="%1.0f%%", startangle=90,
    textprops={"fontsize": 11}, pctdistance=0.62,
    wedgeprops={"edgecolor": "white", "linewidth": 2})
for at in autotexts:
    at.set(fontsize=12, fontweight="bold", color="white")
ax1.set_title("Training Set\n(known labels)", fontsize=11, pad=10)
 
#Panel B: Polyp prediction pie 
ax2 = fig.add_axes([0.03, 0.08, 0.20, 0.38])
ax2.pie(
    [n_high, n_low],
    labels=[f"! High Risk\n(n={n_high})", f"OK Low Risk\n(n={n_low})"],
    colors=[CRC_COL, H_COL], autopct="%1.0f%%", startangle=90,
    textprops={"fontsize": 11}, pctdistance=0.62,
    wedgeprops={"edgecolor": "white", "linewidth": 2})
ax2.set_title("Polyp Patients\n(predicted risk)", fontsize=11, pad=10)
 
#Panel C: Per-polyp prediction bars
ax3 = fig.add_axes([0.28, 0.10, 0.24, 0.84])
conf_vals  = [max(p) * 100 for p in y_proba]
bar_colors = [CRC_COL if p == 0 else H_COL for p in y_pred]
y_pos      = np.arange(len(poly_names))
 
ax3.barh(y_pos, conf_vals, color=bar_colors, edgecolor="white", linewidth=1.5, height=0.65)
 
for i, (pred, conf) in enumerate(zip(y_pred, conf_vals)):
    label = "! CRC-like" if pred == 0 else "OK Healthy-like"
    ax3.text(2, i, f"  {label}", va="center", fontsize=8.5,
             color="white", fontweight="bold")
    ax3.text(conf + 1.5, i, f"{conf:.0f}%", va="center", fontsize=8.5, color="#333")
 
ax3.set_yticks(y_pos)
ax3.set_yticklabels(poly_names, fontsize=10)
ax3.set_xlim(0, 115)
ax3.axvline(50, color="gray", linestyle="--", alpha=0.4, linewidth=1)
ax3.set_xlabel("Prediction Confidence (%)", fontsize=10)
ax3.set_title("Per-Patient Prediction\n(confidence %)", fontsize=11)
ax3.set_facecolor("#f0f0f0")
ax3.spines[["top", "right"]].set_visible(False)
ax3.legend(handles=[mpatches.Patch(color=CRC_COL, label="! High Risk (CRC-like)"),
                    mpatches.Patch(color=H_COL,   label="OK Low Risk (Healthy-like)")],
           loc="lower right", fontsize=9)
 
#Panel D: Top-20 bacteria with CRC% and Healthy% 
ax4 = fig.add_axes([0.57, 0.10, 0.41, 0.84])
y_pos2 = np.arange(len(bact_labels))
bar_w  = 0.28
 
bars_crc = ax4.barh(y_pos2,          crc_pcts,  height=bar_w, color=CRC_COL,
                    label="% Present in CRC",   edgecolor="white", linewidth=0.8, alpha=0.85)
bars_hlt = ax4.barh(y_pos2 - bar_w,  hlt_pcts,  height=bar_w, color=H_COL,
                    label="% Present in Healthy", edgecolor="white", linewidth=0.8, alpha=0.85)
 
#Add percentage labels on CRC and Healthy bars
for i, (cp, hp) in enumerate(zip(crc_pcts, hlt_pcts)):
    ax4.text(cp + 0.01, i,          f"{cp:.0%}", va="center", fontsize=7.5, color="#333")
    ax4.text(hp + 0.01, i - bar_w,  f"{hp:.0%}", va="center", fontsize=7.5, color="#333")
 
ax4.set_yticks(y_pos2)
ax4.set_yticklabels(bact_labels, fontsize=8.5)
ax4.set_xlabel("Prevalence (%)", fontsize=10)
ax4.set_title("Top 20 Most Predictive Bacteria\n(importance + % of patients where bacterium is present)",
              fontsize=11)
ax4.set_facecolor("#f0f0f0")
ax4.spines[["top", "right"]].set_visible(False)
ax4.legend(loc="lower right", fontsize=9)
ax4.set_xlim(0, 1.0)
 
#Footer
fig.text(0.28, 0.025,
         f"Training: {sum(crc_mask)} CRC + {sum(hlt_mask)} Healthy  |  "
         f"LOO-CV Accuracy: {loo_acc:.1%}  |  "
         f"Polyp predictions: {n_high} high risk, {n_low} low risk",
         ha="left", fontsize=10, color="#555",
         bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#ccc"))
 
plt.savefig("crc_results.png", dpi=150, bbox_inches="tight")
print("\nSaved: crc_results.png")