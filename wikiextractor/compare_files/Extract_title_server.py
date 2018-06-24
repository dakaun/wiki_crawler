from bs4 import BeautifulSoup
import re

#TODO reduce RAM used with beautiful soap
# iterate through all articles
# get title of those articles
# which contain redirect
# and preview page

# open wiki files and split into articles
def open_wiki_files():
    with open(
            '/home/daniela/wikipedia20180401/enwiki-20180401-pages-articles-multistream_1.xml') as wiki_f:
        wiki_files = wiki_f.read()
        soup = BeautifulSoup(wiki_files, "html.parser")
        articles = soup.find_all('page')
    return articles

def get_titles():
    wiki_articles = open_wiki_files()
    redirect_titles = []
    preview_titles = []

    for article in wiki_articles:
        if '>#REDIRECT' in str(article):
            redirect_title = article.contents[1].text
            redirect_titles.append(redirect_title)
        re_preview = re.search(r'>.*?may refer to', str(article))
        if re_preview:
            preview = re_preview.group()
            if preview in str(article):
                preview_title = article.contents[1].text
                preview_titles.append(preview_title)

    redirect_titles_set = set(redirect_titles)
    preview_titles_set = set(preview_titles)
    titles = redirect_titles_set | preview_titles_set
    return titles

