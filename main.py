import requests
from bs4 import BeautifulSoup as BS
import json
from settings import BOARD


def get_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"error {url}: {e}")
        return None


def parse_soup(response):
    soup = BS(response.text, 'lxml')
    posts = soup.find_all(class_='thread')
    return posts


def process_post(post):
    post_id = post.get('id').split('-')[1]
    text = post.find('article', class_="post__message post__message_op").text.strip()
    img_link = post.find('a', class_='post__image-link').get('href')
    img_url = 'https://2ch.hk' + img_link if img_link else None
    return post_id, text, img_url


def save_data(data):
    with open('threads.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main(url):
    response = get_response(url)
    if response is None:
        return

    posts = parse_soup(response)

    data = {}
    for index, post in enumerate(posts):
        if index in (1, 2):
            continue

        post_id, text, img_url = process_post(post)

        data[post_id] = {
            'img': img_url,
            'text': text
        }

    save_data(data)


if __name__ == '__main__':
    main('https://2ch.hk/' + BOARD)
