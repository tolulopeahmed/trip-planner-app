from django.db import models
from django.utils.timezone import now  # ✅ Import `now` correctly


class Trip(models.Model):
    current_location = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    current_cycle_hours = models.FloatField()
    start_time = models.DateTimeField(
        default=now
    )  # ✅ Auto-fills with the current timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()  # Explicitly define objects manager

    def __str__(self):
        return f"Trip from {self.pickup_location} to {self.dropoff_location}"
