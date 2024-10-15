import aiohttp
import asyncio

async def download_file(url, save_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(save_path, 'wb') as f:
                    f.write(await response.read())
                print(f"Plik zapisano jako: {save_path}")
            else:
                print(f"Błąd pobierania pliku: {response.status}")

def main(url, save_path):
    asyncio.run(download_file(url, save_path))

if __name__ == "__main__":
    url =
    save_path =
    main(url, save_path)
