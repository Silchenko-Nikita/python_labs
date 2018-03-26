import dublicates
from dublicates import dump_similarities
from dublicates import fetch_articles

if __name__ == "__main__":
    urls_filename = 'urls.xml'
    articles_dir = 'articles'
    output_filename = 'similarities.xml'

    # dublicates.rss_dumb_similarity('urls.xml', 'articles', 'similarities.xml', articles_limit=10)

    # fetch_articles(urls_filename, articles_dir)
    dump_similarities(articles_dir, output_filename, articles_limit=14)
