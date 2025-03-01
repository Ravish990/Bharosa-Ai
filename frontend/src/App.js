import React, { useState } from "react";
import "./styles.css"; // Ensure styles are linked

const API_BASE_URL = "http://127.0.0.1:8000/risk/ai_risk";

function App() {
    const [userId, setUserId] = useState("");
    const [friendPhone, setFriendPhone] = useState("");
    const [city, setCity] = useState("");
    const [riskScore, setRiskScore] = useState(null);
    const [loading, setLoading] = useState(false);
    const [recordedAudioUrl, setRecordedAudioUrl] = useState("");
    const [mediaRecorder, setMediaRecorder] = useState(null);
    const [audioChunks, setAudioChunks] = useState([]);

    // Fetch Risk Score
    const fetchRiskScore = async () => {
        if (!city) {
            alert("Please enter a city name.");
            return;
        }

        setLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/${city}/`);
            if (!response.ok) {
                throw new Error("City not found");
            }

            const data = await response.json();
            setRiskScore(data.risk_score);
        } catch (error) {
            console.error("Error fetching risk score:", error);
            alert("Failed to fetch risk score. Please check the city name or try again.");
            setRiskScore(null);
        } finally {
            setLoading(false);
        }
    };

    // Share Location via WhatsApp
    const sendLocation = () => {
        if (!userId || !friendPhone) {
            alert("Please enter your ID and your friend's phone number.");
            return;
        }

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                const googleMapsLink = `https://www.google.com/maps?q=${lat},${lon}`;

                let message = `Hey, I'm sharing my live location. Click here: ${googleMapsLink}`;
                if (riskScore !== null) {
                    message += `\n🚨 City Risk Score: ${riskScore}/10 (Higher is more dangerous)`;
                }

                const whatsappURL = `https://wa.me/${friendPhone}?text=${encodeURIComponent(message)}`;
                window.open(whatsappURL, "_blank");
            });
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    };

    // Start Voice Recording
    const startVoiceRecording = () => {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                const recorder = new MediaRecorder(stream);
                setMediaRecorder(recorder);
                setAudioChunks([]);

                recorder.start();

                recorder.addEventListener("dataavailable", event => {
                    setAudioChunks(prevChunks => [...prevChunks, event.data]);
                });

                recorder.addEventListener("stop", () => {
                    const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    setRecordedAudioUrl(audioUrl);
                });

                setTimeout(() => {
                    recorder.stop();
                }, 5000);
            })
            .catch(error => {
                console.error("Error accessing microphone:", error);
                alert("Microphone access denied or unavailable.");
            });
    };

    return (
        <div>
            {/* Navigation */}
            <nav>
                <ul>
                    <li><a href="#"><i className="fas fa-home"></i> Home</a></li>
                    <li><a href="#stories"><i className="fas fa-book-open"></i> All Stories</a></li>
                    <li><a href="#about"><i className="fas fa-info-circle"></i> About Us</a></li>
                    <li><a href="#contact"><i className="fas fa-envelope"></i> Get in Touch</a></li>
                    <li><a href="trusted-contacts.html">Add Trusted Contacts</a></li>
                </ul>
            </nav>

            {/* Welcome Section */}
            <div className="welcome-section">
                <h1>Welcome to Bharosa AI</h1>
                <p>Empowering solutions with AI for a safer world.</p>
            </div>

            {/* Location Sharing with Risk Score */}
            <div className="location-section">
                <h2>Live Location Sharing with Risk Score</h2>
                <label>Your Unique ID:</label>
                <input 
                    type="text" 
                    value={userId} 
                    onChange={(e) => setUserId(e.target.value)}
                    placeholder="Enter your ID" 
                /><br /><br />

                <label>Friend's Phone Number:</label>
                <input 
                    type="tel" 
                    value={friendPhone} 
                    onChange={(e) => setFriendPhone(e.target.value)}
                    placeholder="Enter friend's phone number" 
                /><br /><br />

                <label>Enter City Name:</label>
                <input 
                    type="text" 
                    value={city} 
                    onChange={(e) => setCity(e.target.value)}
                    placeholder="Enter city name" 
                />
                <button onClick={fetchRiskScore} disabled={loading}>
                    {loading ? "Loading..." : "Check Risk Score"}
                </button>
                
                {riskScore !== null && (
                    <p style={{ fontSize: "24px", fontWeight: "bold", color: "red" }}>
                        🚨 Risk Score for {city}: {riskScore}/10
                    </p>
                )}

                <button onClick={sendLocation}>Share My Location</button>
            </div>

            {/* Voice Activation Feature */}
            <div className="voice-section">
                <h2>Record and Share Voice Message</h2>
                <button onClick={startVoiceRecording}>🎤 Start Recording</button>

                {recordedAudioUrl && (
                    <div>
                        <audio controls>
                            <source src={recordedAudioUrl} type="audio/wav" />
                            Your browser does not support the audio element.
                        </audio>
                        <a href={recordedAudioUrl} download="voice_message.wav">⬇️ Download Voice Message</a>
                    </div>
                )}
            </div>

            {/* Stories Section */}
            <div className="stories-section" id="stories">
                <h2>Discover Stories</h2>
                <div className="story-box">
                    <img src="https://www.ourbetterworld.org/sites/default/files/webform/ugc_form_women_empowerment/260644/2%20-%20a%20boy%20had%20been%20bothering%20me%20on%20Facebook%20sendin.png" alt="Story 1"/>
                    <h3>Environment</h3>
                    <p>Exploring how AI can save the environment.</p>
                </div>
            </div>

            {/* Footer */}
            <footer>
                <p>© 2025 Bharosa AI. All Rights Reserved.</p>
            </footer>
        </div>
    );
}

export default App;
