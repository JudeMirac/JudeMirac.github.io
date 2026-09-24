# Jude Mirac | Data Analyst

Portfolio focused on **Health and Safety Data Analytics**. Built as a static, accessible site for GitHub Pages, with no framework or build dependency required for production. Vite is included only for local development.

## Project order

1. Transportation Performance & Risk — SEPTA-inspired practice project
2. Safety Risk Analysis
3. Fraud Risk Modeling
4. AI Investment Dashboard

The supplied résumé informs the biography and project results. Public project source links use the existing `JudeMirac` repositories. The AI source repository remains private; the site includes a résumé-based summary without exposing its contents.

## Publish on GitHub Pages

Use the public user-site repository **JudeMirac/JudeMirac.github.io**. Keep these files at its root. In Settings → Pages, select **Deploy from a branch**, branch **main**, folder **/ (root)**. `.nojekyll` serves the HTML/CSS/JS directly. The expected user-site address is `https://judemirac.github.io/`; this is a configuration target, not proof of a completed deployment.

## Tableau status

`assets/tableau-config.js` intentionally has an empty URL until a real dashboard is published and verified. A static project snapshot is already visible. No sample URL or unrelated dashboard is embedded.

`tableau/` contains separate trip, maintenance, and compliance exports, native Tableau calculation definitions, a dashboard layout, reconciliation totals, and the reconstructed Access KPI SQL. These preparation files are not a published Tableau workbook.

## Refresh data

```bash
python3 scripts/build_data.py /path/to/extracted/SEPTA_CSVs
```

This validates unique IDs, trip references, date parsing, boundary conditions, and totals, then rebuilds the JSON and Tableau CSV exports. Source timestamps are minute-precision. The compliance reference date is fixed in the script at September 24, 2026 for a reproducible snapshot.

The portfolio HTML contains the verified September 24 snapshot so it works without JavaScript. If source data changes, update the HTML numbers and supporting findings along with the generated exports.

## Files

- `index.html` — portfolio
- `projects/transportation.html` — transportation case study and eventual Tableau embed
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

## Tableau publishing

The Tableau Public workbook and embed are pending. The portfolio currently presents the validated transportation snapshot.
