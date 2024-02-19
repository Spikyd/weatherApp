import requests
import logging

from django.shortcuts import render
from .models import Forecast
from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from django.utils.text import slugify

logger = logging.getLogger(__name__)


def get_weather_data(city):
    safe_city = slugify(city)
    cache_key = f"weather_data_{safe_city}"
    cached_data = cache.get(cache_key)
    if cached_data:
        logger.debug("Cached data found for city: %s", city)
        return cached_data

    try:
        api_key = settings.WEATHER_API_KEY
        base_url = "http://api.weatherapi.com/v1/forecast.json"
        params = {"key": api_key, "q": city, "days": 4}

        response = requests.get(base_url, params=params)
        if response.status_code == 400:
            error_msg = f"The city name '{city}' is not recognized. Please enter a valid city name."
            logger.error(error_msg)
            raise Exception(error_msg)
        response.raise_for_status()
        weather_data = response.json()
        cache.set(cache_key, weather_data, timeout=3600)
        logger.debug("Weather data fetched and cached for city: %s", city)
        return weather_data
    except requests.RequestException as e:
        logger.exception("Error fetching data from WeatherAPI for city: %s", city)
        raise Exception("Error fetching data from WeatherAPI.")


def update_or_create_forecast(city, forecast_data):
    next_three_days_forecast = forecast_data["forecast"]["forecastday"][1:4] = (
        forecast_data["forecast"]["forecastday"][1:4]
    )
    logger.debug(
        "Processing forecast for next three days: %s", next_three_days_forecast
    )

    for daily_forecast in next_three_days_forecast:
        date = datetime.strptime(daily_forecast["date"], "%Y-%m-%d").date()
        sunrise = format_time(daily_forecast["astro"]["sunrise"])
        sunset = format_time(daily_forecast["astro"]["sunset"])
        condition = daily_forecast["day"]["condition"]["text"]
        humidity = daily_forecast["day"]["avghumidity"]
        uv = daily_forecast["day"]["uv"]
        wind_speed = daily_forecast["day"]["maxwind_kph"]

        Forecast.objects.update_or_create(
            date=date,
            city=city,
            defaults={
                "max_temp": daily_forecast["day"]["maxtemp_c"],
                "min_temp": daily_forecast["day"]["mintemp_c"],
                "total_precip": daily_forecast["day"]["totalprecip_mm"],
                "sunrise": sunrise,
                "sunset": sunset,
                "condition": condition,
                "humidity": humidity,
                "uv": uv,
                "wind_speed": wind_speed,
            },
        )


def format_time(time_str):
    """Converts 12-hour time format to 24-hour format."""
    return datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")


def index(request):
    error_message = None
    forecasts = []
    if request.method == "POST":
        city = request.POST.get("city")
        try:
            weather_data = get_weather_data(city)
            if not weather_data.get("forecast", {}).get("forecastday"):
                error_msg = f"No forecast data found for '{city}'."
                logger.error(error_msg)
                raise Exception(error_msg)

            update_or_create_forecast(city, weather_data)
            forecasts = Forecast.objects.filter(city=city).order_by("date")
            logger.debug("Forecasts prepared for template rendering for city: %s", city)
        except Exception as e:
            logger.error("Error in index view: %s", e)
            error_message = str(e)

    return render(
        request, "index.html", {"forecasts": forecasts, "error_message": error_message}
    )
