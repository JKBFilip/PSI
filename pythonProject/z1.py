import aiohttp
import asyncio

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    url = "http://wmii.uwm.edu.pl/"
    content = await fetch_url(url)
    print(content)

if __name__ == "__main__":
    asyncio.run(main())
