from django.urls import path
from .views import home, get_risk_score, get_ai_risk_score, get_risk_by_city

urlpatterns = [
    path('', home, name='home'),
    path('get_risk_score/<str:latitude>/<str:longitude>/', get_risk_score, name='risk_score'),
    path('get_risk_by_city/<str:city>/', get_risk_by_city, name='risk_by_city'),
    path('ai_risk/<int:crime_type>/', get_ai_risk_score, name='ai_risk_score'),
    path('ai_risk/<str:city>/', get_ai_risk_score, name='ai_risk_score'),

]
