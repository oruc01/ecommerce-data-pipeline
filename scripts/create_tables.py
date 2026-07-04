import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "ecommerce_warehouse",
    "user": "oruc_user",
    "password": "my_secret_password"
}

def create_tables():
    try:
        print("PostgreSQL bazasına qoşulur...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 1. Bronze
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bronze_products (
            id SERIAL PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL,
            price NUMERIC(10, 2),
            category VARCHAR(100),
            extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 2. Silver
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS silver_products (
            id INT PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL,
            clean_price NUMERIC(10, 2),
            category_upper VARCHAR(100),
            transformed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 3. Gold
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS gold_category_summary (
            category_upper VARCHAR(100) PRIMARY KEY,
            total_products INT,
            average_price NUMERIC(10, 2),
            calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        conn.commit()
        print("Təbriklər! 'bronze', 'silver' və 'gold' cədvəlləri uğurla hazır vəziyyətə gətirildi. 🏆🎉")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Baza ilə əlaqə zamanı xəta baş verdi: {e}")

if __name__ == "__main__":
    create_tables()