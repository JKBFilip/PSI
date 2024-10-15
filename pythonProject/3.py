import aiohttp
import asyncio


async def add_user(url: str, header: dict, body: dict) -> str:
    async with aiohttp.ClientSession(headers=header) as session:
        async with session.post(url, data=body) as response:
            return await response.json()


async def main() -> None:
    url = "https://670bef0e7e5a228ec1cf1824.mockapi.io/api/v1/user"
    header = {"Token": "Bearer SOME_CHARS"}
    body = {
        "name": "Janusz Badziewiak",
        "avatar": "https://naukawpolsce.pl/sites/default/files/styles/strona_glowna_slider_750x420/public/202005/portretProboscis_monkey_%28Nasalis_larvatus%29_male_head_0.jpg.webp?itok=HXkRpCtR",
    }

    users = await add_user(url=url, header=header, body=body)

    print(users)


if __name__ == "__main__":
    asyncio.run(main())
