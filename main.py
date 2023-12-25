import imp
import json
import re
from bs4 import BeautifulSoup
import datetime
from config import *
import aiohttp
import asyncio
from utils import *
import streamlit as st
import os
from os import listdir
from os.path import isfile, join
import time

st.set_page_config(
    page_title='Parsing book store',
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    'Get Help': 'https://www.extremelycoolapp.com/help',
    'Report a bug': "https://www.extremelycoolapp.com/bug",
    'About': "# This is a header. This is an *extremely* cool app!"})

placeholder = st.empty()
# placeholder1 = st.empty()


def cs_sidebar():
    st.sidebar.header('Парсим www.labirint.ru/')
    output_file = st.sidebar.radio(
    "Choice output file",
    [":rainbow[.json]", ":rainbow[.csv]", ":rainbow[.excel]"],
    index=None,
    )

    st.write("*You selected*:", output_file)
    if output_file:
        return output_file
    else:
        return 'Файл не выбран'



async def get_page_data(session, page, total):
    url_page = url + f'&page={page}'
    async with session.get(url=url_page) as response:
        response_text = await response.text()

        core(response_text)
        # with st.empty():
        #     placeholder1.progress(page, 'Working ...')

        with st.empty():
            placeholder.info(f"Обрабатывается {page}/{total} ⏳", icon="ℹ️")


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

def display_file(path):
    with open(f"data/{path}", "rb") as file:
        st.sidebar.download_button(
                label=f"Download {path}",
                data=file,
                file_name=path,
                mime="application/json"
            )

def main(url, f):
    if not f:
        st.error('***Не выбран файл! Слева выберите в каком форамате вернуть данные***')
        return None
    asyncio.run(gather_data(url))

    if f == ':rainbow[.json]':
        display_file(writer_json())
        st.success("Success!")
        return None

    if f == ':rainbow[.csv]':
        display_file(writer_csv())
        st.success("Success!")
        return None

    if f == ':rainbow[.excel]':
        display_file(writer_excel())
        st.success("Success!")
        return None

    else:
        st.sidebar.error(f)


if __name__ == '__main__':
    f = cs_sidebar()
    if not os.path.isdir("data"):
        os.mkdir("data")

    url = st.text_input('Введите url')
    if "https://www.labirint.ru/" in url:
        st.button('Начать парсинг', on_click=main, args=(url, f,))
    else:
        st.button('Начать парсинг', disabled=True)
        st.error("Не корректный url адрес! На сайте магазина выберите нужную котегорию скопируйте и вставте в поле выше...")
