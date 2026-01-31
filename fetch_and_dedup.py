import os
import re
import ssl
import base64
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# === НАСТРОЙКИ ПУТЕЙ ===
shared_folder = r"E:\ЕГ\принтер\keys GitHub"
configs_file = os.path.join(shared_folder, "configs.txt")
log_file = os.path.join(shared_folder, "log.txt")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# === ПОЛНЫЙ СПИСОК ССЫЛОК ===
sub_urls = list(set([
    # EtoNeYaProject - оставляем обе, как ты просил
    "https://raw.githubusercontent.com/EtoNeYaProject/etoneyaproject.github.io/main/whitelist",
    "https://raw.githubusercontent.com/EtoNeYaProject/etoneyaproject.github.io/main/test",
    
    # Свежие источники
    "https://rstnnl.gitverse.site/sb/dev.txt",
    "https://nowmeow.pw/8ybBd3fdCAQ6Ew5H0d66Y1hMbh63GpKUtEXQClIu/whitelist",
    "https://gitverse.ru/api/repos/LowiK/LowiKLive/raw/branch/main/ObhodBSfree.txt",
    
    # Основной массив (GitHub, S3, Gists)
    "https://raw.githubusercontent.com/Egkaz/Proxy-list-20k-server/main/stable.txt",
    "https://raw.githubusercontent.com/LimeHi/LimeVPN/main/LimeVPN.txt",
    "https://raw.githubusercontent.com/xcom024/vless/main/list.txt",
    "https://raw.githubusercontent.com/KiryaScript/white-lists/main/githubmirror/28.txt",
    "https://raw.githubusercontent.com/KiryaScript/white-lists/main/githubmirror/27.txt",
    "https://raw.githubusercontent.com/KiryaScript/white-lists/main/githubmirror/26.txt",
    "https://wlr.s3-website.cloud.ru/zNhbYZtBc",
    "https://s3c3.001.gpucloud.ru/dixsm/htxml",
    "https://raw.githubusercontent.com/sakha1370/OpenRay/main/output/kind/vless.txt",
    "https://raw.githubusercontent.com/FLEXIY0/matryoshka-vpn/main/configs/russia_whitelist.txt",
    "https://storage.yandexcloud.net/cid-vpn/whitelist.txt",
    "http://fsub.flux.2bd.net/githubmirror/bypass/bypass-all.txt",
    "https://storage.yandexcloud.net/nllrcn-proxy-subs/subs/main-sub.txt",
    "https://raw.githubusercontent.com/whoahaow/rjsxrd/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt",
    "https://raw.githubusercontent.com/vsevjik/OBWL/main/wwh",
    "https://raw.githubusercontent.com/LowiKLive/BypassWhitelistRu/main/WhiteList-Bypass_Ru.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_universal.txt",
    "https://raw.githubusercontent.com/STR97/STRUGOV/main/STR.BYPASS",
    "https://bp.wl.free.nf/confs/wl.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-CIDR-RU-checked.txt",
    "https://raw.githubusercontent.com/55prosek-lgtm/vpn_config_for_russia/main/whitelist.txt",
    "https://raw.githubusercontent.com/Created-By/Telegram-Eag1e_YT/main/%40Eag1e_YT",
    "https://raw.githubusercontent.com/Mosifree/-FREE2CONFIG/main/Reality",
    "https://peige.dpkj.qzz.io/dapei",
    "https://raw.githubusercontent.com/ovmvo/SubShare/main/sub/permanent/mihomo.yaml",
    "https://raw.githubusercontent.com/AzadNetCH/Clash/main/AzadNet_hy.txt",
    "https://raw.githubusercontent.com/amirkma/proxykma/main/mix.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity",
    "https://gist.githubusercontent.com/Syavar/7b868a1682aa4a87d9ec2e9bca729f38/raw/gistfile1.txt",
    "https://gist.githubusercontent.com/Syavar/3e76222fc05fde9abcb35c2f24572021/raw/gistfile1.txt",
    "https://raw.githubusercontent.com/Kirillo4ka/vpn-configs-for-russia/main/Vless-Rus-Mobile-White-List.txt",
    "https://raw.githubusercontent.com/vlesscollector/vlesscollector/main/vless_configs.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/hamedp-71/v2go_NEW/main/All_Configs_base64_Sub.txt",
    "https://raw.githubusercontent.com/ninjastrikers/v2ray-configs/main/splitted/vless.txt",
    "https://raw.githubusercontent.com/Sage-77/V2ray-configs/main/config.txt",
    "https://raw.githubusercontent.com/kort0881/vpn-key-vless/main/vpn-files/all_posts.txt",
    "https://raw.githubusercontent.com/SoroushImanian/BlackKnight/main/sub/vlessbase64"
] + [f"https://github.com/AvenCores/goida-vpn-configs/raw/main/githubmirror/{i}.txt" for i in range(1, 27)]))

def fetch_urllib(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=45, context=ctx) as response:
            content = response.read().decode('utf-8', errors='ignore').strip()
        
        pattern = r'(vmess|vless|ss|trojan|hy2|tuic|wg|hysteria)://[^\s"\'<>]+'
        valid = [m.group(0).strip() for m in re.finditer(pattern, content, re.I)]
        
        # Если в открытом виде нет, пробуем декодировать Base64
        if not valid and len(content) > 30:
            try:
                # Очистка для NowMeow и других зашифрованных списков
                clean_content = "".join([l.strip() for l in content.splitlines() if not l.strip().startswith('#') and ':' not in l[:10]])
                decoded = base64.b64decode(clean_content + "===").decode('utf-8', errors='ignore')
                valid = [m.group(0).strip() for m in re.finditer(pattern, decoded, re.I)]
            except: pass
        return {"url": url, "configs": valid, "count": len(valid), "status": "OK"}
    except Exception as e:
        return {"url": url, "configs": [], "count": 0, "status": f"Err: {str(e)[:15]}"}

if __name__ == "__main__":
    start_time = datetime.now()
    print(f"[{start_time.strftime('%H:%M:%S')}] СТАРТ СБОРА ({len(sub_urls)} источников)...")
    os.makedirs(shared_folder, exist_ok=True)

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(fetch_urllib, sub_urls))

    all_raw = []
    log_lines = [f"Мега-отчет от {datetime.now()}"]
    for r in results:
        all_raw.extend(r["configs"])
        log_lines.append(f"[{r['status']}] | {r['count']} | {r['url']}")

    # Умная очистка (оставляем один экземпляр сервера, даже если названия разные)
    unique_map = {}
    for c in all_raw:
        body = c.split('#')[0].strip() if '#' in c else c.strip()
        if body not in unique_map:
            unique_map[body] = c

    final_keys = list(unique_map.values())
    
    with open(configs_file, "w", encoding="utf-8") as f:
        f.write("\n".join(final_keys))
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

    end_time = datetime.now()
    print(f"\n--- ГОТОВО ЗА {(end_time - start_time).seconds} сек. ---")
    print(f"Всего ключей найдено: {len(all_raw)}")
    print(f"Чистых (уникальных): {len(final_keys)}")
    print(f"Файл сохранен: {configs_file}")