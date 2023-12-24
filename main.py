import json
from bs4 import BeautifulSoup
import datetime
from config import *
import aiohttp
import asyncio
from utils import *

async def get_page_data(session, page):
    url_page = url + f'&page={page}'
    async with session.get(url=url_page) as response:
        response_text = await response.text()

        core(response_text)
        print(f"[INFO] Обработал страницу {page}")


async def gather_data():
    async with aiohttp.ClientSession(headers=headers) as session:
        response = await session.get(url=url)
        soup = BeautifulSoup(await response.text(encoding='utf-8'), "lxml")
        pages_count = int(soup.find("div", class_="pagination-numbers").find_all("a")[-1].text)

        tasks = []
        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_page_data(session=session, page=page))
            tasks.append(task)

        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(gather_data())

    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    with open(f"labirint_{cur_time}_async.json", "w", encoding='utf-8') as file:
        json.dump(books_data, file, indent=4, ensure_ascii=False)
