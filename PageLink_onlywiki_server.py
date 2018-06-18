from bs4 import BeautifulSoup
import re
import datetime
import time

start = time.time()
now = datetime.datetime.now()


# input --> result_file from wikiExtractor
# wiki articles, splitted by <doc id='' url='' title='' ></doc>
def open_wiki_files():
    with open(
            '/home/daniela/wiki_pagelinks_2016-10/wikipedia20180401/wikiextractor/result_wikiextractor_1/AA/wiki_00') as wiki_f:
        wiki_files = wiki_f.read()
        soup = BeautifulSoup(wiki_files, "html.parser")
        articles = soup.find_all('doc')
    return articles


file = open(
    '/home/daniela/wiki_pagelinks_2016-10/wikipedia20180401/wikiextractor/result/wikiresult_' + str(now.month) + str(
        now.day), "w+")


def write_file(title, entity, sentence):
    title = title.replace(' ', '_')
    entity = entity.replace(' ', '_')
    file.write(
        '<https://en.wikipedia.org/wiki?' + title + '> ' + '<https://en.wikipedia.org/wiki?' + entity + '> ' + '\"' + sentence + '\" \n')


def extract_header(article):
    re_article_header = re.search(r'<doc .*?>', article)
    article_header = re_article_header.group()

    re_article_url = re.search(r'url="(.*?)"', article)
    article_url = re_article_url.group()
    url = article_url.split('"')
    return article_header


def extract_title(article):
    re_article_title = re.search(r'title=".*?"', article)
    article_title = re_article_title.group()
    title = article_title.split('"')
    return title[1]


def extract_entity(element):
    element = str(element)
    link = element.replace('>', '<').split('<')
    if link[2]:
        link = link[2]
    else:
        link = 'NO ENTITY'
    return link


def extract_sentence(entity, article):
    re_sentence = re.search(r'([^.]*>%s<.*?\.)(?!\d)' % entity, article) # added those >< around the entity, otherwise it doesn't extract the entity literately  stateless vs state
    if not re_sentence:
        sentence = 'NO SENTENCE FOUND'
    else:
        sentence = re_sentence.group()
        if '<' in sentence:
            sentence_link = re.findall(r'<a href=.*?</a>', sentence)
            for link_element in sentence_link:
                link_entity = link_element.replace('>', '<').split('<')
                sentence = sentence.replace(link_element, link_entity[2])
        sentence = sentence.replace('\n', '')
    return sentence


articles = open_wiki_files()
for article in articles:
    article = str(article)
    header = extract_header(article)
    title = extract_title(article)
    article = article.replace(header, '').replace(title, '', 1)
    re_links = re.findall(r'<a href=.*?</a>', article)
    print('Article: {} has {} links'.format(title, len(re_links)))
    for element in re_links:
        entity = extract_entity(element)
        sentence = extract_sentence(entity, article)
        write_file(title, entity, sentence)

end = time.time()
print('--- TIME {}'.format(end - start))
