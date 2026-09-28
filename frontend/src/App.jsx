import { useEffect, useState } from "react";
import "./App.css";
import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";


function App() {
  const [weather, setWeather] = useState(null);
  const [airQuality, setAirQuality] = useState(null);
  const [riskData, setRiskData] = useState(null);
  const [riskLoading, setRiskLoading] = useState(true);
  const [riskError, setRiskError] = useState(false);

  const [weatherLoading, setWeatherLoading] = useState(true);
  const [airLoading, setAirLoading] = useState(true);

  const [weatherError, setWeatherError] = useState(false);
  const [airError, setAirError] = useState(false);

  const [mode, setMode] = useState("citizen");
  const [activeTab, setActiveTab] = useState("Overview");
  const [mapLayer, setMapLayer] = useState("air");
  const [alertsOpen, setAlertsOpen] = useState(false);
  const [askAiraOpen, setAskAiraOpen] = useState(false);
  const [airaQuestion, setAiraQuestion] = useState("");
  const [airaMessages, setAiraMessages] = useState([]);
  const [mapView, setMapView] = useState("map");

  const location = "Shillong, Meghalaya";

  useEffect(() => {
    fetch(
      "https://api.open-meteo.com/v1/forecast?latitude=25.5788&longitude=91.8933&current=temperature_2m,relative_humidity_2m,wind_speed_10m,surface_pressure,weather_code"
    )
      .then((response) => {
        if (!response.ok) throw new Error("Weather API error");
        return response.json();
      })
      .then((data) => {
        setWeather(data.current);
        setWeatherLoading(false);
      })
      .catch((error) => {
        console.error("Weather error:", error);
        setWeatherError(true);
        setWeatherLoading(false);
      });

    fetch(
      "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=25.5788&longitude=91.8933&current=us_aqi,pm2_5,pm10,ozone,nitrogen_dioxide"
    )
      .then((response) => {
        if (!response.ok) throw new Error("Air quality API error");
        return response.json();
      })
      .then((data) => {
        setAirQuality(data.current);
        setAirLoading(false);
      })
      .catch((error) => {
        console.error("Air quality error:", error);
        setAirError(true);
        setAirLoading(false);
      });
  }, []);


    useEffect(() => {
    if (airQuality?.us_aqi == null) return;

    const windSpeed = weather?.wind_speed_10m ?? null;

    fetch("/api/risk", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        aqi: airQuality.us_aqi,
        anomaly_score: 0,
        wind_speed_kmh: windSpeed,
      }),
    })
      .then((response) => {
        if (!response.ok) throw new Error("Risk API error");
        return response.json();
      })
      .then((data) => {
        setRiskData(data);
        setRiskLoading(false);
      })
      .catch((error) => {
        console.error("Risk error:", error);
        setRiskError(true);
        setRiskLoading(false);
      });
  }, [airQuality, weather]);
  const getAirStatus = () => {
    if (!airQuality) return "Data unavailable";

    if (airQuality.us_aqi <= 50) return "Good";
    if (airQuality.us_aqi <= 100) return "Moderate";
    if (airQuality.us_aqi <= 150) return "Unhealthy for sensitive groups";
    if (airQuality.us_aqi <= 200) return "Unhealthy";

    return "Very unhealthy";
  };

  const getRisk = () => {
    if (!airQuality) return "Data unavailable";

    if (airQuality.us_aqi <= 50) return "Low";
    if (airQuality.us_aqi <= 100) return "Moderate";

    return "High";
  };

  const formatValue = (value, unit = "") => {
    if (value === null || value === undefined) return "--";
    return `${value}${unit}`;
  };
  const handleAskAira = () => {
    const question = airaQuestion.trim();

    if (!question) return;

    let answer = "";

    const lowerQuestion = question.toLowerCase();

  if (
    lowerQuestion.includes("air quality") ||
    lowerQuestion.includes("aqi") ||
    lowerQuestion.includes("pollution")
  ) {
    if (airQuality?.us_aqi != null) {
      answer = `The current air quality in ${location} is ${getAirStatus()} with a US AQI of ${airQuality.us_aqi}.`;
    } else {
      answer = "Air-quality data is currently unavailable.";
    }
  } else if (
    lowerQuestion.includes("weather") ||
    lowerQuestion.includes("temperature") ||
    lowerQuestion.includes("hot") ||
    lowerQuestion.includes("cold")
  ) {
    if (weather?.temperature_2m != null) {
      answer = `The current temperature in ${location} is ${weather.temperature_2m}°C.`;
    } else {
      answer = "Weather data is currently unavailable.";
    }
  } else if (
    lowerQuestion.includes("risk") ||
    lowerQuestion.includes("safe")
  ) {
    if (airQuality?.us_aqi != null) {
      answer = `Based on the available air-quality measurement, the current environmental risk assessment for ${location} is ${getRisk()}.`;
    } else {
      answer = "An environmental risk assessment cannot be calculated because the required data is unavailable.";
    }
  } else {
    answer =
      "I can currently answer questions about the environmental data available to AIRA, such as air quality, AQI, weather and environmental risk.";
  }

  setAiraMessages((messages) => [
    ...messages,
    { type: "user", text: question },
    { type: "aira", text: answer },
  ]);

  setAiraQuestion("");
};

  return (
    <div className="app">

      {/* HEADER */}
      <header className="header">

        <div className="brand">
          <h1>AIRA</h1>
          <p>
            Environmental Monitoring
            <br />
            & Risk Assessment
          </p>
        </div>

        <div className="mode-switch">
          <button
            className={mode === "citizen" ? "active" : ""}
            onClick={() => setMode("citizen")}
          >
            Citizen <span>→</span>
          </button>

          <button
            className={mode === "government" ? "active" : ""}
            onClick={() => setMode("government")}
          >
            Command Center <span>→</span>
          </button>
        </div>
      
        <div className="location">
          <div className="location-text">
            <div className="location-title">
              <svg
                className="location-icon"
                viewBox="0 0 24 24"
                aria-hidden="true"
            >
                <path
                  d="M12 21s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12Z"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                />
                <circle
                  cx="12"
                  cy="9"
                  r="2.5"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                />
              </svg>

              <span>Current Location</span>
            </div>

            <strong>{location}</strong>
          </div>
         </div>
    
      </header>

      {/* ================= CITIZEN ================= */}

      {mode === "citizen" && (
        <main className="citizen-page">

          <section className="location-banner">
           <div className="location-banner-content">
             <p className="section-label">ENVIRONMENTAL STATUS</p>

             <h2>Your area</h2>

             <p className="large-location">
               <span>●</span> {location}
             </p>

             <p className="location-summary">
               Environmental conditions and air quality for your current area.
            </p>
         </div>

         <div className="location-status">
           <span className="status-dot"></span>
           <div>
             <strong>Environmental status</strong>
             <span>Based on available data</span>
          </div>
        </div>
     </section>

          <div className="citizen-grid">

            {/* WEATHER */}

            <section className="data-card">

              <div className="card-title">
                <h2>Weather</h2>
                <span className="source-label">Open-Meteo</span>
              </div>

              {weatherLoading ? (
                <p className="state-message">Loading weather data...</p>
              ) : weatherError ? (
                <p className="state-message error">
                  Weather data unavailable.
                </p>
              ) : (
                <>
                  <div className="primary-value">
                    {formatValue(weather?.temperature_2m, "°C")}
                  </div>

                  <p className="description">
                    Current local conditions
                  </p>

                  <div className="metric-list">

                    <div>
                      <span>Humidity</span>
                      <strong>
                        {formatValue(
                          weather?.relative_humidity_2m,
                          "%"
                        )}
                      </strong>
                    </div>

                    <div>
                      <span>Wind Speed</span>
                      <strong>
                        {formatValue(
                          weather?.wind_speed_10m,
                          " km/h"
                        )}
                      </strong>
                    </div>

                    <div>
                      <span>Pressure</span>
                      <strong>
                        {formatValue(
                          weather?.surface_pressure,
                          " hPa"
                        )}
                      </strong>
                    </div>

                  </div>
                </>
              )}

            </section>

            {/* AIR QUALITY */}

            <section className="data-card">

              <div className="card-title">
                <h2>Air Quality</h2>
                <span className="source-label">
                  Open-Meteo
                </span>
              </div>

              {airLoading ? (
                <p className="state-message">
                  Loading air-quality data...
                </p>
              ) : airError ? (
                <p className="state-message error">
                  Air-quality data unavailable.
                </p>
              ) : (
                <>
                  <div className="aqi-row">

                    <div className="primary-value green">
                      {airQuality?.us_aqi ?? "--"}
                    </div>

                    <span className="status-badge">
                      {getAirStatus()}
                    </span>

                  </div>

                  <p className="description">
                    Current air quality in your area
                  </p>

                  <div className="metric-list">

                    <div>
                      <span>PM2.5</span>
                      <strong>
                        {formatValue(
                          airQuality?.pm2_5,
                          " µg/m³"
                        )}
                      </strong>
                    </div>

                    <div>
                      <span>PM10</span>
                      <strong>
                        {formatValue(
                          airQuality?.pm10,
                          " µg/m³"
                        )}
                      </strong>
                    </div>

                    <div>
                      <span>O₃</span>
                      <strong>
                        {formatValue(
                          airQuality?.ozone,
                          " µg/m³"
                        )}
                      </strong>
                    </div>

                    <div>
                      <span>NO₂</span>
                      <strong>
                        {formatValue(
                          airQuality?.nitrogen_dioxide,
                          " µg/m³"
                        )}
                      </strong>
                    </div>

                  </div>
                </>
              )}

            </section>

          </div>

          {/* ALERTS */}

          <section className="alert-card">

            <div>
              <h2>Environmental Alerts</h2>
              <p>No active alerts in your area.</p>
            </div>
          <button
            className="text-button alerts-button"
            onClick={() => setAlertsOpen(true)}
          >
            View all alerts →
          </button>

          </section>

          {/* ASK AIRA */}

          <button
            className="ask-aira"
            onClick={() => setAskAiraOpen(true)}
          >
           <img
             src="/aira-logo.png"
             alt="AIRA"
             className="ask-aira-logo"
          />
          <span>Ask AIRA</span>
          </button>
          
          {alertsOpen && (
            <section className="alerts-panel">
              <div className="alerts-panel-header">
                <div>
                  <h2>Environmental Alerts</h2>
                  <p>Alerts for your selected area.</p>
              </div>

              <button
                className="alerts-close"
                onClick={() => setAlertsOpen(false)}
              >
                ×
              </button>
            </div>

            <div className="alerts-empty">
              <strong>No active alerts</strong>
              <p>There are currently no environmental alerts in your area.</p>
            </div>
           </section>
          )}
          </main>
      )}

      {/* ================= COMMAND CENTER ================= */}

      {mode === "government" && (
        <main className="command-page">

          <div className="command-heading">

            <div>
              <h2>Command Center</h2>
              <p>
                Environmental monitoring, risk analysis and
                decision support
              </p>
            </div>

            <div className="updated-box">
              <span>Last updated</span>
              <strong>Current session</strong>
            </div>

          </div>

          {/* TABS */}

          <nav className="command-tabs">

            {[
              "Overview",
              "Risk Map",
              "Hotspots",
              "Incidents",
              "Forecast",
              "Historical Data",
              "AI Insights",
            ].map((tab) => (
              <button
                key={tab}
                className={activeTab === tab ? "active" : ""}
                onClick={() => setActiveTab(tab)}
              >
                {tab}
              </button>
            ))}

          </nav>

          {/* OVERVIEW */}

          {activeTab === "Overview" && (
          <>

              <div className="command-top-grid">

                {/* AIR QUALITY */}

                <section className="command-card">

                  <div className="card-title">
                    <h3>Air Quality</h3>
                    <span className="source-label">
                      Open-Meteo
                    </span>
                  </div>

                  {airLoading ? (
                    <p className="state-message">
                      Loading...
                    </p>
                  ) : airError ? (
                    <p className="state-message error">
                      Data unavailable
                    </p>
                  ) : (
                    <>
                      <div className="command-primary">
                        {airQuality?.us_aqi ?? "--"}
                      </div>

                      <p>AQI (US)</p>

                      <div className="aq-metrics">

                        <div>
                          <span>PM2.5</span>
                          <strong>
                            {formatValue(
                              airQuality?.pm2_5
                            )}
                          </strong>
                          <small>µg/m³</small>
                        </div>

                        <div>
                          <span>PM10</span>
                          <strong>
                            {formatValue(
                              airQuality?.pm10
                            )}
                          </strong>
                          <small>µg/m³</small>
                        </div>

                        <div>
                          <span>O₃</span>
                          <strong>
                            {formatValue(
                              airQuality?.ozone
                            )}
                          </strong>
                          <small>µg/m³</small>
                        </div>

                        <div>
                          <span>NO₂</span>
                          <strong>
                            {formatValue(
                              airQuality?.nitrogen_dioxide
                            )}
                          </strong>
                          <small>µg/m³</small>
                        </div>

                      </div>
                    </>
                  )}

                </section>

                {/* WEATHER */}

                <section className="command-card">

                  <div className="card-title">
                    <h3>Weather</h3>
                    <span className="source-label">
                      Open-Meteo
                    </span>
                  </div>

                  {weatherLoading ? (
                    <p className="state-message">
                      Loading...
                    </p>
                  ) : weatherError ? (
                    <p className="state-message error">
                      Data unavailable
                    </p>
                  ) : (
                    <>
                      <div className="command-primary">
                        {formatValue(
                          weather?.temperature_2m,
                          "°C"
                        )}
                      </div>

                      <p>Current local conditions</p>

                      <div className="weather-metrics">

                        <div>
                          <span>Humidity</span>
                          <strong>
                            {formatValue(
                              weather?.relative_humidity_2m,
                              "%"
                            )}
                          </strong>
                        </div>

                        <div>
                          <span>Wind Speed</span>
                          <strong>
                            {formatValue(
                              weather?.wind_speed_10m,
                              " km/h"
                            )}
                          </strong>
                        </div>

                        <div>
                          <span>Pressure</span>
                          <strong>
                            {formatValue(
                              weather?.surface_pressure,
                              " hPa"
                            )}
                          </strong>
                        </div>

                      </div>
                    </>
                  )}

                </section>

              </div>

              {/* RISK MAP */}

              <section className="map-card">

                <div className="map-header">
                  <div>
                    <h3>Risk Map</h3>
                    <p>
                      Environmental risk overview for the region
                    </p>
                  </div>

                  <span>Interactive Regional Map</span>
                </div>

                <div className="risk-map">
                  <MapContainer
                    center={[25.5788, 91.8933]}
                    zoom={11}
                    scrollWheelZoom={false}
                    className="risk-map"
                  >
                   {mapView === "map" ? (
                     <TileLayer
                       attribution="&copy; OpenStreetMap contributors"
                       url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                     />
                   ) : (
                     <TileLayer
                       attribution="Tiles &copy; Esri"
                       url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
                     />
                   )}
                  
                   {mapLayer === "air" && airQuality?.us_aqi != null && (
                     <CircleMarker
                       center={[25.5788, 91.8933]}
                       radius={10}
                       pathOptions={{
                         color: "#176b5b",
                         fillColor: "#176b5b",
                         fillOpacity: 0.8,
                       }}
                     >
                       <Popup>
                         <strong>Shillong Air Quality</strong>
                         <br />
                          AQI (US): {airQuality.us_aqi}
                       </Popup>
                     </CircleMarker>
                   )}
                   {mapLayer === "risk" && airQuality?.us_aqi != null && (
                     <CircleMarker
                       center={[25.5788, 91.8933]}
                       radius={14}
                       pathOptions={{
                         color: "#176b5b",
                         fillColor: "#176b5b",
                         fillOpacity: 0.25,
                       }}
                    >
                       <Popup>
                         <strong>Environmental Risk</strong>
                         <br />
                         Based on current AQI: {airQuality.us_aqi}
                         <br />
                         Assessment: {getRisk()}
                      </Popup>
                    </CircleMarker>
                   )}
                   
                </MapContainer>
                <div className="map-controls">
                  <div className="map-view-toggle">
                    <button
                      className={`map-view ${mapView === "map" ? "active" : ""}`}
                      onClick={() => setMapView("map")}
                    >
                      Map View
                    </button>

                    <button
                      className={`map-view ${mapView === "satellite" ? "active" : ""}`}
                      onClick={() => setMapView("satellite")}
                    >
                      Satellite
                    </button>
                  </div>
                  <div className="map-controls-title">MAP LAYERS</div>
                  <button
                    className={`map-layer ${mapLayer === "air" ? "active" : ""}`}
                    onClick={() => setMapLayer("air")}
                  >
                    Air Quality
                </button>

                <button
                  className={`map-layer ${mapLayer === "fire" ? "active" : ""}`}
                  onClick={() => setMapLayer("fire")}
                >
                   Fire Detection
                </button>

                <button
                  className={`map-layer ${mapLayer === "risk" ? "active" : ""}`}
                  onClick={() => setMapLayer("risk")}
                >
                  Environmental Risk
                </button>
                </div>
                <div className="map-legend">
                  <div className="map-legend-title">RISK LEVEL</div>

                  <div className="legend-item">
                    <span className="legend-dot low"></span>
                    <span>Low Risk</span>
                </div>

                  <div className="legend-item">
                    <span className="legend-dot moderate"></span>
                    <span>Moderate Risk</span>
                </div>

                  <div className="legend-item">
                    <span className="legend-dot high"></span>
                    <span>High Risk</span>
                </div>

                  <div className="legend-item">
                    <span className="legend-dot fire"></span>
                    <span>Active Fire</span>
                </div>
              </div>

                </div>
              </section>

              {/* BOTTOM CARDS */}

              <div className="command-bottom-grid">

                <section className="command-card">

                  <div className="card-title">
                    <h3>Fire Detection</h3>
                    <span className="source-label">
                      NASA FIRMS
                    </span>
                  </div>

                  <div className="empty-value">
                    --
                  </div>

                  <p>
                    Fire detection data is not currently
                    available.
                  </p>

                </section>

                <section className="command-card risk-assessment">

                  <div className="card-title">
                    <h3>Overall Environmental Risk</h3>
                  </div>

                  <div className="risk-value">
                    {getRisk()}
                  </div>

                  <p>
                    Assessment based on available environmental
                    measurements.
                  </p>

                </section>

              </div>

            </>
          )}

          {/* OTHER COMMAND CENTER SECTIONS */}
          {activeTab === "Hotspots" && (
            <section className="data-section">
              <div className="data-section-header">
                <div>
                  <h3>Environmental Hotspots</h3>
                  <p>
                    Areas requiring attention based on verified environmental data.
                  </p>
                </div>

                <span className="data-source">AIRA data sources</span>
              </div>

              <div className="empty-state">
               <h4>No hotspot data available</h4>
               <p>
                 Verified hotspot information will appear here when the
                 corresponding environmental data source is available.
               </p>
             </div>
           </section>
          )}
          {activeTab === "Forecast" && (
            <section className="data-section">
              <div className="data-section-header">
                <div>
                  <h3>Environmental Forecast</h3>
                  <p>
                    Forecast information based on verified environmental data.
                  </p>
                </div>

                <span className="data-source">Verified sources only</span>
              </div>

              <div className="empty-state">
                <h4>Forecast data unavailable</h4>
                <p>
                  Forecast information will appear here when the required
                  environmental forecast data is available.
                </p>
              </div>
            </section>
          )}
         {activeTab === "Historical Data" && (
           <section className="data-section">
             <div className="data-section-header">
               <div>
                 <h3>Historical Environmental Data</h3>
                 <p>
                   Historical environmental measurements from verified data sources.
                 </p>
               </div>

               <span className="data-source">Verified sources only</span>
             </div>

             <div className="empty-state">
               <h4>No historical data available</h4>
               <p>
                 Historical measurements will appear here when the required
                 environmental data is available.
               </p>
             </div>
          </section>
         )}
         {activeTab === "AI Insights" && (
           <section className="data-section">
             <div className="data-section-header">
               <div>
                 <h3>AI Environmental Insights</h3>
                 <p>
                   Evidence-based environmental insights generated from AIRA data.
                 </p>
               </div>

               <span className="data-source">AIRA context required</span>
             </div>

             <div className="empty-state">
               <h4>AI insights unavailable</h4>
               <p>
                 AI insights will appear here when verified environmental data
                 and the required AIRA analysis service are available.
               </p>
             </div>
          </section>
         )}
         {activeTab === "Incidents" && (
            <section className="data-section">
              <div className="data-section-header">
                <div>
                  <h3>Environmental Incidents</h3>
                  <p>
                    Verified environmental incidents detected through AIRA data sources.
                 </p>
               </div>

               <span className="data-source">Verified sources only</span>
              </div>

              <div className="empty-state">
                <h4>No incidents available</h4>
                <p>
                  Incident records will appear here when verified event data
                  is available from the connected environmental sources.
                </p>
              </div>
            </section>
          )}

          {activeTab !== "Overview" &&
           activeTab !== "Hotspots" &&
           activeTab !== "Incidents" &&
           activeTab !== "Forecast" && 
           activeTab !== "Historical Data" &&
           activeTab !== "AI Insights" &&
           (
            <section className="section-placeholder">
              <h3>{activeTab}</h3>
              <p>
                This section will use verified AIRA data
                sources when the corresponding backend
                integration is available.
              </p>
            </section>
          )}

        </main>
      )}

      {/* AIRA */}
      {mode === "government" && (
        <button
          className="ask-gemini"
          onClick={() => setAskAiraOpen(true)}
        >
          <img
            src="/aira-logo.png"
            alt="AIRA"
            className="ask-aira-logo"
         />
         <span>Ask AIRA</span>
        </button>
      )}
      {askAiraOpen && (
        <div className="aira-chat-panel">
          <div className="aira-chat-header">
            <div>
              <strong>Ask AIRA</strong>
              <span>Environmental assistant</span>
            </div>

            <button
              className="aira-close"
              onClick={() => setAskAiraOpen(false)}
            >
              ×
            </button>
          </div>

          <div className="aira-chat-messages">
            {airaMessages.length === 0 && (
              <div className="aira-welcome">
                <strong>How can I help?</strong>
                <p>
                  Ask about the current air quality, weather or
                  environmental risk in the selected area.
                </p>
              </div>
          )}

          {airaMessages.map((message, index) => (
            <div
              key={index}
              className={`aira-message ${message.type}`}
           >
             {message.text}
          </div>
        ))}
      </div>

      <div className="aira-chat-input">
        <input
          type="text"
          value={airaQuestion}
          onChange={(e) => setAiraQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleAskAira();
            }
          }}
          placeholder="Ask about your environment..."
       />

      <button onClick={handleAskAira}>
        Ask
      </button>
    </div>
  </div>
)}
</div>
);
}
   
export default App;

