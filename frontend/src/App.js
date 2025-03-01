import React, { useState } from "react";
import "./styles.css"; // Ensure styles are linked

const API_BASE_URL = "http://127.0.0.1:8000/risk/ai_risk";

function App() {
    const [userId, setUserId] = useState("");
    const [friendPhone, setFriendPhone] = useState("");
    const [city, setCity] = useState("");
    const [riskScore, setRiskScore] = useState(0);
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
            const data = await response.json();

            if (data.error) {
                alert("City not found. Please enter a valid city.");
                setRiskScore(0);
            } else {
                setRiskScore(data.risk_score || 0);
            }
        } catch (error) {
            console.error("Error fetching risk score:", error);
            alert("Failed to fetch risk score. Please try again.");
            setRiskScore(0);
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
                message += `\n🚨 City Risk Score: ${riskScore}/10 (Higher is more dangerous)`;

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
                    <li><a href="#home">Home</a></li>
                    <li><a href="#stories">All Stories</a></li>
                    <li><a href="#about">About Us</a></li>
                    <li><a href="#contact">Get in Touch</a></li>
                    <li><a href="trusted-contacts.html">Add Trusted Contacts</a></li>
                </ul>
            </nav>

            {/* Welcome Section */}
            <div className="welcome-section" id="home">
                <h1>Welcome to Bharosa AI</h1>
                <p>Empowering solutions with AI for a safer world.</p>
            </div>

            {/* Location Sharing with Risk Score */}
            <div className="location-section" id="location">
                <h2>Live Location Sharing with Risk Score</h2>
                <div className="input-group">
                    <label>Your Unique ID:</label>
                    <input 
                        type="text" 
                        value={userId} 
                        onChange={(e) => setUserId(e.target.value)}
                        placeholder="Enter your ID" 
                    />
                </div>
                <div className="input-group">
                    <label>Friend's Phone Number:</label>
                    <input 
                        type="tel" 
                        value={friendPhone} 
                        onChange={(e) => setFriendPhone(e.target.value)}
                        placeholder="Enter friend's phone number" 
                    />
                </div>
                <div className="input-group">
                    <label>Enter City Name:</label>
                    <input 
                        type="text" 
                        value={city} 
                        onChange={(e) => setCity(e.target.value)}
                        placeholder="Enter city name" 
                    />
                </div>
                <button onClick={fetchRiskScore} disabled={loading}>
                    {loading ? "Loading..." : "Check Risk Score"}
                </button>

                {/* Risk Score Display */}
                <div className="risk-score">
                    🚨 Risk Score for {city || "Unknown City"}: <span>{riskScore}/10</span>
                </div>

                <button onClick={sendLocation}>Share My Location</button>
            </div>

            {/* Voice Activation Feature */}
            <div className="voice-section" id="voice">
                <h2>Record and Download Voice Message</h2>
                <button onClick={startVoiceRecording}>🎤 Start Recording</button>

                {recordedAudioUrl && (
                    <div>
                        <a href={recordedAudioUrl} download="voice_message.wav">⬇️ Download Voice Message</a>
                    </div>
                )}
            </div>

            {/* Stories Section */}
            <div className="stories-section" id="stories">
                <h2>Discover Stories</h2>
                <div className="story-box">
                    <img src="https://www.ourbetterworld.org/sites/default/files/webform/ugc_form_women_empowerment/260644/2%20-%20a%20boy%20had%20been%20bothering%20me%20on%20Facebook%20sendin.png" alt="Story 1" />
                    <h3>Environment</h3>
                    <p>Exploring how AI can save the environment.</p>
                </div>
            </div>

            {/* Footer */}
            <footer id="contact">
                <p>© 2025 Bharosa AI. All Rights Reserved.</p>
            </footer>

            {/* CSS Styles */}
            <style>{`
                /* Basic Reset */
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }

                /* Body styles */
                body {
                    font-family: 'Poppins', sans-serif;
                    background-image: url('https://static.lsm.lv/media/2020/11/large/1/ebr4.jpg');
                    background-size: cover;
                    background-position: center;
                    color: #333;
                    overflow-x: hidden;
                }

                /* Navigation Bar */
                nav {
                    width: 100%;
                    background-color: rgba(26, 188, 156, 0.9);
                    position: fixed;
                    top: 0;
                    left: 0;
                    z-index: 100;
                    padding: 10px 0;
                }

                nav ul {
                    display: flex;
                    list-style: none;
                    justify-content: center;
                }

                nav ul li {
                    margin: 0 30px;
                }

                nav ul li a {
                    color: #fff;
                    text-decoration: none;
                    font-size: 1.5rem;
                    font-weight: 500;
                    transition: color 0.3s ease;
                }

                nav ul li a:hover {
                    color: #f39c12;
                }

                /* Welcome Section */
                .welcome-section {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                    height: 100vh;
                    margin-top: 60px; /* to account for fixed nav */
                    background-color: rgba(255, 255, 255, 0.9);
                }

                /* Location Sharing with Risk Score */
                .location-section {
                    display: flex;
                    flex-direction: column;
                    align-items: flex-start;
                    justify-content: center;
                    background-color: rgba(255, 255, 255, 0.8);
                    padding: 20px;
                    margin: 20px auto;
                    border-radius: 8px;
                    width: 80%;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                }

                .input-group {
                    margin-bottom: 15px;
                    width: 100%;
                }

                .input-group label {
                    display: block;
                    margin-bottom: 5px;
                }

                .input-group input {
                    width: calc(100% - 16px);
                    padding: 8px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }

                .risk-score {
                    font-size: 28px;
                    font-weight: bold;
                    color: red;
                    margin-top: 10px;
                }

                /* Voice Section */
                .voice-section {
                    background-color: rgba(255, 255, 255, 0.8);
                    padding: 20px;
                    margin: 20px auto;
                    border-radius: 8px;
                    width: 80%;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                    text-align: center;
                }

                /* Stories Section */
                .stories-section {
                    padding: 40px 20px;
                    text-align: center;
                }

                .story-box {
                    display: inline-block;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 15px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                    width: 300px;
                    transition: transform 0.3s;
                }

                .story-box:hover {
                    transform: scale(1.05);
                }

                .story-box img {
                    width: 100%;
                    height: 160px;
                    object-fit: cover;
                    border-radius: 10px;
                    margin-bottom: 10px;
                }

                /* Footer Section */
                footer {
                    background-color: #34495e;
                    color: #fff;
                    padding: 30px;
                    text-align: center;
                }
            `}</style>
        </div>
    );
}

export default App;