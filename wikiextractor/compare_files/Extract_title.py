from bs4 import BeautifulSoup
import re

# iterate through all articles
# get title of those articles
# which contain redirect
# and preview page

# open wiki files and split into articles
def open_wiki_files():
    with open(
            'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/compare_title/extract title/wiki_pages(redirect_preview).txt',encoding='cp65001') as wiki_f:
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
    #print(redirect_titles)
    #print(preview_titles)
    redirect_titles_set = set(redirect_titles)
    preview_titles_set = set(preview_titles)
    titles = redirect_titles_set | preview_titles_set
    #print(titles)
    return titles
