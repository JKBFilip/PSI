import asyncio
import aiohttp

async def fetch_weather():
    latitude = 49.2992
    longitude = 19.9496
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise Exception(f'Error fetching weather data: {response.status}')


async def get_weather_forecast():
    weather_data = await fetch_weather()
    hourly_data = weather_data.get('hourly', {})
    temperatures = hourly_data.get('temperature_2m', [])
    wind_speeds = hourly_data.get('wind_speed_10m', [])


    if temperatures and wind_speeds:
        return {
            'temperature': temperatures[0],
            'wind_speed': wind_speeds[0]
        }
    return None


def main():
    loop = asyncio.get_event_loop()
    forecast = loop.run_until_complete(get_weather_forecast())
    if forecast:
        print(f"Temperatura: {forecast['temperature']} °C")
        print(f"Prędkość wiatru: {forecast['wind_speed']} m/s")
    else:
        print("Brak danych prognozy pogody.")


if __name__ == '__main__':
    main()
