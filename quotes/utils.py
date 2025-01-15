from pymongo import MongoClient
from collections import Counter

def get_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['hw_10']
    return db

def get_top_tags():
    db = get_mongodb()
    quotes = db.quotes.find()  # Отримуємо всі цитати
    all_tags = []

    # Перебираємо всі цитати та додаємо їх теги до списку
    for quote in quotes:
        all_tags.extend(quote.get('tags', []))  # Якщо немає тегів, повернемо порожній список

    # Підраховуємо кількість кожного тега
    tag_counts = Counter(all_tags)
    
    # Повертаємо топ-10 тегів
    top_tags = tag_counts.most_common(10)
    return top_tags