import requests
import json
import os

def extract_data():
    # Real E-commerce API linki (Məhsullar siyahısı)
    url = "https://fakestoreapi.com/products"
    
    print("API-dan data çəkilir...")
    response = requests.get(url)
    
    # Əgər internet sorğusu uğurludursa (Status Code 200)
    if response.status_code == 200:
        data = response.json()
        print(f"Uğurlu! {len(data)} ədəd məhsul datası tapıldı.")
        
        # Datanı xam şəkildə saxlamaq üçün 'data/bronze' qovluğunu yaradırıq
        os.makedirs('data/bronze', exist_ok=True)
        
        # Datanı JSON faylı olaraq yaddaşa veririk
        with open('data/bronze/products.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print("Xam data 'data/bronze/products.json' ünvanına yazıldı.")
    else:
        print(f"Xəta baş verdi! Status kod: {response.status_code}")

if __name__ == "__main__":
    extract_data()
