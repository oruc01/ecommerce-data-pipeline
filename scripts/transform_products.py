import psycopg2
from datetime import datetime

# Docker bazamızın parametrləri
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "ecommerce_warehouse",
    "user": "oruc_user",
    "password": "my_secret_password"
}

def transform_and_load_silver():
    try:
        print("PostgreSQL bazasına qoşulur...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 1. Datanı BRONZE cədvəlindən oxuyuruq
        print("Bronze təbəqəsindən xam datalar oxunur...")
        cursor.execute("SELECT id, product_name, price, category FROM bronze_products;")
        raw_products = cursor.fetchall()

        # 2. SILVER cədvəlinə yazmaq üçün SQL sorğusu Hazırlayırıq
        # Əgər eyni ID-li məhsul varsa, üzərinə yazsın (ON CONFLICT)
        insert_silver_query = """
        INSERT INTO silver_products (id, product_name, clean_price, category_upper, transformed_at)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            product_name = EXCLUDED.product_name,
            clean_price = EXCLUDED.clean_price,
            category_upper = EXCLUDED.category_upper,
            transformed_at = EXCLUDED.transformed_at;
        """

        # 3. Məlumatları təmizləyib sətir-sətir Silver-ə yükləyirik
        print("Datanın transformasiyası və Silver təbəqəsinə köçürülməsi başlayır...")
        for row in raw_products:
            prod_id = row[0]
            prod_name = row[1]
            price = row[2]
            category = row[3]

            # --- TRANSFORMATSİYA HİSSƏSİ ---
            # Kateqoriya adını tamamilə böyük hərflərə çeviririk
            clean_category = category.upper() if category else "UNKNOWN"
            # -------------------------------

            # Silver cədvəlinə yazırıq
            cursor.execute(insert_silver_query, (
                prod_id,
                prod_name,
                price,
                clean_category,
                datetime.now()
            ))

        # Dəyişiklikləri təsdiqləyirik
        conn.commit()
        print(f"Uğurlu! Toplam {len(raw_products)} məhsul təmizləndi və 'silver_products' cədvəlinə köçürüldü! 🥈🚀")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Transformasiya zamanı xəta baş verdi: {e}")

if __name__ == "__main__":
    transform_and_load_silver()