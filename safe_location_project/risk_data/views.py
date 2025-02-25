import requests
from django.http import JsonResponse
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to Bharosa-AI</h1><p>Use /risk/get_risk_score/{latitude}/{longitude}/ to check risk score.</p>")


def get_risk_score(request, latitude, longitude):
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      node["amenity"="police"](around:1000,{latitude},{longitude});
      node["amenity"="hospital"](around:1000,{latitude},{longitude});
    );
    out;
    """
    response = requests.get(overpass_url, params={"data": query}).json()
    
    risk_score = len(response.get("elements", []))  # More police/hospitals → high-risk area
    return JsonResponse({"latitude": latitude, "longitude": longitude, "risk_score": risk_score})
