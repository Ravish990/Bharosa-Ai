const API_BASE_URL = "http://localhost:8000/api";

// Store trusted contacts at login
function storeTrustedContacts(userId, trustedContacts) {
    fetch(`${API_BASE_URL}/trusted_contacts`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, trusted_contacts: trustedContacts })
    })
    .then(response => response.json())
    .then(data => console.log(data.message))
    .catch(error => console.error("Error saving trusted contacts"));
}

// Function to share location
function sendLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const userId = prompt("Enter your User ID:");
            const trustedContacts = prompt("Enter trusted contacts (comma separated User IDs):").split(",");

            const locationData = {
                user_id: userId,
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
                timestamp: Date.now(),
                trusted_contacts: trustedContacts
            };

            fetch(`${API_BASE_URL}/location/share`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(locationData)
            })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(error => alert("Error sharing location"));
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

// Function to get location
function getLocation() {
    const userId = document.getElementById("userId").value;
    const requesterId = prompt("Enter your User ID to verify:");

    fetch(`${API_BASE_URL}/location/${userId}/${requesterId}`)
        .then(response => response.json())
        .then(data => {
            if (data.latitude && data.longitude) {
                document.getElementById("locationResult").innerText =
                    `Latitude: ${data.latitude}, Longitude: ${data.longitude}`;

                updateMap(data.latitude, data.longitude);
            } else {
                alert("Location not found.");
            }
        })
        .catch(error => alert("User location not found"));
}

// Initialize Google Map
let map;
function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 0, lng: 0 },
        zoom: 5
    });
}

// Update Map with User Location
function updateMap(lat, lng) {
    const userLocation = new google.maps.LatLng(lat, lng);
    map.setCenter(userLocation);
    map.setZoom(15);

    new google.maps.Marker({
        position: userLocation,
        map: map,
        title: "User's Location"
    });
}
