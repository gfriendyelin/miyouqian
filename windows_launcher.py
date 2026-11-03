# -*- coding: utf-8 -*-
from pathlib import Path
import sys, threading, time, webbrowser, shutil
from miyouqian.cli import main
from miyouqian.core.config import create_config

def run():
    base = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
    config = base / "config.yaml"
    if not config.exists():
        example = base / "config.example.yaml"
        shutil.copy2(example, config) if example.exists() else create_config(config)
    url = "http://127.0.0.1:5890"
    def open_page():
        time.sleep(2)
        webbrowser.open(url)
    threading.Thread(target=open_page, daemon=True).start()
    print("米游签正在启动：" + url)
    print("关闭此窗口即可停止服务。")
    return main(["--config", str(config), "serve", "--host", "127.0.0.1", "--port", "5890"])

if __name__ == "__main__":
    raise SystemExit(run())
