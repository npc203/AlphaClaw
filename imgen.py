import aiofiles, aiohttp, asyncio
import json

with open("nft_grab.json", "r") as f:
    data = json.load(f)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def fetch(session, url, path, price):
    async with session.get(url) as resp:
        if resp.status == 200:
            async with aiofiles.open(path + f"{price}_" + url.split("/")[-1], mode="wb") as f:
                await f.write(await resp.read())
                await f.close()
        else:
            print(f"BROKE:{resp.status}\n{url}")
        print("Done:", url)


async def download(image_urls: list, path):
    tasks = []
    headers = {
        "user-agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        for url, price in image_urls:
            tasks.append(fetch(session, url, path, max(price)))
        await asyncio.gather(*tasks)


async def main_gql():
    for thing in data["gql"]:
        image_urls = []
        path = f"tmp/{thing}/"
        async with aiofiles.open(path + "index.json", mode="r") as f:
            x = json.loads(await f.read())["nfts"]
            for i in x:
                image_urls.append(
                    (
                        data["gql"][thing]["img"].format(
                            uri_id=int(i["uri"].split("/")[-1]), contract_hash=i["contract"]["id"]
                        ),
                        [*map(lambda x: x["amount"], i["sales"])] or [0],
                    )
                )
            await download(image_urls, path)


async def main_rest():
    for thing in data["rest"]:
        pass


loop = asyncio.get_event_loop()
loop.run_until_complete(main_gql())
loop.run_until_complete(main_rest())
loop.close()
