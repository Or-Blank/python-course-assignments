# CRC Gut Microbiome — Polyp Patient Risk Prediction #

This tool predict whether Adenomatous Polyp patients resemble Colorectal cancer (CRC) (high risk) or Healthy (low risk) based on the **gut microbiome** 16S rRNA data.

## Background:
* An adenomatous polyp or Colon polyps are growths, like tiny bumps, that form on the inside lining of your colon or rectum. They’re usually harmless, but some types can turn into colon cancer after many years. Therefore, Patients with colon polyps may or may not progress to CRC.

* The microbiome plays a major, dynamic role in both overall human physiology and in the biology of tumors such as CRC. It’s well established that as tissue transitions from healthy to precancerous to cancerous, the tumor microenvironment changes also.

* There are, as I used for this tool, datasets comparing the gut microbiome of healthy individuals and patients with colorectal cancer, giving us a clearer picture of how microbial signatures reflect disease progression.

 * Because the outcome for polyp patients is unknown, we can use microbiome datasets from confirmed CRC and Healthy individuals, we can train a model and then apply it to polyp patients to estimate what is the patient's likelihood of progressing to colorectal cancer.


## Method:
  - Use the source dataset - **CRC Gut Microbiome ML Data**: https://www.kaggle.com/datasets/aramelheni/crc-gut-microbiome-ml-data
  - **Files needed**:
  * *metadata.csv*
  * *taxa_species.xlsx*
  * *seqtab.xlsx*
  * *Note:* The files are a bit diffrent than in the source, use the ones I uploaded in the repo.
    
  - Train on the  CRC + Healthy patients
  - Predict on Adenomatous Polyp patients (n=19, genuinely unknown outcome).
  * Each polyp patient is classified as resembling CRC (high risk) or Healthy (low risk).


## How to run:
Before running:
1. Install dependencies using:
```bash
pip install -r requirements.txt
```
2. Make sure all 3 files (2 xlsx and 1 csv) are in the same folde as the code

Then run:
```bash
python crc_prediction.py
```



## Output:
The pipeline produces a full risk‑prediction report for polyp patients.

1. **In the terminal**:
* Prediction table for all 19 polyp patients.

2. **In a PNG file saved to the folder**:
* Top-left pie chart: Training set composition (21 CRC + 19 Healthy).
* Bottom-left pie chart: Predicted risk split across all 19 polyp patients.
* Middle bar chart: Per-patient prediction with confidence % for each polyp patient.
* Right bar chart: Abundance of the top 20 bacteria in crc and healty samples.

## AI: 
I used Claude and the VS copilot for this week.
Prompts used:
  1. "I have seqtab_nochim_export.xlsx, metadata.csv and taxa_species_export.xlsx. Train on CRC+Healthy, predict on Polyp patients to create plots of predction of the Polyp to develope crc or stay healty.
  2. "For each polyp patient show: predicted label, confidence, risk level.
  For top-20 bacteria show the % of CRC patients and % of Healthy
  patients where that bacterium is present."

## Parpers:
https://my.clevelandclinic.org/health/diseases/15370-colon-polyps
 
