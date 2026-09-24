# Transportation Performance & Risk — Tableau calculations

Source: supplied SEPTA Access practice CSVs. Not official SEPTA service data.

Use `transportation-trips.csv` as a **single trip-grain data source**. Do not physically join maintenance or compliance to it. Those sources have multiple rows per vehicle/contractor and would multiply trip records.

Set `trip_date` to Date and `scheduled_pickup` / `actual_pickup` to Date & Time. The source timestamps have minute precision. Set `contractor_id` and `trip_id` to Dimensions; trip IDs are unique. `passenger_count` is a measure. Empty numeric flags must remain NULL.

## Calculated fields

Create each field under the name shown. Row flags in the export are independently computed validation values; these native Tableau formulas are the authoritative dashboard calculations.

### Valid Pickup
```tableau
[trip_status] = 'Completed'
AND NOT ISNULL([scheduled_pickup])
AND NOT ISNULL([actual_pickup])
```

### Pickup Delay Minutes
```tableau
IF [Valid Pickup] THEN
    DATEDIFF('minute', [scheduled_pickup], [actual_pickup])
END
```

### On Time Flag
```tableau
IF [Valid Pickup] THEN
    IF [Pickup Delay Minutes] >= -5 AND [Pickup Delay Minutes] <= 15
    THEN 1 ELSE 0 END
END
```

### Late Flag
```tableau
IF [Valid Pickup] THEN
    IF [Pickup Delay Minutes] >= 16 THEN 1 ELSE 0 END
END
```

### On Time Performance
```tableau
AVG([On Time Flag])
```
Format as percentage with one decimal. Do not multiply by 100 and also apply percentage formatting. Do not average contractor percentages.

### Late Pickups
```tableau
SUM([Late Flag])
```

### Cancellation Rate
```tableau
SUM(IF [trip_status] = 'Cancelled' THEN 1 ELSE 0 END) / COUNT([trip_id])
```
Format as percentage with one decimal.

### Average Pickup Delay
```tableau
AVG([Pickup Delay Minutes])
```
Format as a number with one decimal and `min` suffix. This is signed delay: early arrivals remain negative. It is not the average of only positive delays.

### Valid Completed Trips
```tableau
SUM(IF [Valid Pickup] THEN 1 ELSE 0 END)
```

### Completed Trips
```tableau
SUM(IF [trip_status] = 'Completed' THEN 1 ELSE 0 END)
```

### Completed Passenger Volume
```tableau
SUM(IF [trip_status] = 'Completed' THEN [passenger_count] END)
```

### Contractor Review Flag
```tableau
IF ISNULL(AVG([On Time Flag])) THEN 'No valid trips'
ELSEIF AVG([On Time Flag]) < 0.85 THEN 'Review Needed'
ELSE 'Acceptable'
END
```
Evaluate at contractor grain. Compare the unrounded ratio to 0.85. Compliance is intentionally excluded from this flag. Franklin Coach Group has no trip records, so it does not appear in a trip-only view; show the eight-contractor coverage note separately. Do not give it 0% OTP.

### Completed Missing Pickup
```tableau
SUM(IF [trip_status] = 'Completed' AND
    (ISNULL([scheduled_pickup]) OR ISNULL([actual_pickup]))
    THEN 1 ELSE 0 END)
```

### Pickup Classification
```tableau
IF NOT [Valid Pickup] THEN 'Excluded'
ELSEIF [Pickup Delay Minutes] < -5 THEN 'Too early'
ELSEIF [Pickup Delay Minutes] <= 15 THEN 'On time'
ELSE 'Late'
END
```

## Dashboard views

1. **Service Performance:** four headline KPIs (OTP, late pickups, cancellation rate, average signed delay), daily OTP line with an 85% reference line, contractor OTP bars sorted ascending, and contractor scorecard including numerator / denominator. Filters: contractor and trip date, applied to every trip-based sheet. Keep all statuses in the source; do not globally filter to Completed, because that breaks cancellation rate.
2. **Fleet & Compliance:** separate maintenance and compliance sources. Show 188 maintenance events, 42 mechanical failures, 2,845.8 total downtime hours, 44 audits, and 12 overdue open actions as of September 24, 2026. Fleet status snapshot: 3 of 56 vehicles out of service. Apply dates to their respective service/audit fields, not `trip_date`. Do not imply missing return dates are closed work.
3. **Data Quality:** missing actual pickup, actual dropoff, driver, and vehicle fields; completed trips with missing pickup timestamps; status distribution. Show that missing-field counts overlap and include expected blanks for non-completed trips.

Use 1,200 × 900 for the desktop dashboard and add a phone layout. Navy `#101e32`, teal `#007d78`, amber `#e5b559`, light blue `#91acd2`. Use a source/provenance subtitle and show denominators in tooltips. Add navigation among the three views.

## Reconciliation — unfiltered trip source

| Check | Expected |
|---|---:|
| Total trips | 650 |
| Completed | 562 |
| Valid completed pickups | 556 |
| On time | 319 |
| OTP | 57.4% |
| Late | 155 |
| Too early | 82 |
| Cancelled | 51 |
| No Show | 37 |
| Cancellation rate | 7.8% |
| Average signed pickup delay | 8.0 min |
| Completed passenger volume | 13,587 |
| Completed trips missing pickup times | 6 |
| All missing actual pickup | 94 |
| All missing actual dropoff | 93 |
| Missing vehicle | 12 |
| Missing driver | 9 |

Boundary checks: −6 minutes = too early; −5 and +15 = on time; +16 = late. Missing timestamps and non-completed trips are NULL for pickup KPIs. An empty filtered period has no valid OTP, not 0%.

## Supporting sources

- Tableau date calculations: https://help.tableau.com/current/pro/desktop/en-us/functions_functions_date.htm
- Tableau dashboard authoring: https://help.tableau.com/current/pro/desktop/en-us/dashboards_create.htm
- Tableau Public FAQ: https://help.tableau.com/current/pro/desktop/en-us/public_faq.htm

## Embed configuration

After publishing and checking the Tableau Public view, copy its verified `https://public.tableau.com/views/.../...` URL into `assets/tableau-config.js` as `window.PORTFOLIO_TABLEAU.url`. The case study adds an iframe and an external fallback link automatically. Until a real URL is supplied, the page shows the verified project snapshot and omits the embed section.
