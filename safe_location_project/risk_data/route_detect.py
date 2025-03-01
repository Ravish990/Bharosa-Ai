import geopy.distance
import requests
import speech_recognition as sr
from textblob import TextBlob
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# OpenRouteService Free API Key
ORS_API_KEY = "5b3ce3597851110001cf6248a10a79fd6b38422da5ac6090b8ed500e"
ORS_BASE_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

# Expected route (Waypoints)
EXPECTED_ROUTE = [(12.9716, 77.5946), (12.9726, 77.5956)]  # Example coordinates

# 1. Route Deviation Detection
def check_route_deviation(current_location):
    closest_distance = min(
        geopy.distance.geodesic(current_location, waypoint).meters
        for waypoint in EXPECTED_ROUTE
    )
    deviation_threshold = 50  # meters
    return closest_distance > deviation_threshold

# 2. Distress Message Analysis
def analyze_text_distress(message):
    analysis = TextBlob(message)
    return analysis.sentiment.polarity < -0.3  # Negative sentiment threshold

# 3. Voice Panic Detection
def detect_voice_panic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for panic...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return analyze_text_distress(text)  # Use same NLP distress check
    except Exception as e:
        print("Voice recognition failed:", e)
        return False

@csrf_exempt
def safety_check(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        current_location = tuple(data.get("location"))
        message = data.get("message", "")
        
        # Check for route deviation
        deviated = check_route_deviation(current_location)
        
        # Check for distress signals
        text_panic = analyze_text_distress(message) if message else False
        voice_panic = detect_voice_panic()
        
        alert_triggered = deviated or text_panic or voice_panic
        
        if alert_triggered:
            send_alert_to_contacts()
        
        return JsonResponse({"deviated": deviated, "text_panic": text_panic, "voice_panic": voice_panic, "alert_triggered": alert_triggered})

def send_alert_to_contacts():
    print("⚠️ ALERT: User in distress! Sending notifications...")
    # Integrate Free SMS API (like Textbelt) or WebSocket notifications here
