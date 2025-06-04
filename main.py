import requests

API_KEY = "YOUR_API_KEY_HERE"  # Replace with your OpenWeatherMap API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if response.status_code != 200:
            print(f"Error: {data.get('message', 'Unable to fetch weather.')}")
            return

        weather = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        city_name = data["name"]
        country = data["sys"]["country"]

        print(f"\nWeather for {city_name}, {country}:")
        print(f"  Description : {weather}")
        print(f"  Temperature : {temp}°C")
        print(f"  Feels Like  : {feels_like}°C")
        print(f"  Humidity    : {humidity}%")
        print(f"  Wind Speed  : {wind_speed} m/s\n")

    except Exception as e:
        print("Error:", e)

def main():
    print("=== Simple Weather CLI App ===")
    print("Type 'exit' to quit.\n")
    while True:
        city = input("Enter city name: ").strip()
        if city.lower() == "exit":
            print("Goodbye!")
            break
        if not city:
            print("Please enter a valid city name.")
            continue
        get_weather(city)

if __name__ == "__main__":
    main()
