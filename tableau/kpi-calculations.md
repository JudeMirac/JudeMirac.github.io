# Transportation Performance — published Tableau workbook

Source: supplied SEPTA-inspired practice CSVs. Not official SEPTA service data.

Published September 26, 2026:
https://public.tableau.com/app/profile/jude.mirac/viz/TransportationPerformanceJudeMirac/TransportationPerformance

## Source and grain

`transportation-trips.csv` is the single trip-grain source. Maintenance and compliance are not physically joined, preventing duplicate trip counts. Tableau displays the imported column names in title case. Trip Date is a date; Scheduled Pickup and Actual Pickup are date/time. Trip Id and Contractor Id are dimensions. Exported numeric validation flags retain NULL for excluded pickups.

## Native Tableau calculations

The five calculated fields below are used in the published workbook. The CSV also contains independently computed row-level flags, used for validation and numerator/denominator tooltips.

### On-Time Performance

```tableau
AVG(IF [Trip Status] = 'Completed'
    AND NOT ISNULL([Scheduled Pickup]) AND NOT ISNULL([Actual Pickup])
THEN IF DATEDIFF('minute', [Scheduled Pickup], [Actual Pickup]) >= -5
    AND DATEDIFF('minute', [Scheduled Pickup], [Actual Pickup]) <= 15
    THEN 1 ELSE 0 END
END)
```

### Late Pickups

```tableau
SUM(IF [Trip Status] = 'Completed'
    AND NOT ISNULL([Scheduled Pickup]) AND NOT ISNULL([Actual Pickup])
THEN IF DATEDIFF('minute', [Scheduled Pickup], [Actual Pickup]) >= 16
    THEN 1 ELSE 0 END
END)
```

### Cancellation Rate

```tableau
SUM(IF [Trip Status] = 'Cancelled' THEN 1 ELSE 0 END) / COUNT([Trip Id])
```

### Average Pickup Delay

```tableau
AVG(IF [Trip Status] = 'Completed'
    AND NOT ISNULL([Scheduled Pickup]) AND NOT ISNULL([Actual Pickup])
THEN DATEDIFF('minute', [Scheduled Pickup], [Actual Pickup])
END)
```

Delay is signed, in minutes; early pickups remain negative. The dashboard displays 7.97 minutes for the full source, equivalent to 8.0 minutes at one decimal on the website.

### Contractor Review Flag

```tableau
IF ISNULL([On-Time Performance]) THEN 'No valid trips'
ELSEIF [On-Time Performance] < 0.85 THEN 'Review Needed'
ELSE 'Acceptable'
END
```

Compare the unrounded ratio with 0.85 at contractor grain. This flag does not incorporate compliance. Franklin Coach Group has no trips and is documented as unscored, not 0%.

## Published dashboard

**Transportation Performance**, desktop canvas 1,000 × 800:

- **Service KPIs:** average signed pickup delay, cancellation rate, late pickups, and on-time performance.
- **Contractor Performance:** ascending OTP bars, 85% reference line, review flag, and valid/on-time trip counts in tooltips.
- **Daily On-Time Trend:** continuous daily OTP line with an 85% reference line and trip counts in tooltips.
- Shared contractor and trip-date filters apply to all worksheets using this source. All statuses remain available so cancellation rate keeps the correct denominator.
- Source disclosure, KPI definitions, and no-trip contractor coverage note are visible on the dashboard.

The website separately presents fleet, compliance, and data-quality findings. These are not additional published Tableau dashboards.

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

## Embed configuration

`assets/tableau-config.js` contains the verified Tableau share URL. The case-study script embeds that view and supplies a direct Tableau Public fallback link. The website remains readable without JavaScript through its static validated snapshot.
