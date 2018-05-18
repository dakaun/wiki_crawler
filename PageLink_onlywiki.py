from bs4 import BeautifulSoup
import re
import datetime

now = datetime.datetime.now()

# input --> result_file from wikiExtractor
# wiki articles, splitted by <doc id='' url='' title='' ></doc>
def open_wiki_files():
    with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_extractor.txt',
              encoding='cp65001') as wiki_f:
        wiki_files = wiki_f.read()
        soup = BeautifulSoup(wiki_files, "html.parser")
        articles = soup.find_all('doc')
    return articles

file = open('result/result'+ str(now.month) + str(now.day) + ".txt", "w+", encoding='cp65001')
def write_file(article_url, entity, sentence):
    file.write('<' + article_url[1] + '> ' + '<https://en.wikipedia.org/wiki?' + entity + '> ' + '\"' + sentence + '\" \n')


def extract_header(article):
    re_article_header = re.search(r'<doc .*?>', article)
    article_header = re_article_header.group()

    re_article_url = re.search(r'url="(.*?)"', article)
    article_url = re_article_url.group()
    url = article_url.split('"')
    return url


def extract_entity(element):
    element = str(element)
    link = element.replace('>', '<').split('<')
    if link[2]:
        link = link[2]
    else:
        link = 'NO ENTITY'
    return link


def extract_sentence(entity, element, article):
    re_sentence = re.search(r'[^.]*' + entity + '[^.]*\.', article)
    if not re_sentence:
        sentence = 'NO SENTENCE FOUND'
    else:
        sentence = re_sentence.group()
        sentence = sentence.replace(element, entity).replace('\n', '')
    return sentence


articles = open_wiki_files()
for article in articles:
    article = str(article)
    url = extract_header(article)
    re_links = re.findall(r'<a href=.*?</a>', article)
    for element in re_links:
        entity = extract_entity(element)
        sentence = extract_sentence(entity, element, article)
        write_file(url, entity, sentence)
