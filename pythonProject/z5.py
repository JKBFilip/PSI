import asyncio
import aiohttp


async def fetch_weather(latitude, longitude):
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,wind_speed_10m'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise Exception(f'Error fetching weather data: {response.status}')


async def get_weather_forecast(city_coordinates):
    tasks = []
    for city, (latitude, longitude) in city_coordinates.items():
        tasks.append(fetch_weather(latitude, longitude))

    results = await asyncio.gather(*tasks)

    weather_forecast = {}
    for i, city in enumerate(city_coordinates.keys()):
        hourly_data = results[i].get('hourly', {})
        temperatures = hourly_data.get('temperature_2m', [])
        wind_speeds = hourly_data.get('wind_speed_10m', [])

        if temperatures and wind_speeds:
            weather_forecast[city] = {
                'temperature': temperatures[0],
                'wind_speed': wind_speeds[0]
            }

    return weather_forecast


def main():
    city_coordinates = {
        'Porlamar': (10.95, -63.85),
        'Moroni': (-11.70, 43.24),
        'Helsinki': (60.1695, 24.9354)
    }

    loop = asyncio.get_event_loop()
    forecast = loop.run_until_complete(get_weather_forecast(city_coordinates))

    for city, data in forecast.items():
        print(f"{city}: Temperatura: {data['temperature']} °C, Prędkość wiatru: {data['wind_speed']} m/s")


if __name__ == '__main__':
    main()
