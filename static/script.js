const API_BASE_URL = "http://localhost:8000/api";

// Function to share location via WhatsApp
function sendLocation() {
    const userId = document.getElementById("userId").value;
    const friendPhone = document.getElementById("friendPhone").value;

    if (!userId || !friendPhone) {
        alert("Please enter your ID and your friend's phone number.");
        return;
    }

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(async (position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            const googleMapsLink = `https://www.google.com/maps?q=${lat},${lon}`;

            // Send location via WhatsApp
            const message = `Hey, I'm sharing my live location. Click here: ${googleMapsLink}`;
            const whatsappURL = `https://wa.me/${friendPhone}?text=${encodeURIComponent(message)}`;

            window.open(whatsappURL, "_blank"); // Open WhatsApp chat
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

// -------------------- VOICE ACTIVATION FEATURE --------------------

let mediaRecorder;
let audioChunks = [];

// Function to start voice recording
function startVoiceRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            audioChunks = [];

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
                sendAudioToWhatsApp(audioBlob);
            });

            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000); // Stop recording after 5 seconds
        })
        .catch(error => {
            console.error("Error accessing microphone:", error);
            alert("Microphone access denied or unavailable.");
        });
}

// Function to send recorded voice via WhatsApp
function sendAudioToWhatsApp(audioBlob) {
    const friendPhone = document.getElementById("friendPhone").value;

    if (!friendPhone) {
        alert("Please enter your friend's phone number before sending the voice note.");
        return;
    }

    // Create a download link for the audio
    const audioUrl = URL.createObjectURL(audioBlob);
    
    // WhatsApp does not allow direct media uploads, so we provide a manual sharing link
    alert("WhatsApp does not support direct voice message uploads. Please download the audio and share it manually.");
    
    // Create a temporary link for users to download the voice message
    const tempLink = document.createElement("a");
    tempLink.href = audioUrl;
    tempLink.download = "voice_message.wav";
    tempLink.click();
}
