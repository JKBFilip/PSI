import asyncio
import aiohttp

urls = [
    'http://wmii.uwm.edu.pl/',
    'https://httpbin.org/get',
    'https://jsonplaceholder.typicode.com/posts',
    'https://www.wikipedia.org',
    'https://www.python.org'
]


async def fetch(session, url):
    async with session.get(url) as response:

        return await response.text(encoding='utf-8')

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

def main():
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(fetch_all(urls))
    for i, content in enumerate(results):
        print(f"Treść strony {urls[i]}:\n{content}...\n")

if __name__ == '__main__':
    main()