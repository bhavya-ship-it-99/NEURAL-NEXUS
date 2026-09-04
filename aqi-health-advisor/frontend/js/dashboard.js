async function loadDashboard() {
    const errorBox = document.querySelector("#dataError");

    try {
        await Aero.locate();

        const [weather, aqi, forecast] = await Promise.all([
            Aero.get(`/api/weather/?lat=${Aero.coords.lat}&lon=${Aero.coords.lon}`),
            Aero.get(`/api/aqi/?lat=${Aero.coords.lat}&lon=${Aero.coords.lon}`),
            Aero.get(`/api/forecast/?lat=${Aero.coords.lat}&lon=${Aero.coords.lon}`)
        ]);

        const setText = (selector, value) => {
            const element = document.querySelector(selector);
            if (element) {
                element.textContent = value;
            }
        };

        // AQI
        const aqiValue = Number(aqi.aqi);
        const [aqiState, aqiLabel] = Aero.aqiState(aqiValue);

        setText("#aqiNumber", Number.isFinite(aqiValue) ? aqiValue : "—");
        setText("#aqiNumber2", Number.isFinite(aqiValue) ? aqiValue : "—");
        setText("#station", aqi.station || "Nearest monitoring station");

        const aqiBadge = document.querySelector("#aqiBadge");

        if (aqiBadge) {
            aqiBadge.textContent = aqiLabel;
            aqiBadge.className = `status-badge ${aqiState}`;
        }

        // Weather
        setText(
            "#temp",
            weather.temperature != null
                ? `${weather.temperature}°C`
                : "—"
        );

        setText(
            "#humidity",
            weather.humidity != null
                ? `${weather.humidity}%`
                : "—"
        );

        setText(
            "#wind",
            weather.wind_speed != null
                ? `${weather.wind_speed} km/h`
                : "—"
        );

        setText(
            "#weatherText",
            Aero.weatherCode(weather.weather_code)
        );

        // Forecast
        const forecastContainer =
            document.querySelector("#forecastPreview");

        if (forecastContainer) {
            forecastContainer.innerHTML =
                (forecast.forecast || [])
                    .slice(0, 7)
                    .map((day, index) => {
                        const date =
                            new Date(`${day.date}T12:00:00`);

                        return `
                            <div class="forecast-day ${index === 0 ? "active" : ""}">
                                <div class="dow">
                                    ${date.toLocaleDateString("en-IN", {
                                        weekday: "short"
                                    })}
                                </div>

                                <div class="date">
                                    ${date.toLocaleDateString("en-IN", {
                                        day: "numeric",
                                        month: "short"
                                    })}
                                </div>

                                <div class="weather-symbol">
                                    ${Aero.weatherEmoji(day.weather_code)}
                                </div>

                                <div class="forecast-temp">
                                    ${Math.round(day.temp_max)}°
                                    <span class="muted">
                                        ${Math.round(day.temp_min)}°
                                    </span>
                                </div>

                                <div class="forecast-meta">
                                    <span>
                                        💨 ${Math.round(day.wind_speed_max)} km/h
                                    </span>

                                    <span>
                                        💧 ${Math.round(day.humidity_max)}%
                                    </span>
                                </div>
                            </div>
                        `;
                    })
                    .join("");
        }

        setText(
            "#lastUpdated",
            `Updated ${new Date().toLocaleTimeString("en-IN", {
                hour: "2-digit",
                minute: "2-digit"
            })}`
        );

        if (errorBox) {
            errorBox.textContent = "";
            errorBox.classList.add("hidden");
        }

    } catch (error) {
        console.error("Dashboard load failed:", error);

        if (errorBox) {
            errorBox.textContent =
                `Could not load dashboard data: ${error.message || error}`;
            errorBox.classList.remove("hidden");
        }
    }
}

document.addEventListener("DOMContentLoaded", loadDashboard);
