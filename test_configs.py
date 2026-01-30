# test_configs.py
# Запускается вручную на локальном ПК
# Берёт configs.txt → параллельно тестирует → сохраняет рабочие в tested_configs.txt

import os
import subprocess
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # для красивого прогресс-бара

# Путь на локальном ПК
shared_folder = r"Z:\принтер\keys GitHub"
configs_file = os.path.join(shared_folder, "configs.txt")
tested_file = os.path.join(shared_folder, "tested_configs.txt")

# Сколько одновременно проверять (можно увеличить до 50–100)
MAX_WORKERS = 30

def test_config(config):
    """Простой тест: резолвинг + ping хоста"""
    try:
        u = urlparse(config)
        host = u.hostname
        if not host:
            return False, config

        # Пинг — 1 пакет, таймаут 2 секунды
        result = subprocess.run(
            ['ping', '-n', '1', '-w', '2000', host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5
        )
        return result.returncode == 0, config
    except:
        return False, config

def main():
    if not os.path.exists(configs_file):
        print(f"Файл configs.txt не найден: {configs_file}")
        return

    with open(configs_file, "r", encoding="utf-8") as f:
        configs = [line.strip() for line in f if line.strip()]

    print(f"\nНайдено конфигов для теста: {len(configs)}")
    print(f"Запускаем параллельную проверку ({MAX_WORKERS} потоков)...\n")

    passed = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_config = {executor.submit(test_config, conf): conf for conf in configs}

        with tqdm(total=len(configs), desc="Проверка", unit="conf") as pbar:
            for future in as_completed(future_to_config):
                success, config = future.result()
                if success:
                    passed.append(config)
                pbar.update(1)

    print(f"\nПрошли тест: {len(passed)} из {len(configs)}")
    print(f"Не прошли: {len(configs) - len(passed)}")

    if passed:
        with open(tested_file, "w", encoding="utf-8") as f:
            f.write("\n".join(passed))
        print(f"\nРабочие конфиги сохранены: {tested_file}")
    else:
        print("\nНи один конфиг не прошёл тест.")

    print("\nГотово! Теперь на RDP-машине можно запустить пуш в GitHub.")

if __name__ == "__main__":
    main()
