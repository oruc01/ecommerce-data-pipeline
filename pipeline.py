import sys
import os

# scripts qovluğundakı kodları tapmaq üçün
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

# Bütün mərhələlərin funksiyalarını import edirik
from create_tables import create_tables
from load_products import load_json_to_postgres
from transform_products import transform_and_load_silver
from generate_gold import generate_gold_summary  # Yeni əlavə etdiyimiz Gold funksiyası

def run_pipeline():
    print("==================================================")
    print("🚀 E-COMMERCE END-TO-END DATA PIPELINE BAŞLAYIR... 🚀")
    print("==================================================")

    # Addım 1: İnfrastruktur
    print("\n[ADDIM 1/4] Cədvəllər yoxlanılır (Bronze, Silver, Gold)...")
    create_tables()

    # Addım 2: Extract & Load
    print("\n[ADDIM 2/4] Xam data oxunur və Bronze-a yüklənir...")
    load_json_to_postgres()

    # Addım 3: Transform
    print("\n[ADDIM 3/4] Data təmizlənir və Silver-ə köçürülür...")
    transform_and_load_silver()

    # Addım 4: Aggregate (Biznes Analitika)
    print("\n[ADDIM 4/4] Biznes metrikaları hesablanır və Gold-a yazılır...")
    generate_gold_summary()

    print("\n==================================================")
    print("🏆 🎉 TƏBRİKLƏR! BRONZE -> SILVER -> GOLD ZƏNCİRİ TAMAMLANDI! 🎉 🏆")
    print("==================================================")

if __name__ == "__main__":
    run_pipeline()