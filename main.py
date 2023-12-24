import imp
import json
from bs4 import BeautifulSoup
import datetime
from config import *
import aiohttp
import asyncio
from utils import *
import streamlit as st
from os import listdir
from os.path import isfile, join


async def get_page_data(session, page, total):
    url_page = url + f'&page={page}'
    async with session.get(url=url_page) as response:
        response_text = await response.text()

        core(response_text)
        st.write(f"[INFO] Обработал страницу {page}/{total}")


async def gather_data(st_url):
    async with aiohttp.ClientSession(headers=headers) as session:
        response = await session.get(url=st_url)
        soup = BeautifulSoup(await response.text(), "lxml")
        pages_count = int(soup.find("div", class_="pagination-numbers").find_all("a")[-1].text) # type: ignore

        tasks = []
        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_page_data(session=session, page=page, total=pages_count))
            tasks.append(task)

        await asyncio.gather(*tasks)

def main(url):
    asyncio.run(gather_data(url))
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f"data/labirint_{cur_time}_async.json", "w", encoding='utf-8') as file:
        json.dump(books_data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    url = st.text_input('Введите url')
    if "https://www.labirint.ru/" in url:
        st.button('Начать парсинг', on_click=main, args=(url,))
    else:
        st.write("Некорректный url адресс")

    names = [f for f in listdir('data') if isfile(join('data', f))]
    if names:
        for name in names:
            with open(f"data/{name}", "rb") as file:
                btn = st.download_button(
                        label=f"Download {name}",
                        data=file,
                        file_name=name,
                        mime="application/json"
                    )
