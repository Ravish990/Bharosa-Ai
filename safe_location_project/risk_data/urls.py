from django.urls import path
from .views import get_risk_score

urlpatterns = [
    path('get_risk_score/<str:latitude>/<str:longitude>/', get_risk_score, name='risk_score'),
]
