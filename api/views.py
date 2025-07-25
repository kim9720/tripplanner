from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Trip
from .serializers import TripSerializer

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        driver_id = self.request.query_params.get('driver_id')
        if driver_id:
            queryset = queryset.filter(driver_id=driver_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trip = serializer.save()
        response_data = {
            'trip': {
                'driver_id': trip.driver_id,
                'current_location': [trip.current_location_lat, trip.current_location_lng],
                'pickup_location': [trip.pickup_location_lat, trip.pickup_location_lng],
                'dropoff_location': [trip.dropoff_location_lat, trip.dropoff_location_lng],
            },
            'logs': [
                {
                    'date': log.date.strftime('%Y-%m-%d'),
                    'driving_hours': log.driving_hours,
                    'on_duty_hours': log.on_duty_hours,
                    'off_duty_hours': log.off_duty_hours,
                    'fueling_stops': log.fueling_stops,
                    'status_log': log.status_log,
                } for log in trip.log_sheets.all()
            ]
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
