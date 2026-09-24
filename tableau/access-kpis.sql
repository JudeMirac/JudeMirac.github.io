/* Save as qValidPickupMetrics in Microsoft Access.
   This reconstructs the agreed KPI logic from the supplied CSV schema.
   These queries are new portfolio documentation, not a verbatim export of
   every saved query in the supplied Access database. */
SELECT
    t.trip_id,
    t.trip_date,
    t.contractor_id,
    t.trip_status,
    IIf(t.trip_status='Completed'
        AND t.scheduled_pickup Is Not Null
        AND t.actual_pickup Is Not Null,
        DateDiff('n', t.scheduled_pickup, t.actual_pickup),
        Null) AS pickup_delay_minutes,
    IIf(t.trip_status='Completed'
        AND t.scheduled_pickup Is Not Null
        AND t.actual_pickup Is Not Null,
        IIf(DateDiff('n', t.scheduled_pickup, t.actual_pickup)
            Between -5 And 15, 1, 0),
        Null) AS on_time_flag,
    IIf(t.trip_status='Completed'
        AND t.scheduled_pickup Is Not Null
        AND t.actual_pickup Is Not Null,
        IIf(DateDiff('n', t.scheduled_pickup, t.actual_pickup)>=16,1,0),
        Null) AS late_flag
FROM trips AS t;

/* Run separately, after saving the query above. A LEFT JOIN retains
   contractors with no trips. COUNT(trip_id) excludes the empty joined row. */
SELECT
    c.contractor_id,
    c.contractor_name,
    Count(q.trip_id) AS total_trips,
    Count(q.on_time_flag) AS valid_completed_trips,
    Sum(q.on_time_flag) AS on_time_trips,
    Round(Avg(q.on_time_flag)*100,1) AS otp_percent,
    Sum(q.late_flag) AS late_trips,
    Round(Avg(q.pickup_delay_minutes),1) AS avg_pickup_delay_minutes,
    Round(Avg(IIf(q.trip_id Is Null,Null,
        IIf(q.trip_status='Cancelled',1,0)))*100,1) AS cancellation_rate_percent,
    IIf(Count(q.on_time_flag)=0,'No valid trips',
        IIf(Avg(q.on_time_flag)<0.85,'Review Needed','Acceptable')) AS risk_flag
FROM contractors AS c
LEFT JOIN qValidPickupMetrics AS q ON c.contractor_id=q.contractor_id
GROUP BY c.contractor_id,c.contractor_name;
