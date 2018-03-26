from dublicates import dump_similarities
from dublicates import fetch_articles
from dublicates import get_similarities


def rss_get_similarity(urls_filename, articles_dir, articles_limit=None):
    fetch_articles(urls_filename, articles_dir, articles_limit=articles_limit)
    return get_similarities(articles_dir, articles_limit=articles_limit)


def rss_dumb_similarity(urls_filename, articles_dir,
                        output_filename, articles_limit=None):
    fetch_articles(urls_filename, articles_dir,
                   articles_limit=articles_limit)

    return dump_similarities(articles_dir, output_filename,
                             articles_limit=articles_limit)
