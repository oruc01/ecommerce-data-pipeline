import psycopg2
import time

# Docker-dəki PostgreSQL bazamıza qoşulma parametrləri
# docker-compose.yml faylında nə yazmışdıqsa, tam olaraq eynisidir
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "ecommerce_warehouse",
    "user": "oruc_user",
    "password": "my_secret_password"
}

def create_tables():
    try:
        # Bazaya körpü (bağlantı) salırıq
        print("PostgreSQL bazasına qoşulur...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # İlk cədvəlimizi (products) yaradacaq SQL sorğusu
        create_table_query = """
        CREATE TABLE IF NOT EXISTS bronze_products (
            id SERIAL PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL,
            price NUMERIC(10, 2),
            category VARCHAR(100),
            extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        # Sorğunu bazada icra edirik
        cursor.execute(create_table_query)
        
        # Dəyişiklikləri bazaya bərkidirik (Commit)
        conn.commit()
        print("Təbriklər! 'bronze_products' cədvəli uğurla yaradıldı. 🎉")

        # Qapıları bağlayırıq
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Baza ilə əlaqə zamanı xəta baş verdi: {e}")

if __name__ == "__main__":
    create_tables()