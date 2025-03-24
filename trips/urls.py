from django.urls import path
from django.http import JsonResponse
from .views import TripListCreateView, TripDetailView, LatestTripView


def api_root(request):
    return JsonResponse({"message": "Welcome to the Trip Planner API!"})


urlpatterns = [
    path("", api_root, name="api-root"),
    path("trips/", TripListCreateView.as_view(), name="trip-list"),
    path("trips/<int:pk>/", TripDetailView.as_view(), name="trip-detail"),
    path("trips/latest/", LatestTripView.as_view(), name="latest-trip"),
]
