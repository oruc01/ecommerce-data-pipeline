# Ecommerce End-to-End Data Pipeline 
# 🚀 E-Commerce End-to-End Medallion Data Pipeline

Bu layihə, xam e-ticarət məhsul datalarını (JSON formatında) avtomatik şəkildə qəbul edən, təmizləyən və biznes analitikası üçün hazır vəziyyətə gətirən **End-to-End (Ucdan-Uca) Data Pipeline** sistemidir. Layihədə müasir data memarlığı olan **Medallion Architecture** (Bronze -> Silver -> Gold) tətbiq olunmuşdur.

## 🏗️ Data Memarlığı Sxemi (Architecture)

```text
[ xam_products.json ] 
         │
         ▼ (Extract & Load)
┌─────────────────────────────────┐
│ 🥉 BRONZE: bronze_products      │ -> Xam dataların saxlandığı ilkin təbəqə
└─────────────────────────────────┘
         │
         ▼ (Transform & Clean)
┌─────────────────────────────────┐
│ 🥈 SILVER: silver_products      │ -> Unikal, təmizlənmiş və standartlaşdırılmış data
└─────────────────────────────────┘
         │
         ▼ (Aggregate & Business Logic)
┌─────────────────────────────────┐
│ 🥇 GOLD: gold_category_summary  │ -> Biznes metrikaları (COUNT, AVG qiymət)
└─────────────────────────────────┘
