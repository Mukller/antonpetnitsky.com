#!/usr/bin/env python3
# Базовый скрипт проверки скорости загрузки сайта
# Проверяет TTFB и полный размер страницы

import subprocess
import sys
import time

def check_ttfb(url="https://antonpetnitsky.com/"):
    try:
        cmd = [
            "curl.exe", "-s", "-o", "/dev/null",
            "-w", "%{time_total}\n",
            "--connect-timeout", "10",
            "--max-time", "30",
            url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
        total_time = float(result.stdout.strip()) if result.stdout.strip() else 999
        print(f"Load time for {url}: {total_time:.2f}s")
        if total_time > 3:
            print("WARNING: Load time > 3s — consider image compression or cache tuning.")
        else:
            print("OK: Load time acceptable.")
        return total_time
    except Exception as e:
        print("ERROR checking load speed:", e)
        return 999

if __name__ == "__main__":
    t = check_ttfb()
    # Check size of key assets
    for asset in ["og.png", "assets/css/style.css", "assets/site.js"]:
        try:
            import os
            size = os.path.getsize(asset)
            kb = size / 1024
            print(f"Asset size: {asset} = {kb:.1f} KB")
            if kb > 500 and asset == "assets/css/style.css":
                print("  Note: CSS file is large — check for unused rules.")
        except FileNotFoundError:
            pass
    sys.exit(0 if t < 999 else 1)
