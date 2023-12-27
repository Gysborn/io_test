import re
from bs4 import BeautifulSoup
from config import *
import datetime
import json
import csv
import pandas as pd
from openpyxl.workbook import Workbook


def core(soup_obj):
    soup = BeautifulSoup(soup_obj, "lxml")
    books_items = soup.find_all("div", class_="genres-carousel__item")
    if not books_items:
        return None

    for book in books_items:
        book_data = book.next.next
        try:
            price = book_data.find_next("div", class_="price")  # скидка
        except:
            discount_percent = 'Скидка не предусмотрена'
        else:
            discount_percent = price.next.next.get("title", None)
        title = book_data.get("data-name", None)
        genre = book_data.get("data-maingenre-name", None)
        publisher = book_data.get("data-pubhouse", None)
        series = book_data.get("data-series", "Нет")
        publisher += f" серия: {series}"
        new_price = book_data.get("data-discount-price", None)
        old_price = book_data.get("data-price", None)
        link = "https://www.labirint.ru" + book_data.find("a", class_="product-title-link").get("href", None)
        try:
            book_authors = book.find_next("div", class_="product-author").find_all('a')  # авторы
        except:
            book_authors = "Автор не указан"
        else:
            book_authors = ', '.join([author.get("title", None) for author in book_authors])

        books_data.append(
            {
            "book_title": title,
            "book_genre": genre,
            "book_authors": book_authors,
            "book_publishing": publisher,
            "book_new_price": new_price,
            "book_old_price": old_price,
            "book_sale": discount_percent,
            "book_link": link
          }
        )

def writer_csv():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    path = f"labirint_{cur_time}_.csv"

    with open(f"data/{path}", "w") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Название книги",
                "Жанр"
                "Автор",
                "Издательство",
                "Цена со скидкой",
                "Цена без скидки",
                "Процент скидки",
                "Ссылка"
            )
        )

    for book in books_data:
        with open(f"data/{path}", "a") as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                    book["book_title"],
                    book["book_genre"],
                    book["book_authors"],
                    book["book_publishing"],
                    book["book_new_price"],
                    book["book_old_price"],
                    book["book_sale"],
                    book["book_link"]
                )
            )

    return path

def writer_json():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    path = f"labirint_{cur_time}_.json"

    with open(f"data/{path}", "w", encoding='utf-8') as file:
        json.dump(books_data, file, indent=4, ensure_ascii=False)
    return path


def writer_excel():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    path = f"labirint_{cur_time}_.xlsx"
    path_js = writer_json()
    pd.read_json(f"data/{path_js}").to_excel(f"data/{path}")
    return path


# p = 'labirint_25_12_2023_22_03_.json'

# pd.read_json(f"data/{p}").to_excel("data/labirint.xlsx")
