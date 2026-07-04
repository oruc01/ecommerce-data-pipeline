import sys
import os

# scripts qovluğundakı kodları tapmaq üçün
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from create_tables import create_tables
from load_products import load_json_to_postgres
from transform_products import transform_and_load_silver

def run_pipeline():
    print("==================================================")
    print("🚀 E-COMMERCE DATA PIPELINE BAŞLAYIR... 🚀")
    print("==================================================")

    print("\n[ADDIM 1/3] Cədvəllər yoxlanılır...")
    create_tables()

    print("\n[ADDIM 2/3] Xam data oxunur və Bronze-a yüklənir...")
    load_json_to_postgres()

    print("\n[ADDIM 3/3] Data təmizlənir və Silver-ə köçürülür...")
    transform_and_load_silver()

    print("\n==================================================")
    print("🎉 TƏBRİKLƏR! BÜTÜN DATA PİPELİNE UĞURLA BAŞA ÇATDI! 🎉")
    print("==================================================")

if __name__ == "__main__":
    run_pipeline()