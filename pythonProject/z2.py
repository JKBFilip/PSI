import aiohttp
import asyncio

async def post_data(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
         return await response.json()


async def main():
    url = "https://jsonplaceholder.typicode.com/posts"
    data = {"name": "New User", "email": "newuser@example.com"}

    response = await post_data(url, data)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
