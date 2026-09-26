# Jude Mirac | Data Analyst

Portfolio focused on **Health and Safety Data Analytics**. Built as a static, accessible site for GitHub Pages, with no framework or build dependency required for production. Vite is included only for local development.

## Project order

1. Transportation Performance & Risk — SEPTA-inspired practice project
2. Safety Risk Analysis
3. Fraud Risk Modeling
4. AI Investment Dashboard

The supplied résumé informs the biography and project results. Public project source links use the existing `JudeMirac` repositories. The AI source repository remains private; the site includes a résumé-based summary without exposing its contents.

## Live portfolio and dashboard

Portfolio: https://judemirac.github.io/

Transportation case study: https://judemirac.github.io/projects/transportation.html

Tableau Public: https://public.tableau.com/app/profile/jude.mirac/viz/TransportationPerformanceJudeMirac/TransportationPerformance

GitHub Pages deploys from **main / (root)** in **JudeMirac/JudeMirac.github.io**. `.nojekyll` serves the HTML/CSS/JS directly.

The published Tableau dashboard is embedded in the transportation case study through `assets/tableau-config.js`. It includes four KPI values, contractor OTP bars, a daily OTP trend, 85% reference lines, and shared contractor/date filters. The static snapshot remains available alongside the interactive dashboard.

`tableau/` contains trip, maintenance, and compliance exports, calculation documentation, reconciliation totals, and reconstructed Access KPI SQL. The published dashboard uses only the trip-grain source; fleet, audit, and data-quality findings appear in the website case study.

## Refresh data

```bash
python3 scripts/build_data.py /path/to/extracted/SEPTA_CSVs
```

This validates unique IDs, trip references, date parsing, boundary conditions, and totals, then rebuilds the JSON and Tableau CSV exports. Source timestamps are minute-precision. The compliance reference date is fixed in the script at September 24, 2026 for a reproducible snapshot.

The portfolio HTML contains the verified September 24 snapshot so it works without JavaScript. If source data changes, update the HTML numbers and supporting findings along with the generated exports.

## Files

- `index.html` — portfolio
- `projects/transportation.html` — transportation case study and published Tableau embed
- `assets/styles.css` — responsive design, focus styling, reduced motion, print styles
- `assets/Jude-Mirac-Resume.pdf` — supplied résumé, unchanged
- `data/transportation-summary.json` — computed results
- `tableau/` — publishing inputs and methods

Google Fonts is optional; the site uses system font fallbacks if unavailable. Chart values are also available as text. No analytics tracking, cookies, form backend, or credentials are included.

## Provenance and limitations

- Transportation data is a user-supplied SEPTA-inspired practice dataset, not official SEPTA performance.
- Safety findings use synthetic demonstration data and the supplied résumé.
- Fraud capture is a reported project evaluation, not a production result.
- Financial research descriptions do not claim investment returns.
- Fleet and audit sources have distinct dates and grain; do not flatten them onto trips.
- Original driver names and license numbers are omitted from published analysis exports.

## Validation

```bash
python3 scripts/check_site.py
node --check assets/transportation.js
node --check assets/tableau-config.js
```

