import os
import django

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "safe_location.settings")
django.setup()

from risk_data.models import RiskyLocation

# Insert Sample Risky Locations
data = [
    {"latitude": 12.9716, "longitude": 77.5946, "risk_score": 8.5, "description": "High crime area at night"},
    {"latitude": 28.7041, "longitude": 77.1025, "risk_score": 7.0, "description": "Pickpocketing incidents reported"},
]

for entry in data:
    RiskyLocation.objects.create(**entry)

print("Risky Locations Added to Database!")
