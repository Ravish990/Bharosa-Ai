const BASE_URL = "http://127.0.0.1:8000";

export const fetchRiskData = async (city) => {
    console.log(`📡 Fetching risk data for: ${city}`);
    try {
        const response = await fetch(`${BASE_URL}/risk/ai_risk/${city}/`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        console.log("✅ Fetched Risk Data:", data);
        return data;
    } catch (error) {
        console.error("❌ Fetch error:", error);
        return { error: "Failed to fetch data" };
    }
};
