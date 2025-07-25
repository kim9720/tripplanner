from django.db import models

class Trip(models.Model):
    driver_id = models.CharField(max_length=50)
    current_location_lat = models.FloatField()
    current_location_lng = models.FloatField()
    pickup_location_lat = models.FloatField()
    pickup_location_lng = models.FloatField()
    dropoff_location_lat = models.FloatField()
    dropoff_location_lng = models.FloatField()
    current_cycle_hours = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trip for Driver {self.driver_id} from ({self.pickup_location_lat}, {self.pickup_location_lng}) to ({self.dropoff_location_lat}, {self.dropoff_location_lng})"

class LogSheet(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='log_sheets')
    date = models.DateField()
    driving_hours = models.FloatField()
    on_duty_hours = models.FloatField()
    off_duty_hours = models.FloatField()
    fueling_stops = models.IntegerField()
    status_log = models.JSONField()

    def __str__(self):
        return f"Log for {self.trip} on {self.date}"
