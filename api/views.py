from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class TripPlanView(APIView):
    def post(self, request):
        data = request.data
        current_location = data.get("current_location")
        pickup_location = data.get("pickup_location")
        dropoff_location = data.get("dropoff_location")
        cycle_hours = data.get("cycle_hours")

        # Simulate logic (later you'll add real route + log sheet generation)
        response_data = {
            "message": "Trip planned successfully",
            "route": [current_location, pickup_location, dropoff_location],
            "stops": ["Rest Stop 1", "Fuel Stop"],
        }
        return Response(response_data, status=status.HTTP_200_OK)
