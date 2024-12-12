import os
import sys
import requests
import re
from bs4 import BeautifulSoup  # type: ignore


def get_page():
    url = input('Enter the URL of a Medium article: ')
    if not re.match(r'https?://medium.com/', url):
        print('Please enter a valid Medium article URL.')
        sys.exit(1)
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Error fetching the page: {e}')
        sys.exit(1)
    return BeautifulSoup(res.text, 'html.parser')


def purify(text):
    replacements = {"<br>": "\n", "<br/>": "\n", "<li>": "\n"}
    pattern = re.compile("|".join(map(re.escape, replacements)))
    text = pattern.sub(lambda m: replacements[m.group(0)], text)
    text = re.sub(r'<[^>]*>', '', text)
    return text


def collect_text(soup):
    title = soup.head.title.text.split('|')[0].strip()
    fin = f'URL: {soup.head.title.text.split("|")[1].strip()}\n\nTitle: {title.upper()}\n\n'

    headers = soup.find_all('h1')
    for header in headers:
        fin += f'\n\n{header.text.upper()}\n'
        for elem in header.next_siblings:
            if elem.name == 'h1':
                break
            fin += f'{purify(str(elem))}\n'
    return title, fin


def save_file(title, fin):
    directory = './scraped_articles'
    os.makedirs(directory, exist_ok=True)
    fname = os.path.join(directory, '_'.join(title.split()) + '.txt')
    with open(fname, 'w', encoding='utf8') as outfile:
        outfile.write(fin)
    print(f'File saved in directory {fname}')


if __name__ == '__main__':
    soup = get_page()
    title, fin = collect_text(soup)
    save_file(title, fin)
