import UtilApiURLs from "../../_globals/UtilApiUrls.js";

document.addEventListener("DOMContentLoaded", function() {
    fetch(UtilApiURLs.GetRealTimeWeatherURL)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error fetching weather data:', data.error);
                return;
            }

            document.getElementById('location').innerText = data.location.name;
            document.getElementById('time').innerText = new Date().toLocaleTimeString();
            document.getElementById('temperature').innerText = `${data.temperature}°C`;
            document.getElementById('weather-condition').innerText = data.conditions;
            document.getElementById('wind-speed').innerText = `${data.windSpeed} km/h`;
            document.getElementById('humidity').innerText = `${data.humidity}%`;
            document.getElementById('sun-hours').innerText = `${data.sunHours} h`;
            document.getElementById('weather-icon').src = data.iconUrl;
        })
        .catch(error => console.error('Error:', error));
});