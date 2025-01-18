import pymongo
import psycopg2
from psycopg2.extras import execute_values

# Підключення до MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["hw_10"]
# Підключення до PostgreSQL
pg_conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="0997943465",  # Замініть на ваш пароль
    host="localhost",
    port="5433",
)
pg_cursor = pg_conn.cursor()

# 1. Створення таблиць у PostgreSQL
pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bio TEXT
);

CREATE TABLE IF NOT EXISTS quotes (
    id SERIAL PRIMARY KEY,
    quote TEXT NOT NULL,
    author_id INTEGER REFERENCES authors(id),
    tags TEXT[]
);
""")
pg_conn.commit()

# 2. Міграція авторів
authors_collection = mongo_db["authors"]  # Колекція авторів у MongoDB
authors_map = {}  # Для збереження відповідності ID авторів між MongoDB та PostgreSQL

for author in authors_collection.find():
    pg_cursor.execute(
        "INSERT INTO authors (name, bio) VALUES (%s, %s) RETURNING id;",
        (author["fullname"], author.get("bio", ""))
    )
    author_id = pg_cursor.fetchone()[0]
    authors_map[author["_id"]] = author_id

pg_conn.commit()

# 3. Міграція цитат
quotes_collection = mongo_db["quotes"]  # Колекція цитат у MongoDB

quotes_data = []
for quote in quotes_collection.find():
    author_id = authors_map.get(quote["author"])
    tags = quote.get("tags", [])
    quotes_data.append((quote["quote"], author_id, tags))

execute_values(
    pg_cursor,
    "INSERT INTO quotes (quote, author_id, tags) VALUES %s;",
    quotes_data
)
pg_conn.commit()

# Закриваємо з'єднання
pg_cursor.close()
pg_conn.close()
mongo_client.close()

print("Міграцію завершено успішно!")
