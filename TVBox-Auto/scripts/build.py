import requests

# 只保留直播源M3U的链接，删除失效的wex.json链接
M3U_URL = "https://raw.githubusercontent.com/zilong7728/Collect-IPTV/main/best_sorted.m3u"

def load_m3u():
    # 增加异常处理，避免M3U链接访问失败导致脚本崩溃
    try:
        resp = requests.get(M3U_URL, timeout=30)
        resp.raise_for_status()  # 检查请求是否成功
        text = resp.text
    except Exception as e:
        print(f"获取M3U直播源失败: {e}")
        return [], []
    
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
    # 只加载M3U直播源，删除所有wex.json相关代码
    lives, live_lines = load_m3u()

    # 只保留生成live.m3u的逻辑，删除tvbox_final.json和wex.json的写入
    if live_lines:  # 只有获取到直播源才写入文件
        with open("TVBox-Auto/data/live.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(live_lines) + "\n")
        print("live.m3u 文件更新成功！")
    else:
        print("未获取到有效直播源，跳过写入live.m3u")

if __name__ == "__main__":
    build()
