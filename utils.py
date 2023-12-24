from bs4 import BeautifulSoup
from config import *
import datetime
import json
import csv


def core(soup_obj):
    soup = BeautifulSoup(soup_obj, "lxml")
    books_items = soup.find_all("div", class_="genres-carousel__item")

    for book in books_items:
        book_data = book.next.next
        price = book_data.find_next("div", class_="price")  # скидка
        title = book_data.get("data-name", None)
        genre = book_data.get("data-maingenre-name", None)
        publisher = book_data.get("data-pubhouse", None)
        series = book_data.get("data-series", "Нет")
        publisher += f" серия: {series}"
        new_price = book_data.get("data-discount-price", None)
        old_price = book_data.get("data-price", None)
        discount_percent = price.next.next.get("title", None)
        link = "https://www.labirint.ru" + book_data.find("a", class_="product-title-link").get("href")
        book_authors = book.find_next("div", class_="product-author").find_all('a')  # авторы
        book_authors = ', '.join([author.get("title", None) for author in book_authors])

        books_data.append(
            {
            "book_title": title,
            "book_genre": genre,
            "book_author": book_authors,
            "book_publishing": publisher,
            "book_new_price": new_price,
            "book_old_price": old_price,
            "book_sale": discount_percent,
            "book_link": link
          }
        )

def writer_result():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f"labirint_{cur_time}_async.json", "w") as file:
        json.dump(books_data, file, indent=4, ensure_ascii=False)

    with open(f"labirint_{cur_time}_async.csv", "w") as file:
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
        with open(f"labirint_{cur_time}_async.csv", "a") as file:
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
