import aiohttp
import asyncio

async def fetch(url: str, header: dict) -> str:
    async with aiohttp.ClientSession(headers=header) as session:
        async with session.get(url) as response:
            return await response.json()


async def main() -> None:
    url = "https://670bef0e7e5a228ec1cf1824.mockapi.io/api/v1/user"
    header = {"Token": "Bearer SOME_CHARS"}

    users = await fetch(url=url, header=header)

    print(users)


if __name__ == "__main__":
    asyncio.run(main())