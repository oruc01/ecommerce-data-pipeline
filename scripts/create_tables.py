import psycopg2

# Docker-dəki yeni parametrlərimiz
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

        # 1. Bronze cədvəli
        create_bronze_table = """
        CREATE TABLE IF NOT EXISTS bronze_products (
            id SERIAL PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL,
            price NUMERIC(10, 2),
            category VARCHAR(100),
            extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_bronze_table)

        # 2. Silver cədvəli
        create_silver_table = """
        CREATE TABLE IF NOT EXISTS silver_products (
            id INT PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL,
            clean_price NUMERIC(10, 2),
            category_upper VARCHAR(100),
            transformed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_silver_table)
        
        conn.commit()
        print("Təbriklər! Həm 'bronze', həm 'silver' cədvəlləri uğurla hazır vəziyyətə gətirildi. 🎉")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Baza ilə əlaqə zamanı xəta baş verdi: {e}")

# Bu hissə mütləq faylın ən aşağısında olmalıdır ki, kod icra olunsun!
if __name__ == "__main__":
    create_tables()