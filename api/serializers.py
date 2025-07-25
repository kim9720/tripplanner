from rest_framework import serializers
from .models import Trip, LogSheet
from .eld_logic import calculate_eld_logs

class LogSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogSheet
        fields = ['date', 'driving_hours', 'on_duty_hours', 'off_duty_hours', 'fueling_stops', 'status_log']

class TripSerializer(serializers.ModelSerializer):
    log_sheets = LogSheetSerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = [
            'id', 'driver_id', 'current_location_lat', 'current_location_lng',
            'pickup_location_lat', 'pickup_location_lng',
            'dropoff_location_lat', 'dropoff_location_lng',
            'current_cycle_hours', 'created_at', 'log_sheets'
        ]

    def validate(self, data):
        if not data.get('driver_id').strip():
            raise serializers.ValidationError({'driver_id': 'Driver ID is required'})
        return data

    def create(self, validated_data):
        trip = Trip.objects.create(**validated_data)
        logs, error = calculate_eld_logs(trip)
        if error:
            raise serializers.ValidationError({'error': error})
        for log in logs:
            LogSheet.objects.create(trip=trip, **log)
        return trip
