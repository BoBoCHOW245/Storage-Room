import requests
import json

WEX_URL = "https://9280.kstore.space/wex.json"
M3U_URL = "https://raw.githubusercontent.com/zilong7728/Collect-IPTV/main/best_sorted.m3u"

def load_wex():
    # 下载并返回完整的 wex.json 数据
    resp = requests.get(WEX_URL, timeout=30)
    resp.raise_for_status()  # 请求失败直接报错
    return resp.json()

def load_m3u():
    # 下载并解析 m3u 文件，同时生成新的 live.m3u
    text = requests.get(M3U_URL, timeout=30).text
    lines = []
    live_lines = []
    name = "未知频道"

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("#EXTINF:"):
            # 提取频道名称
            if "," in line:
                name = line.split(",")[-1]
            live_lines.append(line)
        elif line.startswith("http"):
            # 添加到 JSON 数据和 m3u 文件中
            lines.append({
                "name": name,
                "type": 0,
                "playerType": 2,
                "url": line
            })
            live_lines.append(line)
    return lines, live_lines

def build():
    # 1. 下载原始数据
    wex_data = load_wex()
    lives, live_lines = load_m3u()

    # 2. 构建 tvbox_final.json
    final_config = {
        "spider": wex_data.get("spider", ""),
        "wallpaper": wex_data.get("wallpaper", ""),
        "sites": wex_data.get("sites", []),
        "parses": wex_data.get("parses", []),
        "lives": lives
    }

    # 3. 写入三个文件
    # 写入 tvbox_final.json
    with open("TVBox-Auto/tvbox_final.json", "w", encoding="utf-8") as f:
        json.dump(final_config, f, ensure_ascii=False, indent=2)

    # 写入 wex.json（保存完整原始数据）
    with open("TVBox-Auto/wex.json", "w", encoding="utf-8") as f:
        json.dump(wex_data, f, ensure_ascii=False, indent=2)

    # 写入 live.m3u（保存原始 m3u 内容）
    with open("TVBox-Auto/live.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(live_lines) + "\n")

if __name__ == "__main__":
    build()
