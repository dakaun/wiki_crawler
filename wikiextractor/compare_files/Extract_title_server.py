from bs4 import BeautifulSoup
import re

#TODO reduce RAM used with beautiful soap
# iterate through all articles
# get title of those articles
# which contain redirect
# and preview page

# open wiki files and split into articles
def open_wiki_files():
    article_list = []
    with open(
            '/home/daniela/wikipedia20180401/enwiki-20180401-pages-articles-multistream_1.xml') as wiki_f:
        wiki_file_line = wiki_f.readline()
        while (wiki_file_line):
            article += wiki_file_line
            if '</doc>' in wiki_file_line:
                article_list.append(article)
                article = ""
            wiki_file_line = wiki_f.readline()
    return article_list

def get_titles():
    wiki_articles = open_wiki_files()
    redirect_titles = []
    preview_titles = []
    redirect2_titles = []

    for article in wiki_articles:
        if '<text xml:space="preserve">#REDIRECT [[' in article:
            redirect_title = article.contents[1].text
            redirect_titles.append(redirect_title)
        if '<redirect title=' in article:
            redirect2_title = article.contents[1].text
            redirect2_titles.append(redirect2_title)
        re_preview = re.search(r'>.*?may refer to', article)
        if re_preview:
            preview = re_preview.group()
            if preview in article:
                preview_title = article.contents[1].text
                preview_titles.append(preview_title)

    redirect_titles_set = set(redirect_titles)
    #redirect_titles_length = len(redirect_titles)
    preview_titles_set = set(preview_titles)
    redirect2_titles_set = set(redirect2_titles)
    #preview_titles_length = len(preview_titles)
    #titles = redirect_titles_set | preview_titles_set
    return redirect_titles_set, preview_titles_set, redirect2_titles_set

