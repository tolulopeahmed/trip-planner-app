from datetime import timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import Trip
from .serializers import TripSerializer


# Helper function: Calculate trip distance (Example: returns 2000 miles)
def calculate_trip_distance(pickup, dropoff):
    return 2000  # Replace with actual logic


# Helper function: Get fuel stop location (Example: returns a mock location)
def get_fuel_stop_location(stop_number, pickup, dropoff):
    return f"Fuel Stop {stop_number}"  # Replace with actual logic


# Helper function: Add hours to time
def add_hours_to_time(start_time, hours):
    return start_time + timedelta(hours=hours)


# Function to generate trip stops
def generate_stops(trip):
    stops = []

    # Add pickup stop
    stops.append(
        {"time": trip.start_time, "location": trip.pickup_location, "reason": "Pickup"}
    )

    # Generate fueling stops every 1,000 miles
    total_miles = calculate_trip_distance(trip.pickup_location, trip.dropoff_location)
    fuel_stops = total_miles // 1000  # One stop every 1000 miles

    for i in range(1, fuel_stops + 1):
        stop_location = get_fuel_stop_location(
            i, trip.pickup_location, trip.dropoff_location
        )
        stops.append(
            {
                "time": add_hours_to_time(
                    trip.start_time, i * 10
                ),  # Assuming 10hrs per 1,000 miles
                "location": stop_location,
                "reason": "Fueling",
            }
        )

    # Add drop-off stop
    stops.append(
        {
            "time": add_hours_to_time(
                trip.start_time, total_miles // 50
            ),  # Assuming avg 50mph speed
            "location": trip.dropoff_location,
            "reason": "Drop-off",
        }
    )

    return stops


# API View for Creating & Listing Trips
class TripListCreateView(generics.ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


class TripPlannerView(APIView):
    def post(self, request):
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            trip = serializer.save()

            # Generate stops
            stops = generate_stops(trip)

            return Response(
                {"trip": TripSerializer(trip).data, "stops": stops}, status=201
            )

        return Response(serializer.errors, status=400)


class LatestTripView(APIView):
    def get(self, request):
        latest_trip = Trip.objects.order_by("-start_time").first()  # Get latest trip
        if latest_trip:
            stops = generate_stops(latest_trip)
            return Response(
                {"trip": TripSerializer(latest_trip).data, "stops": stops}, status=200
            )

        return Response({"message": "No trips found."}, status=404)
