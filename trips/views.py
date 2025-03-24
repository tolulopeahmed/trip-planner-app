from rest_framework import generics
from .models import Trip
from .serializers import TripSerializer


# API View for Creating & Listing Trips
class TripListCreateView(generics.ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


from datetime import timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Trip
from .serializers import TripSerializer


class TripPlannerView(APIView):
    def post(self, request):
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            trip = serializer.save()

            # Assumptions: Stops every 1000 miles, 1-hour pickup/dropoff
            stops = []
            distance_miles = trip.estimated_distance  # Example field
            stop_count = distance_miles // 1000

            for i in range(int(stop_count)):
                stops.append(
                    {
                        "time": str(trip.start_time + timedelta(hours=i * 5)),
                        "location": f"Stop {i+1}",
                        "reason": "Fueling",
                    }
                )

            # Adding pickup and dropoff times
            stops.append(
                {
                    "time": str(trip.start_time),
                    "location": trip.pickup_location,
                    "reason": "Pickup (1-hour)",
                }
            )
            stops.append(
                {
                    "time": str(trip.start_time + timedelta(hours=trip.estimated_time)),
                    "location": trip.dropoff_location,
                    "reason": "Dropoff (1-hour)",
                }
            )

            return Response(
                {"trip": TripSerializer(trip).data, "stops": stops}, status=201
            )

        return Response(serializer.errors, status=400)
