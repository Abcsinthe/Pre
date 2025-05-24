import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_imdb_comments(movie_id, max_comments=300, output_file='imdb_comments.csv'):
    url_template = f"https://www.imdb.com/title/{movie_id}/reviews?sort=helpfulnessScore&dir=desc&ratingFilter=0"
    headers = {"User-Agent": "Mozilla/5.0"}
    comments = []
    start = 0

    while len(comments) < max_comments:
        url = url_template + (f"&start={start}" if start > 0 else "")
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')

        comment_tags = soup.select('.ipc-html-content-inner-div[role="presentation"]')
        if not comment_tags:
            print("没有更多评论了。")
            break

        for tag in comment_tags:
            if len(comments) >= max_comments:
                break
            content = tag.get_text(strip=True)
            comments.append({'content': content})

        start += 25
        time.sleep(1)

    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['content'])
        writer.writeheader()
        writer.writerows(comments)
    print(f"已保存{len(comments)}条评论到 {output_file}")

if __name__ == "__main__":
    movie_id = "tt1684562"  # 替换为你的电影ID
    scrape_imdb_comments(movie_id)