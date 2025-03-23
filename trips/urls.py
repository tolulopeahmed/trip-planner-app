from django.urls import path
from .views import TripListCreateView, TripDetailView


urlpatterns = [
    path("trips/", TripListCreateView.as_view(), name="trip-list"),
    path("trips/<int:pk>/", TripDetailView.as_view(), name="trip-detail"),
]
