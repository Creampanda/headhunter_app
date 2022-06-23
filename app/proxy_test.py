from datetime import datetime
import requests
import datetime
import aiohttp
import asyncio
from random import choice


start = datetime.datetime.now()


all_data = []
working_proxies = []


async def check_proxy(session, i) -> str:
    proxy_London = "http://178.62.72.48:3128"
    proxy_Frank_with_auth = "http://apollo:admin@178.128.194.202:3128"
    # proxy_auth = aiohttp.BasicAuth("apollo", "admin")
    async with session.get(
        "https://httpbin.org/ip", proxy=proxy_Frank_with_auth
    ) as resp:
        print(i, " отправлен")
        resp_text = await resp.text()
        print(resp_text)
        # working_proxies.append(resp_text)
        return resp_text


async def get_working_proxy_async():
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(limit=64, ssl=False), trust_env=True
    ) as session:
        tasks = []
        for i in range(3):
            task = asyncio.create_task(check_proxy(session, i))
            tasks.append(task)
            # process text and do whatever we need...
        await asyncio.gather(*tasks)


APIKEY = "bab708209719c10b8d804ba0add727b2"
asyncio.run(get_working_proxy_async())

print(datetime.datetime.now() - start)
print(working_proxies)
