import psycopg2
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "ecommerce_warehouse",
    "user": "oruc_user",
    "password": "my_secret_password"
}

def generate_gold_summary():
    try:
        print("PostgreSQL bazasına qoşulur (Gold Prosesi)...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 1. Silver təbəqəsindən datanı SQL-də qruplaşdıraraq (Aggregate) çəkirik
        print("Silver təbəqəsindən analitik məlumatlar hesablanır...")
        aggregate_query = """
            SELECT 
                category_upper, 
                COUNT(*) as total_products, 
                ROUND(AVG(clean_price), 2) as average_price 
            FROM silver_products
            GROUP BY category_upper;
        """
        cursor.execute(aggregate_query)
        summary_data = cursor.fetchall()

        # 2. Hesablanmış datanı Gold cədvəlinə yazırıq
        insert_gold_query = """
        INSERT INTO gold_category_summary (category_upper, total_products, average_price, calculated_at)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (category_upper) DO UPDATE SET
            total_products = EXCLUDED.total_products,
            average_price = EXCLUDED.average_price,
            calculated_at = EXCLUDED.calculated_at;
        """

        for row in summary_data:
            cursor.execute(insert_gold_query, (
                row[0], # category_upper
                row[1], # total_products
                row[2], # average_price
                datetime.now()
            ))

        conn.commit()
        print(f"Uğurlu! {len(summary_data)} kateqoriya üzrə biznes xülasəsi Gold təbəqəsinə yazıldı! 🏆💰")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Gold mərhələsində xəta baş verdi: {e}")

if __name__ == "__main__":
    generate_gold_summary()