# Django Weather Project

## Description

This project is a Django-based web application that provides weather forecasts. Users can enter a city name, and the application displays the weather forecast for the next three days using data from the WeatherAPI.

## Features

- Fetch and display weather forecasts for a specified city.
- Show forecasts for the next three days, excluding the current day.
- Use of Django's ORM for database operations.

## Setup and Installation

To set up this project on your local machine, follow these steps:

1. Clone the Repository

```
git clone https://github.com/Spikyd/weatherApp.git
cd weatherApp
```

2. Create and Activate a Virtual Environment (Optional but recommended)

- On Windows:
  ```
  python -m venv venv
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  python3 -m venv venv
  source venv/bin/activate
  ```

3. Install Required Packages

```
pip install -r requirements.txt
```

4. Environment Variables
   Create a `.env` file in the project root directory and add your WeatherAPI key:

```
WEATHER_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

5. Run Migrations

```
python manage.py migrate
```

6. Run the Development Server

```
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.
