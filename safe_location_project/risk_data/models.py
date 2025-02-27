from django.db import models

class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class RiskyLocation(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    risk_score = models.FloatField()  # Risk level from 0 (safe) to 10 (dangerous)
    description = models.TextField()

    def __str__(self):
        return f"Risk Score: {self.risk_score} at ({self.latitude}, {self.longitude})"
