CRC Gut Microbiome Prediction Script

Before running:
    Install dependencies using:
        pip install -r requirements.txt

Then run:
        python crc_prediction.py


"""
CRC Gut Microbiome - Polyp Cancer Risk Prediction
Dataset: https://www.kaggle.com/datasets/aramelheni/crc-gut-microbiome-ml-data
Files needed: seqtab_nochim_export.xlsx, metadata.csv, taxa_species_export.xlsx
 
Method:
  Train on CRC + Healthy patients (n=40, known labels).
  Predict on Adenomatous Polyp patients (n=19, genuinely unknown outcome).
  Each polyp patient is classified as resembling CRC (high risk) or Healthy (low risk).
 
Prompts used:
  1. "I have seqtab_nochim_export.xlsx (59 samples x 6693 ASVs), metadata.csv and
      taxa_species_export.xlsx. Train on CRC+Healthy, predict on Polyp patients.
      Map ASV sequences to bacteria names via the taxa file."
  2. "With n=40 training samples and 6693 features, use VarianceThreshold + 
      StandardScaler + PCA(30) + Random Forest to avoid overfitting."
  3. "For each polyp patient show: predicted label, confidence, risk level.
      For top-20 bacteria show: importance + % of CRC patients and % of Healthy
      patients where that bacterium is present."
"""
 