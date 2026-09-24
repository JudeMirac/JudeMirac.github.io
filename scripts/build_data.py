"""Rebuild the portfolio snapshot from the supplied SEPTA practice CSVs.

Usage: python3 scripts/build_data.py /path/to/extracted/source/csvs
Standard library only. Does not publish driver names or license identifiers.
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(sys.argv[1])
AS_OF = date(2026, 9, 24)

def read(name):
    with (SOURCE / f'{name}.csv').open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def stamp(value):
    return datetime.strptime(value, '%m/%d/%Y %H:%M') if value else None

def day(value):
    return datetime.strptime(value, '%m/%d/%Y').date() if value else None

def classify(status, scheduled, actual):
    if status != 'Completed' or scheduled is None or actual is None:
        return None, None
    # Source timestamps have minute precision, matching Access DateDiff("n", ...).
    delay = int((actual.replace(second=0, microsecond=0) - scheduled.replace(second=0, microsecond=0)).total_seconds() // 60)
    return delay, int(-5 <= delay <= 15)

tables = {name:read(name) for name in ['contractors','drivers','vehicles','trips','maintenance','compliance']}
for name, rows in tables.items():
    key = {'compliance':'compliance_id','maintenance':'maintenance_id'}.get(name, name[:-1]+'_id')
    assert all(row[key] for row in rows), f'Missing key: {name}'
    assert len({row[key] for row in rows}) == len(rows), f'Duplicate key: {name}'
contractors = {row['contractor_id']: row['contractor_name'] for row in tables['contractors']}
vehicles = {row['vehicle_id']: row for row in tables['vehicles']}
drivers = {row['driver_id']: row for row in tables['drivers']}
for row in tables['trips']:
    assert row['contractor_id'] in contractors
    assert not row['vehicle_id'] or row['vehicle_id'] in vehicles
    assert not row['driver_id'] or row['driver_id'] in drivers

trips=[]
for row in tables['trips']:
    scheduled, actual = stamp(row['scheduled_pickup']), stamp(row['actual_pickup'])
    delay, ontime=classify(row['trip_status'],scheduled,actual)
    trips.append({
        'trip_id':int(row['trip_id']), 'trip_date':day(row['trip_date']).isoformat(),
        'contractor_id':int(row['contractor_id']), 'contractor_name':contractors[row['contractor_id']],
        'trip_status':row['trip_status'],
        'scheduled_pickup':scheduled.isoformat(sep=' ') if scheduled else '',
        'actual_pickup':actual.isoformat(sep=' ') if actual else '',
        'pickup_delay_minutes':delay, 'valid_pickup':int(delay is not None),
        'on_time_flag':ontime, 'late_flag':int(delay>=16) if delay is not None else None,
        'early_flag':int(delay < -5) if delay is not None else None,
        'cancelled_flag':int(row['trip_status']=='Cancelled'),
        'completed_flag':int(row['trip_status']=='Completed'),
        'passenger_count':int(row['passenger_count']) if row['passenger_count'] else None,
        'distance_miles':float(row['distance_miles']) if row['distance_miles'] else None,
        'missing_actual_pickup':int(not row['actual_pickup']),
        'missing_actual_dropoff':int(not row['actual_dropoff']),
        'missing_driver':int(not row['driver_id']), 'missing_vehicle':int(not row['vehicle_id'])
    })

def summarize(rows):
    valid=[r for r in rows if r['valid_pickup']]
    completed=[r for r in rows if r['completed_flag']]
    ontime=sum(r['on_time_flag'] for r in valid)
    late=sum(r['late_flag'] for r in valid)
    early=sum(r['early_flag'] for r in valid)
    cancelled=sum(r['cancelled_flag'] for r in rows)
    assert ontime+late+early==len(valid)
    return {'trips':len(rows),'completed':len(completed),'valid_pickups':len(valid),
            'on_time':ontime,'late':late,'early':early,'cancelled':cancelled,
            'otp':100*ontime/len(valid) if valid else None,
            'cancellation_rate':100*cancelled/len(rows) if rows else None,
            'avg_delay':sum(r['pickup_delay_minutes'] for r in valid)/len(valid) if valid else None,
            'passengers':sum(r['passenger_count'] or 0 for r in completed),
            'excluded_pickups':len(rows)-len(valid),
            'completed_missing_pickups':len(completed)-len(valid)}

summary=summarize(trips)
by_contractor=[]
for cid,name in contractors.items():
    metric=summarize([r for r in trips if r['contractor_id']==int(cid)])
    metric.update({'id':int(cid),'name':name,'risk':'No valid trips' if metric['otp'] is None else ('Review Needed' if metric['otp']<85 else 'Acceptable')})
    by_contractor.append(metric)
by_date=[]
for d in sorted({row['trip_date'] for row in trips}):
    by_date.append({'date':d,**summarize([r for r in trips if r['trip_date']==d])})
maintenance=[]
for row in tables['maintenance']:
    vehicle=vehicles[row['vehicle_id']]
    maintenance.append({'maintenance_id':int(row['maintenance_id']),
        'contractor_name':contractors[vehicle['contractor_id']],
        'service_date':day(row['service_date']).isoformat(),'service_type':row['service_type'],
        'downtime_hours':float(row['downtime_hours']) if row['downtime_hours'] else None,
        'returned_to_service':stamp(row['returned_to_service']).isoformat(sep=' ') if row['returned_to_service'] else ''})
compliance=[]
for row in tables['compliance']:
    due=day(row['corrective_action_due'])
    compliance.append({'compliance_id':int(row['compliance_id']),
        'contractor_name':contractors[row['contractor_id']],
        'audit_date':day(row['audit_date']).isoformat(),'audit_type':row['audit_type'],
        'score':float(row['score']),'finding_count':int(row['finding_count']),
        'corrective_action_due':due.isoformat() if due else '',
        'corrective_action_closed':row['corrective_action_closed'],
        'overdue_open_flag':int(bool(due and due<AS_OF and row['corrective_action_closed']=='No')),
        'report_as_of':AS_OF.isoformat()})

snapshot={
    'provenance':'User-supplied SEPTA-inspired practice dataset; not official SEPTA performance.',
    'as_of':AS_OF.isoformat(),'start_date':min(r['trip_date'] for r in trips),'end_date':max(r['trip_date'] for r in trips),
    'counts':{k:len(v) for k,v in tables.items()},'summary':summary,
    'contractors':sorted(by_contractor,key=lambda r:(r['otp'] is None,r['otp'] or 0)),
    'daily':by_date,'trip_statuses':dict(Counter(r['trip_status'] for r in trips)),
    'quality':{k:sum(r[k] for r in trips) for k in ['missing_actual_pickup','missing_actual_dropoff','missing_driver','missing_vehicle']},
    'fleet':{'vehicles':len(vehicles),'out_of_service':sum(r['vehicle_status']=='Out of Service' for r in vehicles.values()),
             'maintenance_events':len(maintenance),'downtime_hours':sum(r['downtime_hours'] or 0 for r in maintenance),
             'service_types':dict(Counter(r['service_type'] for r in maintenance))},
    'compliance':{'audits':len(compliance),'overdue_open':sum(r['overdue_open_flag'] for r in compliance),
                  'open':sum(r['corrective_action_closed']=='No' for r in compliance),'as_of':AS_OF.isoformat()}}
ROOT.joinpath('data/transportation-summary.json').write_text(json.dumps(snapshot,indent=2)+'\n')
for filename,rows in [('transportation-trips',trips),('transportation-maintenance',maintenance),('transportation-compliance',compliance)]:
    with ROOT.joinpath(f'tableau/{filename}.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

# Boundary tests protect the earlier agreed inclusion rules.
t=datetime(2026,1,1,12)
from datetime import timedelta
for minutes,expected in [(-6,0),(-5,1),(0,1),(15,1),(16,0)]:
    assert classify('Completed',t,t+timedelta(minutes=minutes))[1]==expected
assert classify('Cancelled',t,t)==(None,None)
assert classify('Completed',t,None)==(None,None)
assert classify('Completed',None,t)==(None,None)
assert sum(r['valid_pickups'] for r in by_contractor)==summary['valid_pickups']
assert sum(r['on_time'] for r in by_contractor)==summary['on_time']
print(json.dumps({k:v for k,v in snapshot.items() if k not in ['daily']},indent=2))
