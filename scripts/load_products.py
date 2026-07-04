import json
import psycopg2
from datetime import datetime

# Sənin Docker parametrlərinə uyğun config
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "ecommerce_warehouse",
    "user": "oruc_user",
    "password": "my_secret_password"
}

def load_json_to_postgres():
    try:
        # 1. JSON faylını oxuyuruq
        json_path = "data/bronze/products.json"
        print(f"{json_path} faylı oxunur...")
        with open(json_path, "r", encoding="utf-8") as f:
            products = json.load(f)

        # 2. Bazaya qoşuluruq
        print("PostgreSQL bazasına qoşulur...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 3. Məlumatları sətir-sətir bazaya yazırıq
        insert_query = """
        INSERT INTO bronze_products (product_name, price, category, extracted_at)
        VALUES (%s, %s, %s, %s);
        """

        for product in products:
            # Dəyişiklik buradadır: product["product_name"] yerinə product["title"] yazdıq!
            cursor.execute(insert_query, (
                product["title"],    # JSON-dakı 'title' dəyərini bazadakı 'product_name' sütununa yazır
                product["price"],
                product["category"],
                datetime.now()
            ))

        # 4. Dəyişiklikləri təsdiqləyirik
        conn.commit()
        print(f"Uğurlu! Toplam {len(products)} məhsul 'bronze_products' cədvəlinə yükləndi! 🚀")

        # Qapıları bağlayırıq
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Datanı yükləyərkən xəta baş verdi: {e}")

if __name__ == "__main__":
    load_json_to_postgres()