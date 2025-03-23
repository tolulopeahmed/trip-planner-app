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


from django.contrib import admin
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = (
        "pickup_location",
        "dropoff_location",
        "current_cycle_hours",
        "created_at",
    )
    search_fields = ("pickup_location", "dropoff_location")
