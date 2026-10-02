# Fraud dashboard sources and calculations

Source repository: https://github.com/JudeMirac/Fraud-Model-Project
Source tree: 370f3857b561f9a74d8ca5b21e6cae4c8b7a3964

## Dataset summaries
Data/fraud_risk_dataset.csv contains 5,000 transactions, 363 labeled fraud (7.26%).
Merchant and transaction-location summaries count rows and sum the binary fraud flag.
Fraud Rate Percent = 100 × Fraud Cases / Transactions within each category.
International=1 maps to International; 0 maps to Domestic.

## Saved decision evaluation
Notebooks/Prescriptive.ipynb contains final saved outputs for the percentile policy:
ALLOW: 4,000 transactions, 3.55% fraud, 142 fraud cases.
REVIEW: 750 transactions, 18.133333% fraud, 136 fraud cases.
BLOCK: 250 transactions, 34% fraud, 85 fraud cases.
Fraud counts are reconstructed from the saved counts and fraud rates, and reconcile to 363.
Review + block capture = (136+85)/363 = 60.8815427%, reported as 61%.
These policy outputs score the full 5,000-row dataset, including training records. They are not a held-out performance estimate.
The notebook contains intermediate attempts and out-of-order execution; the dashboard reproduces its final saved summary outputs, not a new model run.
No row-level decision assignments or risk scores were invented or joined to merchant records.

## Dashboard grain and filters
The aggregate file has three independent views, each covering the same 5,000 transactions:
Merchant category; Transaction location; Model decision.
Every Tableau worksheet is filtered to exactly one View.
Do not sum transactions or fraud cases across views: that would triple-count the underlying population.
Each category has one summary row; displayed rates are already calculated percentages.
The dashboard contains 4 charts: Fraud Rate by Merchant, Domestic vs International,
Transactions by Decision, and Fraud Rate by Decision.

## Model evaluation context
Notebooks/Modeling_Fraud.ipynb reports ROC-AUC 0.7195074495940483 on a 1,500-row test set.
This is distinct from the full-dataset policy capture result and is not combined with it in this dashboard.
