from xml.etree import ElementTree
import os
import feedparser
import requests
import shutil
from bs4 import BeautifulSoup
from bs4.element import Comment

from dublicates.consts import ARTICLE_FILE_PREFIX


def tag_visible(element):
    if element.parent.name in \
            ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def fetch_articles(urls_filename, output_dir, articles_limit=None):
    if os.path.exists(output_dir):
        shutil.rmtree(os.path.join(output_dir))

    os.makedirs(output_dir)

    e = ElementTree.parse(urls_filename).getroot()

    for url in e.findall('url'):
        d = feedparser.parse(url.text)
        articles_num = len(d['entries']) if articles_limit is None \
            else min(len(d['entries']), articles_limit)
        for i in range(articles_num):
            entry = d['entries'][i]
            resp = requests.get(entry['link'])

            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, 'html.parser')
                article_texts = soup.html.findAll(text=True)
                visible_text = " ".join(t.strip() for t in
                                        filter(tag_visible, article_texts))

                filename = os.path.join(output_dir, '{}{}'.format(
                    ARTICLE_FILE_PREFIX, i))
                with open(filename, 'a') as f:
                    f.write(entry['link'] + '\n')
                    f.write(visible_text)
