import base64, requests, os, shutil
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

sub_urls = [
    "https://raw.githubusercontent.com/whoahaow/rjsxrd/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt",
    "https://raw.githubusercontent.com/vsevjik/OBSpiskov/refs/heads/main/wwh#OBSpiskov",
    "https://raw.githubusercontent.com/LowiKLive/BypassWhitelistRu/refs/heads/main/WhiteList-Bypass_Ru.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt",
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_universal.txt",
    "https://raw.githubusercontent.com/STR97/STRUGOV/refs/heads/main/STR.BYPASS#STR.BYPASS",
    "https://bp.wl.free.nf/confs/wl.txt",
    "https://nowmeow.pw/8ybBd3fdCAQ6Ew5H0d66Y1hMbh63GpKUtEXQClIu/whitelist",
    "https://rstnnl.gitverse.site/sb/dev.txt",
    "https://raw.githubusercontent.com/EtoNeYaProject/etoneyaproject.github.io/refs/heads/main/whitelist",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-checked.txt",
    "https://bp.wl.free.nf/confs/merged.txt",
    "https://bp.wl.free.nf/confs/selected.txt",
    "https://raw.githubusercontent.com/Created-By/Telegram-Eag1e_YT/main/%40Eag1e_YT",
    "https://raw.githubusercontent.com/Mosifree/-FREE2CONFIG/refs/heads/main/Clash_T,H",
    "https://raw.githubusercontent.com/Mosifree/-FREE2CONFIG/refs/heads/main/T,H",
    "https://raw.githubusercontent.com/Mosifree/-FREE2CONFIG/refs/heads/main/Clash_Reality",
    "https://raw.githubusercontent.com/Mosifree/-FREE2CONFIG/refs/heads/main/Reality",
    "https://peige.dpkj.qzz.io/dapei",
    "https://raw.githubusercontent.com/ovmvo/SubShare/refs/heads/main/sub/permanent/mihomo.yaml",
    "https://raw.githubusercontent.com/AzadNetCH/Clash/main/AzadNet_hy.txt",
    "https://raw.githubusercontent.com/amirkma/proxykma/refs/heads/main/mix.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity",
    "https://gist.githubusercontent.com/Syavar/7b868a1682aa4a87d9ec2e9bca729f38/raw/75ff3ee7c1bb9e08c5f1d91cbc4ee2b82d25635a/gistfile1.txt",
    "https://gist.githubusercontent.com/Syavar/3e76222fc05fde9abcb35c2f24572021/raw/e2f7ef901ae4ba5bab7bef20adef41bead7ba626/gistfile1.txt",
    "https://raw.githubusercontent.com/Kirillo4ka/vpn-configs-for-russia/refs/heads/main/Vless-Rus-Mobile-White-List.txt",
    "https://raw.githubusercontent.com/vlesscollector/vlesscollector/refs/heads/main/vless_configs.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vless.txt",
    "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/hamedp-71/v2go_NEW/main/All_Configs_base64_Sub.txt",
    "https://raw.githubusercontent.com/hamedp-71/v2go_NEW/main/Splitted-By-Protocol/hy2.txt",
    "https://raw.githubusercontent.com/ninjastrikers/v2ray-configs/main/splitted/vless.txt",
    "https://github.com/kismetpro/NodeSuber/raw/refs/heads/main/out/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/Sage-77/V2ray-configs/main/config.txt",
    "https://raw.githubusercontent.com/kort0881/vpn-key-vless/refs/heads/main/vpn-files/all_posts.txt",
    "https://raw.githubusercontent.com/SoroushImanian/BlackKnight/main/sub/vlessbase64",
    "https://github.com/kismetpro/NodeSuber/raw/refs/heads/main/Splitted-By-Protocol/vless.txt",
    "https://github.com/kismetpro/NodeSuber/raw/refs/heads/main/Splitted-By-Protocol/trojan.txt"
]

path = r"E:\ЕГ\принтер\keys GitHub"
file, log = os.path.join(path, "configs.txt"), os.path.join(path, "log.txt")

def rotate(p):
    if os.path.exists(p):
        b = p + ".bak"
        if os.path.exists(b): os.remove(b)
        os.rename(p, b)

def fetch_one(u):
    try:
        r = requests.get(u, headers={"User-Agent":"Mozilla/5.0"}, timeout=15)
        if r.status_code == 200:
            c = r.text.strip()
            if '://' not in c[:100]:
                try: c = base64.b64decode(c + "==" * (-len(c) % 4)).decode('utf-8', errors='ignore')
                except: pass
            v = [l.strip() for l in c.splitlines() if l.strip().startswith(('vless://','vmess://','ss://','trojan://','hy2://'))]
            return {"u": u, "c": v, "n": len(v)}
    except: pass
    return {"u": u, "c": [], "n": 0}

print("Сбор ключей...")
with ThreadPoolExecutor(max_workers=15) as ex:
    res = list(ex.map(fetch_one, sub_urls))

all_c = []
lines = [f"Log {datetime.now()}"]
for r in res:
    all_c.extend(r['c'])
    lines.append(f"{r['n']} | {r['u']}")

# Дедупликация по адресу
unique = list({urlparse(c).netloc + urlparse(c).path: c for c in all_c}.values())

rotate(file)
with open(file, "w", encoding="utf-8") as f: f.write("\n".join(unique))
rotate(log)
with open(log, "w", encoding="utf-8") as f: f.write("\n".join(lines))
print(f"Готово. Собрано: {len(unique)}")