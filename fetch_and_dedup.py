# fetch_and_dedup.py
# Запускается вручную на RDP-машине
# Скачивает подписки → убирает дубли → сохраняет в E:\ЕГ\принтер\keys GitHub\configs.txt

import base64
import requests
from urllib.parse import urlparse, parse_qs
import os

# Список подписок (можно добавлять новые)
sub_urls = [
    "https://raw.githubusercontent.com/LowiKLive/BypassWhitelistRu/refs/heads/main/WhiteList-Bypass_Ru.txt",
    "https://raw.githubusercontent.com/igareck/bypass-whitelist-ru/main/subscription.txt",
    "https://raw.githubusercontent.com/zieng2/whitelist-bypass-ru/main/subscription.txt",
    # Добавь свои подписки сюда, если нужно
]

# Путь на RDP-машине
shared_folder = r"E:\ЕГ\принтер\keys GitHub"
configs_file = os.path.join(shared_folder, "configs.txt")

def fetch_configs_from_sub(sub_url):
    try:
        r = requests.get(sub_url, timeout=15)
        if r.status_code == 200:
            content = r.text.strip()
            try:
                decoded = base64.b64decode(content + "==").decode('utf-8', errors='ignore')
            except:
                decoded = content
            lines = [line.strip() for line in decoded.splitlines() if line.strip()]
            # Оставляем только нужные протоколы
            return [c for c in lines if c.startswith(('vmess://', 'vless://', 'ss://', 'trojan://', 'hy2://', 'hysteria2://'))]
        else:
            print(f"Статус {r.status_code} для {sub_url}")
            return []
    except Exception as e:
        print(f"Ошибка подписки {sub_url}: {e}")
        return []

def get_unique_key(config):
    """Дедупликация как в NekoBox / sing-box"""
    try:
        u = urlparse(config)
        key = f"{u.scheme}://{u.hostname}:{u.port or 443}{u.path}"
        if u.query:
            q = parse_qs(u.query)
            key += "?" + "&".join(f"{k}={v[0]}" for k,v in sorted(q.items()))
        return key
    except:
        return config

def deduplicate_configs(configs):
    seen = {}
    for c in configs:
        k = get_unique_key(c)
        if k not in seen:
            seen[k] = c
    return list(seen.values())

# Основная часть
all_configs = []
for url in sub_urls:
    print(f"Обрабатываю: {url}")
    configs = fetch_configs_from_sub(url)
    all_configs.extend(configs)

unique_configs = deduplicate_configs(all_configs)
print(f"\nСобрано уникальных конфигов: {len(unique_configs)}")

os.makedirs(shared_folder, exist_ok=True)
with open(configs_file, "w", encoding="utf-8") as f:
    f.write("\n".join(unique_configs))

print(f"\nГотово! Файл сохранён: {configs_file}")
print("Теперь на локальном ПК запусти test_configs.py")
