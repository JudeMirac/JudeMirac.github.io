Safety Risk Analysis Tableau source

Source: JudeMirac/Saftey-Risk-Analysis, Safety-Analysis branch, extracted September 27, 2026. Repository README identifies data as synthetic. Fiscal year 2025; week numbers preserved without guessing calendar dates.

Source Group is mandatory as a worksheet filter. Never total across source groups. Site weekly incidents and hours are differences of cumulative site figures; first week uses zero baseline. Process path counts/hours are already weekly and are retained unchanged. Rates use SUM(Incidents)*200000/SUM(Exposure Hours), with NULL if hours are zero. Four process-path rows have incidents and zero hours; keep counts visible and flag unavailable rates. Root cause/severity each cover 199 incidents. Contributing factors cover 18 incidents. These source populations are not joined or presented as matching totals. Original derived process_path_feat.csv is excluded due to negative weekly deltas. Severity codes are retained as supplied without inventing meanings.

Published dashboard: https://public.tableau.com/app/profile/jude.mirac/viz/SafetyRiskAnalysisJudeMirac/SafetyOverview

Overview scope: weekly site incidents and weighted rate, root causes, severity codes, and contributing factors. Process-path records are included in the downloadable source for further analysis but are not charted on the overview. No composite risk score is calculated. The existing portfolio concentration findings refer to the original project snapshots, not the weekly site total.

Site annual totals: 203 incidents / 1,651,921.908 hours × 200,000 = 24.577432990857822. Displayed as 24.58. The title is a fixed FY2025 summary; selecting a mark does not recalculate it.
