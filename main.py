import requests
import sys
from colorama import init, Fore, Style

init(autoreset=True)

API_KEY = "YOUR_API_KEY_HERE"  # Replace with your OpenWeatherMap API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

units = "metric"  # Default: Celsius


def get_weather(city, units):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": units
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()

        if response.status_code == 401:
            print(Fore.RED + "Error: Unauthorized. Check your API key.")
            return None
        elif response.status_code == 404:
            print(Fore.YELLOW + f"Error: City '{city}' not found.")
            return None
        elif response.status_code != 200:
            print(Fore.RED + f"Error: {data.get('message', 'Unable to fetch weather.')}")
            return None

        weather = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        city_name = data["name"]
        country = data["sys"]["country"]
        icon_code = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"

        return {
            "city_name": city_name,
            "country": country,
            "weather": weather,
            "temp": temp,
            "feels_like": feels_like,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "icon_url": icon_url
        }

    except requests.exceptions.Timeout:
        print(Fore.RED + "Error: Request timed out. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error: Network problem occurred: {e}")
        return None


def print_weather(data, units):
    if data is None:
        return

    unit_symbol = "°C" if units == "metric" else "°F"
    print(Fore.CYAN + Style.BRIGHT + f"\nWeather for {data['city_name']}, {data['country']}:\n" + Style.RESET_ALL)
    print(Fore.GREEN + f"  Description : {data['weather']}")
    print(Fore.YELLOW + f"  Temperature : {data['temp']}{unit_symbol}")
    print(Fore.YELLOW + f"  Feels Like  : {data['feels_like']}{unit_symbol}")
    print(Fore.BLUE + f"  Humidity    : {data['humidity']}%")
    print(Fore.MAGENTA + f"  Wind Speed  : {data['wind_speed']} m/s")
    print(Fore.CYAN + f"  Icon        : {data['icon_url']}\n")


def print_banner():
    print(Fore.CYAN + Style.BRIGHT + "=" * 40)
    print(Fore.CYAN + Style.BRIGHT + "      Simple Weather CLI App      ")
    print(Fore.CYAN + Style.BRIGHT + "=" * 40)
    print(Fore.WHITE + "Type 'exit' to quit.")
    print(Fore.WHITE + "Type 'units' to toggle Celsius/Fahrenheit.\n")


def main():
    global units

    if API_KEY == "YOUR_API_KEY_HERE":
        print(Fore.RED + "Warning: Please replace 'YOUR_API_KEY_HERE' with your actual OpenWeatherMap API key.\n")

    print_banner()

    while True:
        city = input(Fore.WHITE + "Enter city name: ").strip()

        if city.lower() == "exit":
            print(Fore.CYAN + "Goodbye!")
            break

        if city.lower() == "units":
            units = "imperial" if units == "metric" else "metric"
            print(Fore.GREEN + f"Units switched to {'Fahrenheit' if units == 'imperial' else 'Celsius'}.\n")
            continue

        if not city:
            print(Fore.YELLOW + "Please enter a valid city name.\n")
            continue

        weather_data = get_weather(city, units)
        print_weather(weather_data, units)


if __name__ == "__main__":
    main()
