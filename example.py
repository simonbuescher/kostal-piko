import asyncio

import aiohttp

from pikoapi import Piko


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_infos(loop))


async def fetch_infos(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        piko = Piko(session, "http://192.168.0.50")
        infos = await piko.get_data()

        for info, value in infos:
            print(f"{info.key}: {value} {info.unit}")


if __name__ == "__main__":
    main()
