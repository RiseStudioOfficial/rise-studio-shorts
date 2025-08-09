#!/usr/bin/env python3
import os, sys, json, time, hashlib, csv, random, pathlib
import requests

ASSETS_BG = "assets/backgrounds"
LICENSE_LOG = "data/licenses.csv"
QUERIES_FILE = "data/background_queries.txt"

PEXELS_KEY = os.getenv("PEXELS_API_KEY", "")
PIXABAY_KEY = os.getenv("PIXABAY_API_KEY", "")
TARGET_BG_COUNT = int(os.getenv("TARGET_BG_COUNT", "120"))  # держим не более 120 фонов
TIMEOUT = 20

os.makedirs(ASSETS_BG, exist_ok=True)
os.makedirs("assets/music", exist_ok=True)
os.makedirs("assets/fonts", exist_ok=True)
os.makedirs("data", exist_ok=True)

def sha1_file(path):
    h=hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def write_license(path, source, license_name, author, url):
    new = not os.path.exists(LICENSE_LOG)
    with open(LICENSE_LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new: w.writerow(["path","source","license","author","url"])
        w.writerow([path, source, license_name, author, url])

def fetch_pexels(query, per_page=5):
    if not PEXELS_KEY: return []
    headers={"Authorization": PEXELS_KEY}
    out=[]
    try:
        r = requests.get("https://api.pexels.com/v1/search", params={"query":query,"per_page":per_page,"orientation":"portrait"}, headers=headers, timeout=TIMEOUT)
        if r.ok:
            for p in r.json().get("photos", []):
                out.append({
                    "type":"image",
                    "url": p["src"]["large2x"],
                    "author": p["photographer"],
                    "page": p["url"],
                    "source": "Pexels",
                    "license": "Pexels License"
                })
        r2 = requests.get("https://api.pexels.com/videos/search", params={"query":query,"per_page":per_page,"orientation":"portrait"}, headers=headers, timeout=TIMEOUT)
        if r2.ok:
            for v in r2.json().get("videos", []):
                vids = v.get("video_files", [])
                # взять лучшее приближение к 1080x1920
                vids.sort(key=lambda x: (abs((x.get("height") or 0)-1920) + abs((x.get("width") or 0)-1080)))
                if vids:
                    out.append({
                        "type":"video",
                        "url": vids[0]["link"],
                        "author": ", ".join([u.get("name","") for u in v.get("user",[])]) if isinstance(v.get("user"), list) else (v.get("user",{}).get("name","")),
                        "page": v.get("url",""),
                        "source": "Pexels",
                        "license": "Pexels License"
                    })
    except Exception as e:
        print("PEXELS error:", e)
    return out

def fetch_pixabay(query, per_page=5):
    if not PIXABAY_KEY: return []
    out=[]
    try:
        r = requests.get("https://pixabay.com/api/", params={"key":PIXABAY_KEY,"q":query,"per_page":per_page,"orientation":"vertical","safesearch":"true"}, timeout=TIMEOUT)
        if r.ok:
            for h in r.json().get("hits", []):
                out.append({
                    "type":"image",
                    "url": h["largeImageURL"],
                    "author": h.get("user",""),
                    "page": h.get("pageURL",""),
                    "source": "Pixabay",
                    "license": "Pixabay License"
                })
        r2 = requests.get("https://pixabay.com/api/videos/", params={"key":PIXABAY_KEY,"q":query,"per_page":per_page,"safesearch":"true"}, timeout=TIMEOUT)
        if r2.ok:
            for h in r2.json().get("hits", []):
                vids = h.get("videos",{})
                # выбрать лучшее (в порядке preference)
                link = vids.get("large",{}).get("url") or vids.get("medium",{}).get("url") or vids.get("small",{}).get("url")
                if link:
                    out.append({
                        "type":"video",
                        "url": link,
                        "author": h.get("user",""),
                        "page": h.get("pageURL",""),
                        "source": "Pixabay",
                        "license": "Pixabay License"
                    })
    except Exception as e:
        print("PIXABAY error:", e)
    return out

def download(item):
    ext = ".mp4" if item["type"]=="video" else ".jpg"
    fname = f'{item["source"].lower()}_{abs(hash(item["url"]))}{ext}'
    path = os.path.join(ASSETS_BG, fname)
    if os.path.exists(path):
        return None
    try:
        with requests.get(item["url"], stream=True, timeout=TIMEOUT) as r:
            r.raise_for_status()
            with open(path, "wb") as f:
                for chunk in r.iter_content(65536):
                    if chunk: f.write(chunk)
        # sanity: small files иногда мусор
        if os.path.getsize(path) < 50_000:
            os.remove(path); return None
        write_license(path, item["source"], item["license"], item["author"], item["page"])
        print("Downloaded:", path)
        return path
    except Exception as e:
        print("Download failed:", e)
        try:
            if os.path.exists(path): os.remove(path)
        except: pass
        return None

def prune(limit):
    files = sorted([str(p) for p in pathlib.Path(ASSETS_BG).glob("*")], key=lambda p: os.path.getmtime(p))
    if len(files) <= limit: return
    to_del = len(files)-limit
    for p in files[:to_del]:
        try:
            os.remove(p)
            print("Pruned:", p)
        except: pass

def main():
    with open(QUERIES_FILE, "r", encoding="utf-8") as f:
        queries = [q.strip() for q in f if q.strip()]
    random.shuffle(queries)
    need = max(0, TARGET_BG_COUNT - len(list(pathlib.Path(ASSETS_BG).glob("*"))))
    target_fetch = min(need, 20) if need>0 else 6  # докачать если мало, иначе понемногу обновлять
    fetched = 0
    for q in queries:
        items = []
        items += fetch_pexels(q, per_page=3)
        items += fetch_pixabay(q, per_page=3)
        random.shuffle(items)
        for it in items:
            if fetched >= target_fetch: break
            if download(it): fetched += 1
        if fetched >= target_fetch: break
    prune(TARGET_BG_COUNT)
    print(f"Fetched {fetched} assets.")

if __name__ == "__main__":
    main()
