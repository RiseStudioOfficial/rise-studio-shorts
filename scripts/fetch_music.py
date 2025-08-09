#!/usr/bin/env python3
import os, json, hashlib, requests, pathlib

MUSIC_DIR = "assets/music"
SOURCES = "data/music_sources.json"
TARGET_MUSIC_COUNT = int(os.getenv("TARGET_MUSIC_COUNT", "30"))
TIMEOUT = 25

os.makedirs(MUSIC_DIR, exist_ok=True)

def have_enough():
    return len(list(pathlib.Path(MUSIC_DIR).glob("*.mp3"))) >= TARGET_MUSIC_COUNT

def download(url, title):
    safe = "".join(c for c in title if c.isalnum() or c in " _-").strip().replace(" ","_")
    path = os.path.join(MUSIC_DIR, f"{safe}.mp3")
    if os.path.exists(path): return False
    try:
        r = requests.get(url, stream=True, timeout=TIMEOUT)
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(65536):
                if chunk: f.write(chunk)
        if os.path.getsize(path) < 50_000:
            os.remove(path); return False
        print("Downloaded music:", path)
        return True
    except Exception as e:
        print("Music failed:", url, e)
        try:
            if os.path.exists(path): os.remove(path)
        except: pass
        return False

def main():
    if not os.path.exists(SOURCES):
        print("No music_sources.json found"); return
    with open(SOURCES, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    count=0
    for t in cfg.get("tracks", []):
        if have_enough(): break
        if download(t["url"], t["title"]): count += 1
    print(f"Fetched {count} tracks (target {TARGET_MUSIC_COUNT}).")

if __name__ == "__main__":
    main()
