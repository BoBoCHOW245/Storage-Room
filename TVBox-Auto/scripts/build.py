import requests
import json

WEX_URL = "https://9280.kstore.space/wex.json"
M3U_URL = "https://raw.githubusercontent.com/zilong7728/Collect-IPTV/main/best_sorted.m3u"

def load_wex():
    resp = requests.get(WEX_URL, timeout=30)
    resp.raise_for_status()
    return resp.json()

def load_m3u():
    text = requests.get(M3U_URL, timeout=30).text
    lines = []
    live_lines = []
    name = "未知频道"

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("#EXTINF:"):
            if "," in line:
                name = line.split(",")[-1]
            live_lines.append(line)
        elif line.startswith("http"):
            lines.append({
                "name": name,
                "type": 0,
                "playerType": 2,
                "url": line
            })
            live_lines.append(line)
    return lines, live_lines

def build():
    wex_data = load_wex()
    lives, live_lines = load_m3u()

    final_config = {
        "spider": wex_data.get("spider", ""),
        "wallpaper": wex_data.get("wallpaper", ""),
        "sites": wex_data.get("sites", []),
        "parses": wex_data.get("parses", []),
        "lives": lives
    }

    # ✅ 全部写入 data 文件夹
    with open("TVBox-Auto/data/tvbox_final.json", "w", encoding="utf-8") as f:
        json.dump(final_config, f, ensure_ascii=False, indent=2)

    with open("TVBox-Auto/data/wex.json", "w", encoding="utf-8") as f:
        json.dump(wex_data, f, ensure_ascii=False, indent=2)

    with open("TVBox-Auto/data/live.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(live_lines) + "\n")

if __name__ == "__main__":
    build()
