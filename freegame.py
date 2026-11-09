import sys
import requests

# Çok dilli destek sözlüğü (Türkçe ve İngilizce)
TRANSLATIONS = {
    "tr": {
        "welcome": "========================================\n   STEAM, EPIC & GOG ÜCRETSİZ OYUN TAKİPÇİSİ\n========================================",
        "steam_title": "\n[+] Steam Ücretsiz Oyunlar & Fırsatlar taranıyor...",
        "epic_title": "\n[+] Epic Games Ücretsiz Oyunlar taranıyor...",
        "gog_title": "\n[+] GOG Ücretsiz Oyunlar taranıyor...",
        "no_game": "Bu platformda şu an aktif yeni ücretsiz içerik bulunamadı.",
        "success": "\nİşlem başarıyla tamamlandı.",
        "exit": "\nKapatmak için Enter tuşuna basın..."
    },
    "en": {
        "welcome": "========================================\n   STEAM, EPIC & GOG FREE GAME TRACKER\n========================================",
        "steam_title": "\n[+] Scanning Steam Free Games & Deals...",
        "epic_title": "\n[+] Scanning Epic Games Free Games...",
        "gog_title": "\n[+] Scanning GOG Free Games...",
        "no_game": "No active free items found on this platform currently.",
        "success": "\nProcess completed successfully.",
        "exit": "\nPress Enter to exit..."
    }
}


def get_steam_free_deals(t):
    """Steam üzerindeki ücretsiz oyun ve fırsatları sorgular."""
    print(t["steam_title"])
    try:
        url = "https://store.steampowered.com/search/results/?query=&start=0&count=20&maxprice=free&infinite=1"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        if "results_html" in data and data["results_html"]:
            print("   > Steam bağlantısı başarılı ve veriler alındı.")
            # İsteğe bağlı olarak burada HTML içeriği ayrıştırılabilir.
        else:
            print(f"   > {t['no_game']}")
    except Exception as e:
        print(f"   > Steam verileri alınırken bir hata oluştu: {e}")


def get_epic_official_free_games(t):
    """Epic Games resmi ücretsiz oyun kampanyalarını sorgular."""
    print(t["epic_title"])
    try:
        url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        elements = data.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", [])
        found = False
        for game in elements:
            title = game.get("title")
            promotions = game.get("promotions")
            if promotions:
                print(f"   - [Epic] {title} (Şu an Ücretsiz!)")
                found = True
        if not found:
            print(f"   > {t['no_game']}")
    except Exception as e:
        print(f"   > Epic Games verileri alınırken bir hata oluştu: {e}")


def get_gog_free_games(t):
    """GOG mağazasındaki ücretsiz oyun kataloğunu sorgular."""
    print(t["gog_title"])
    try:
        url = "https://catalog.gog.com/v1/catalog?limit=24&sorting=popularity&price=free"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        products = data.get("products", [])

        if products:
            for prod in products:
                print(f"   - [GOG] {prod.get('title')}")
        else:
            print(f"   > {t['no_game']}")
    except Exception as e:
        print(f"   > GOG verileri alınırken bir hata oluştu: {e}")


if __name__ == "__main__":
    try:
        # Kullanıcıdan dil tercihi alma (Varsayılan: Türkçe)
        lang_choice = input("Dil seçin / Select language (tr / en) [Varsayılan: tr]: ").strip().lower()
        if lang_choice not in TRANSLATIONS:
            lang_choice = "tr"

        t = TRANSLATIONS[lang_choice]

        print(t["welcome"])

        # Fonksiyonların sırayla çalıştırılması
        get_steam_free_deals(t)
        get_epic_official_free_games(t)
        get_gog_free_games(t)

        print(t["success"])

    except Exception as e:
        print(f"\n❌ Beklenmeyen kritik bir hata oluştu: {e}")

    # Programın anında kapanmasını önleyen güvenli kapanış komutu
    input("\nKapatmak için Enter tuşuna basın...")