import requests
import joblib
import numpy as np
import os
from django.http import JsonResponse, HttpResponse
from geopy.geocoders import Nominatim
from twilio.rest import Client  # Twilio for SMS
from django.views.decorators.csrf import csrf_exempt

# Home Page
def home(request):
    return HttpResponse("""
        <h1>Welcome to Bharosa-AI</h1>
        <p>Use the following endpoints:</p>
        <ul>
            <li><b>Risk Score by City:</b> /risk/get_risk_by_city/&lt;city&gt;/</li>
            <li><b>Risk Score by Coordinates:</b> /risk/get_risk_score/&lt;latitude&gt;/&lt;longitude&gt;/</li>
            <li><b>AI Predicted Risk:</b> /risk/ai_risk/&lt;city&gt;/</li>
        </ul>
    """)

# Load AI Model
model_path = os.path.join("ai_model","ai_model", "crime_risk_model.pkl")
model = joblib.load(model_path) if os.path.exists(model_path) else None

# Twilio SMS Credentials (Replace with actual credentials)
TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "+1234567890"
ALERT_PHONE_NUMBER = "+919569638704"

try:
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
except Exception as e:
    print(f"⚠️ Twilio Initialization Failed: {e}")
    client = None

def send_sms_alert(message):
    """Send an SMS alert using Twilio."""
    if client:
        try:
            sms = client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to=ALERT_PHONE_NUMBER
            )
            print(f"📩 SMS Sent! SID: {sms.sid}")
        except Exception as e:
            print(f"⚠️ Failed to send SMS: {e}")
    else:
        print("⚠️ Twilio Client not initialized.")

def assess_risk(score):
    """Convert a numerical risk score into a human-readable message."""
    if score >= 8:
        return "🔴 High Risk! Avoid if possible."
    elif 4 <= score < 8:
        return "🟠 Moderate Risk. Be cautious."
    else:
        return "🟢 Low Risk. Generally safe."

def get_lat_lon(location_name):
    """Convert location (city or area) to latitude and longitude using Geopy."""
    try:
        geolocator = Nominatim(user_agent="bharosa-ai")
        location = geolocator.geocode(location_name + ", India")  # Add country for better accuracy

        if location:
            return location.latitude, location.longitude
        
        return None, None
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
        return None, None


def get_risk_by_city(request, city):
    """Fetch the risk score by city name."""
    latitude, longitude = get_lat_lon(city)
    if latitude is None or longitude is None:
        return JsonResponse({"error": "City not found or invalid."}, status=400)
    
    return get_risk_score(request, latitude, longitude)

def get_risk_score(request, latitude, longitude):
    """Fetch risk score based on latitude and longitude."""
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return JsonResponse({"error": "Invalid latitude or longitude format."}, status=400)

    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      node["amenity"="police"](around:1000,{latitude},{longitude});
      node["amenity"="hospital"](around:1000,{latitude},{longitude});
    );
    out;
    """
    
    try:
        response = requests.get(overpass_url, params={"data": query}).json()
        risk_score = len(response.get("elements", []))
        risk_message = assess_risk(risk_score)

        if risk_score >= 8:
            sms_message = f"🚨 ALERT: High-risk area detected near ({latitude}, {longitude}). {risk_message}"
            send_sms_alert(sms_message)

        return JsonResponse({
            "latitude": latitude,
            "longitude": longitude,
            "risk_score": risk_score,
            "risk_message": risk_message
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def get_ai_risk_score(request, city=None, latitude=None, longitude=None):
    """Fetch AI-predicted risk score by city OR latitude/longitude."""
    
    if city:
        latitude, longitude = get_lat_lon(city)  # Convert city to lat/lon
        if latitude is None or longitude is None:
            return JsonResponse({"error": "Invalid city name."}, status=400)
    elif latitude and longitude:
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            return JsonResponse({"error": "Invalid latitude or longitude format."}, status=400)
    else:
        return JsonResponse({"error": "Provide a city or latitude/longitude."}, status=400)

    # Debugging log
    print(f"AI Risk Prediction -> City: {city}, Lat: {latitude}, Lon: {longitude}")

    if model:
        try:
            num_features = model.n_features_in_
            if num_features == 1:
                risk_features = np.array([[latitude]])
            else:
                risk_features = np.array([[latitude, longitude]])

            risk_score = model.predict(risk_features)[0]
            risk_score = int(risk_score)  # Convert to Python int
            risk_message = assess_risk(risk_score)

        except Exception as e:
            return JsonResponse({"error": f"AI model prediction error: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "AI model not loaded."}, status=500)

    return JsonResponse({
        "latitude": latitude,
        "longitude": longitude,
        "ai_risk_score": risk_score,
        "ai_risk_message": risk_message
    })
