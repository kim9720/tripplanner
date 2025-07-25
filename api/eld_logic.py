from datetime import datetime, timedelta
from geopy.distance import geodesic

def calculate_eld_logs(trip):
    # Assumptions: 70hrs/8days, 1hr pickup/dropoff, fueling every 1000 miles
    max_cycle_hours = 9000
    max_daily_driving = 11
    max_daily_onduty = 14
    logs = []

    # Calculate distance
    start = (trip.current_location_lat, trip.current_location_lng)
    pickup = (trip.pickup_location_lat, trip.pickup_location_lng)
    dropoff = (trip.dropoff_location_lat, trip.dropoff_location_lng)
    distance_to_pickup = geodesic(start, pickup).miles
    distance_to_dropoff = geodesic(pickup, dropoff).miles
    total_distance = distance_to_pickup + distance_to_dropoff

    # Estimate driving time (60 mph average)
    driving_hours = total_distance / 60
    fueling_stops = int(total_distance / 1000) + 1
    total_onduty_hours = driving_hours + 1 + 1 + (fueling_stops * 0.5)  # 1hr pickup + 1hr dropoff + 0.5hr per fueling

    # Check cycle compliance
    if trip.current_cycle_hours + total_onduty_hours > max_cycle_hours:
        return None, "Exceeds 70-hour cycle limit"

    # Generate daily logs
    current_date = datetime.now().date()
    remaining_hours = driving_hours
    remaining_fueling = fueling_stops
    logs = []

    while remaining_hours > 0:
        daily_driving = min(remaining_hours, max_daily_driving)
        daily_onduty = min(daily_driving + 1 + 1 + (remaining_fueling * 0.5), max_daily_onduty)
        log = {
            'date': current_date.strftime('%Y-%m-%d'),
            'driving_hours': round(daily_driving, 2),
            'on_duty_hours': round(daily_onduty, 2),
            'off_duty_hours': round(24 - daily_onduty, 2),
            'fueling_stops': min(remaining_fueling, 1),
            'status_log': generate_status_log(daily_driving, daily_onduty, current_date),
        }
        logs.append(log)
        remaining_hours -= daily_driving
        remaining_fueling = max(0, remaining_fueling - 1)
        current_date += timedelta(days=1)

    return logs, None

def generate_status_log(driving_hours, on_duty_hours, date):
    status_log = []
    current_time = datetime.combine(date, datetime.min.time())
    
    status_log.append([current_time.isoformat(), 'Off-Duty'])
    current_time += timedelta(hours=1)
    status_log.append([current_time.isoformat(), 'On-Duty'])
    current_time += timedelta(hours=1)
    status_log.append([current_time.isoformat(), 'Driving'])
    current_time += timedelta(hours=driving_hours)
    status_log.append([current_time.isoformat(), 'On-Duty'])
    current_time += timedelta(hours=on_duty_hours - driving_hours - 1)
    status_log.append([current_time.isoformat(), 'Off-Duty'])
    
    return status_log
