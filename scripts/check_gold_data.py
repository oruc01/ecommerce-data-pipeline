import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "ecommerce_warehouse",
    "user": "oruc_user",
    "password": "my_secret_password"
}

def check_gold():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Gold cədvəlindən hər şeyi çəkirik
        cursor.execute("SELECT category_upper, total_products, average_price FROM gold_category_summary;")
        rows = cursor.fetchall()

        print("\n==================================================")
        print("📊 GOLDBERG REPO: BİZNES ANALİTİKA DATASI 📊")
        print("==================================================")
        # Sütun adlarını qəşəng formatda çıxarırıq
        print(f"{'KATEQORİYA':<20} | {'TOPLAM MƏHSUL':<15} | {'ORTA QİYMƏT':<12}")
        print("-" * 55)
        
        for row in rows:
            print(f"{row[0]:<20} | {row[1]:<15} | ${row[2]:<12}")
            
        print("==================================================\n")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Məlumat oxunarkən xəta: {e}")

if __name__ == "__main__":
    check_gold()