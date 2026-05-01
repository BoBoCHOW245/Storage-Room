import requests
import json

WEX_URL = "https://9280.kstore.space/wex.json"
M3U_URL = "https://raw.githubusercontent.com/zilong7728/Collect-IPTV/main/best_sorted.m3u"

def load_wex():
    return requests.get(WEX_URL, timeout=30).json()

def load_m3u():
    text = requests.get(M3U_URL, timeout=30).text
    lives = []

    for line in text.splitlines():
        if line.startswith("#EXTINF"):
            name = line.split(",")[-1]
        elif line.startswith("http"):
            lives.append({
                "name": name,
                "type": 0,
                "playerType": 2,
                "url": line.strip()
            })
    return lives

def build():
    wex = load_wex()
    lives = load_m3u()

    final = {
        "spider": wex.get("spider", ""),
        "wallpaper": wex.get("wallpaper", ""),
        "sites": wex.get("sites", []),
        "parses": wex.get("parses", []),
        "lives": lives
    }

    with open("TVBox-Auto/tvbox_final.json", "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    build()
