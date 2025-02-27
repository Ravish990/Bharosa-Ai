import React, { useState } from "react";
import { fetchRiskData } from "./Api";  // ✅ Ensure the correct filename

const App = () => {
    const [city, setCity] = useState("");
    const [riskData, setRiskData] = useState(null);
    const [error, setError] = useState(null);  // ✅ Add error handling

    const checkRisk = async () => {
        setError(null);  // Reset error before fetching
        if (!city.trim()) {
            setError("Please enter a valid city name.");
            return;
        }

        try {
            const data = await fetchRiskData(city);
            if (data.error) {
                setError(data.error);
                setRiskData(null);
            } else {
                setRiskData(data);
            }
        } catch (err) {
            setError("Failed to fetch data. Try again.");
        }
    };

    return (
        <div style={{ textAlign: "center", marginTop: "20px" }}>
            <h2>Check Risk Level</h2>
            <input 
                type="text" 
                placeholder="Enter city" 
                value={city} 
                onChange={(e) => setCity(e.target.value)}
                style={{ padding: "8px", marginRight: "10px" }}
            />
            <button onClick={checkRisk} style={{ padding: "8px 15px", cursor: "pointer" }}>
                Check
            </button>

            {error && <p style={{ color: "red" }}>{error}</p>}

            {riskData && (
                <div style={{ marginTop: "20px" }}>
                    <h3>Risk Score: {riskData.ai_risk_score}</h3>
                    <p>{riskData.ai_risk_message}</p>
                </div>
            )}
        </div>
    );
};

export default App;
