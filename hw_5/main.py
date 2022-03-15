import argparse
import asyncio
import os

import aiofiles
import aiohttp


async def download_image(url, session, file_name):
    async with session.get(url) as response:
        async with aiofiles.open(file_name, mode='wb') as f:
            await f.write(await response.read())


async def download_images(urls, path_to_dir):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[
            loop.create_task(
                download_image(urls[i], session, f"{path_to_dir}/person{i}.jpg")
            ) for i in range(len(urls))
        ])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('num_of_images', type=int)
    parser.add_argument('path_to_dir')
    args = parser.parse_args()

    if not os.path.exists(args.path_to_dir):
        os.makedirs(args.path_to_dir)
    urls = ["https://picsum.photos/800"] * args.num_of_images
    loop = asyncio.get_event_loop()
    tasks = loop.create_task(download_images(urls, args.path_to_dir))
    loop.run_until_complete(tasks)
    loop.close()
