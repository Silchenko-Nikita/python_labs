import os
import glob

import itertools
from urllib.parse import urlsplit
from xml.dom import minidom

from dublicates.consts import ARTICLE_FILE_PREFIX
from dublicates.shingle import get_shingles_similarity, get_shingles, canonize
from xml.etree import cElementTree as ET


def get_domain(url):
    return "{0.scheme}://{0.netloc}/".format(urlsplit(url))


def get_similarities(input_dir, articles_limit=None):
    filenames_pattern = os.path.join(input_dir,
                                     '{}*'.format(ARTICLE_FILE_PREFIX))
    articles_filenames = glob.glob(filenames_pattern)

    articles_num = len(articles_filenames)\
        if articles_limit is None else min(len(articles_filenames),
                                           articles_limit)
    articles_shingles = []

    for i in range(articles_num):
        with open(articles_filenames[i]) as f:
            article_url = f.readline().rstrip('\n')
            article_text = f.read()

            articles_shingles.append(
                {'url': article_url,
                 'shingles': get_shingles(canonize(article_text))})

    results = []
    for i, j in itertools.combinations(range(0, articles_num), 2):
        article1 = articles_shingles[i]
        article2 = articles_shingles[j]

        similarity = get_shingles_similarity(article1['shingles'],
                                             article2['shingles'])
        results.append({'url1': article1['url'],
                        'url2': article2['url'], 'similarity': similarity})

    results.sort(key=lambda x: (get_domain(x['url1'])
                                == get_domain(x['url2']), -x['similarity']))
    return results


def dump_similarities(input_dir, output_filename, articles_limit=None):
    results = get_similarities(input_dir, articles_limit=articles_limit)

    root = ET.Element('similarities')
    for result in results:
        articles = ET.SubElement(root, 'articles')
        ET.SubElement(articles, 'url1').text = result['url1']
        ET.SubElement(articles, 'url2').text = result['url2']
        ET.SubElement(articles, 'similarity').text = str(result['similarity'])

    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    with open(output_filename, "w") as f:
        f.write(xmlstr)
