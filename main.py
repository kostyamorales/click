import requests
from os import getenv
from urllib.parse import urlparse
import argparse
from dotenv import load_dotenv
load_dotenv()


def shorten_link(token, long_url):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {'Authorization': f'Bearer {token}'}
    body = {"long_url": f"{long_url}"}
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    answer = response.json()
    bitlink = answer['link']
    return bitlink


def count_clicks(token, link):
    parsed_link = urlparse(link)
    bitlink = parsed_link.netloc + parsed_link.path
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    answer = response.json()
    clicks_count = answer['total_clicks']
    return clicks_count


if __name__ == '__main__':

    token = getenv('TOKEN_BITLY')
    parser = argparse.ArgumentParser(
        description='Программа укорачивает ссылки или выводит количество переходов по уже укороченной ссылке'
    )
    parser.add_argument('link', help='ссылка')
    args = parser.parse_args()
    link = args.link

    if link.startswith('https://bit.ly/'):
        try:
            clicks_count = count_clicks(token, link)
        except requests.exceptions.HTTPError:
            print('Введена неправильная ссылка')
        print('Всего переходов по ссылке', clicks_count)
    else:
        try:
            bitlink = shorten_link(token, link)
        except requests.exceptions.HTTPError:
            print('Введена неправильная ссылка')
        print('Битлинк', bitlink)

