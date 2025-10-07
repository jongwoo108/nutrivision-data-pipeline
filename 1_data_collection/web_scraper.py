import requests, os
from bs4 import BeautifulSoup

def crawl_images(query="과자 영양정보", limit=50):
    url = f"https://www.google.com/search?tbm-isch&q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    
    os.makedirs("assets/raw_images", exist_ok=True)
    count = 0
    for img in soup.select("img"):
        src = img.get("src")
        if src and src.startswith("http"):
            with open(f"assets/raw_images/img_{count}.jpg", "wb") as f:
                f.write(requests.get(src).content)
            count += 1
            if count >= limit: break

if __name__== "__main__":
    crawl_images("식품 영양정보 라벨")