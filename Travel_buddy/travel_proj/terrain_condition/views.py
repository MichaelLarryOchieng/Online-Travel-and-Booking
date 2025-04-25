import requests
from django.http import JsonResponse
import numpy as np
from datetime import datetime, timedelta

WEATHER_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Slight or moderate thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

def get_terrain_condition_data(request):
    latitude_str = request.GET.get('latitude')
    longitude_str = request.GET.get('longitude')

    if not latitude_str or not longitude_str:
        return JsonResponse({"error": "Latitude and longitude are required."}, status=400)

    try:
        latitude = float(latitude_str)
        longitude = float(longitude_str)
    except ValueError:
        return JsonResponse({"error": "Invalid latitude or longitude."}, status=400)

    # --- Fetch Current Weather Data ---
    base_url_weather = "https://api.open-meteo.com/v1/forecast"
    params_weather = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "hourly": "temperature_2m,precipitation,weathercode",
        "timezone": "UTC"
    }
    weather_data = {}
    current_condition_description = "Error fetching weather"
    current_temperature = None
    current_windspeed = None
    current_weather_code = None
    try:
        response_weather = requests.get(base_url_weather, params=params_weather)
        response_weather.raise_for_status()
        weather_data = response_weather.json()
        current_weather = weather_data.get("current_weather", {})
        current_weather_code = current_weather.get("weathercode")
        current_condition_description = WEATHER_CODE_MAP.get(current_weather_code, "Unknown")
        current_temperature = current_weather.get("temperature")
        current_windspeed = current_weather.get("windspeed")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching current weather data: {e}")

    # --- Fetch Elevation Data for a 3x3 Grid ---
    base_url_elevation = "https://api.open-meteo.com/v1/elevation"
    latitudes = np.linspace(latitude - 0.02, latitude + 0.02, 3)
    longitudes = np.linspace(longitude - 0.02, longitude + 0.02, 3)
    coordinates = [(lat, lon) for lat in latitudes for lon in longitudes]

    elevation_data = []
    try:
        for coord in coordinates:
            params_elevation = {"latitude": coord[0], "longitude": coord[1]}
            response_elevation = requests.get(base_url_elevation, params=params_elevation)
            response_elevation.raise_for_status()
            elevation_response = response_elevation.json()
            if "elevation" in elevation_response and len(elevation_response["elevation"]) > 0:
                elevation_data.append(elevation_response["elevation"][0])
            else:
                elevation_data.append(None)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching elevation data: {e}")
        elevation_data = [None] * 9

    elevation_grid = np.array(elevation_data).reshape((3, 3))

    # --- Calculate Basic Slope ---
    dominant_slope = "Slope data unavailable"
    if elevation_grid.shape == (3, 3) and np.all(np.logical_not(np.isnan(elevation_grid))):
        dy_dx = np.gradient(elevation_grid, 0.02)
        slope_magnitude = np.sqrt(dy_dx[0]**2 + dy_dx[1]**2)
        average_slope_percent = np.nanmean(slope_magnitude) * 100
        if average_slope_percent <= 5:
            dominant_slope = "Generally flat/gentle"
        elif 5 < average_slope_percent <= 15:
            dominant_slope = "Moderate slope"
        elif 15 < average_slope_percent <= 30:
            dominant_slope = "Steep slope"
        elif average_slope_percent > 30:
            dominant_slope = "Very steep slope"

    # --- Fetch Historical Weather Data (Last 3 Days - Precipitation) ---
    historical_precipitation = None
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    base_url_history = "https://archive-api.open-meteo.com/v1/archive"
    params_history = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "precipitation_sum",
        "timezone": "UTC"
    }
    try:
        response_history = requests.get(base_url_history, params=params_history)
        response_history.raise_for_status()
        history_data = response_history.json()
        if "hourly" in history_data and "precipitation_sum" in history_data["hourly"]:
            historical_precipitation = sum(filter(None, history_data["hourly"]["precipitation_sum"])) # Sum of non-null precipitation
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical weather data: {e}")

    # --- Categorize Weather for Surface Conditions (with Historical Context) ---
    surface_condition = "Surface conditions uncertain based on weather"
    if current_condition_description:
        if any(keyword in current_condition_description.lower() for keyword in ["rain", "drizzle", "showers"]):
            if dominant_slope and "flat" in dominant_slope.lower():
                surface_condition = "Likely muddy or very slippery surface"
            else:
                surface_condition = "Wet and potentially slippery surface"
        elif any(keyword in current_condition_description.lower() for keyword in ["snow", "grains"]):
            surface_condition = "Snow-covered surface, reduced traction"
        elif "fog" in current_condition_description.lower():
            surface_condition = "Foggy, may have damp or slippery patches"
        elif current_temperature is not None and current_temperature <= 0:
            surface_condition = "Potential for icy surface conditions"
            if historical_precipitation is not None and historical_precipitation > 2: # Consider recent precipitation for ice
                surface_condition += " (especially if recent precipitation)"
        elif "overcast" in current_condition_description.lower():
            if historical_precipitation is not None and historical_precipitation > 5: # Significant recent rain
                surface_condition = "Overcast after recent rain, likely damp or potentially muddy"
            else:
                surface_condition = "Overcast, surface dryness depends on very recent conditions"
        elif any(keyword in current_condition_description.lower() for keyword in ["clear", "partly cloudy", "mainly clear"]):
            if historical_precipitation is not None and historical_precipitation > 10: # Significant recent rain even with clear skies
                surface_condition = "Generally dry, but may have lingering dampness from recent rain"
            else:
                surface_condition = "Generally dry surface expected"

    overall_terrain_assessment = f"Dominant slope: {dominant_slope}, Surface: {surface_condition}"

    response_data = {
        "current_condition": current_condition_description,
        "temperature": current_temperature,
        "windspeed": current_windspeed,
        "elevation": weather_data.get("elevation"),
        "dominant_slope": dominant_slope,
        "terrain_assessment": overall_terrain_assessment,
        "latitude": weather_data.get("latitude"),
        "longitude": weather_data.get("longitude"),
        "timezone": weather_data.get("timezone"),
        "hourly_forecast": weather_data.get("hourly"),
        "historical_precipitation": historical_precipitation
    }

    return JsonResponse(response_data)