import requests

def get_russian_quote():
    url = "https://quotes.rest/qod?language=ru"
    headers = {"Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        quote = data['contents']['quotes'][0]['quote']
        author = data['contents']['quotes'][0]['author']
        return f"{quote} — {author}"
    except Exception:
        # Запасная цитата, если API не ответил
        return "Жизнь — это то, что происходит, пока ты строишь планы. — Джон Леннон"
