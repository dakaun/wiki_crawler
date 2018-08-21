import re
import datetime
import time
from nltk.tokenize import sent_tokenize
import nltk

# this script extracts all links and the according sentences from the wikidump files (after parsing with WikiExtractor.py
# input: parsed wiki file
# output: result file with triples like: subject as article name, predicate as entity, object as the according sentence

amount_articles = 0

# input --> result_file from wikiExtractor
# wiki articles, splitted by <doc id='' url='' title='' ></doc>
def open_wiki_files(INPUT_PATH):
    article_list = []
    article = ""
    with open(INPUT_PATH) as wiki_f:
        wiki_file_line = wiki_f.readline()
        while (wiki_file_line):
            article += wiki_file_line
            if '</doc>' in wiki_file_line:
                article_list.append(article)
                article = ""
            wiki_file_line = wiki_f.readline()
    return article_list, len(article_list)

def write_file(title, entity, sentence, file):
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


def extract_sentence(sentence):
    sentence_link = re.findall(r'<a href=.*?</a>', sentence)
    for link_element in sentence_link:
        link_entity = link_element.replace('>', '<').split('<')
        sentence = sentence.replace(link_element, link_entity[2])
    sentence = sentence.replace('\n', '')
    return sentence


def result_file(INPUT_PATH):
    start = time.time()
    # add e.g. as abbreviation to set
    extra_abbreviation = ['e.g', 'co', 'st', 'mr']
    sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentence_tokenizer._params.abbrev_types.update(extra_abbreviation)

    now = datetime.datetime.now()
    resulting_file= open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump/result' + str(now.month) + str(now.day) + '.txt', "w+")


    articles = open_wiki_files(INPUT_PATH)
    amount_articles =articles[1]
    for article in articles[0]:
        header = extract_header(article)
        title = extract_title(article)
        article = article.replace(header, '').replace(title, '', 1)
        re_links = re.findall(r'<a href=.*?</a>', article)
        print('Article: {} has {} links'.format(title, len(re_links)))
        article_in_sentences = sent_tokenize(article)  # find all sentences
        for link in re_links:
            for raw_sentence in article_in_sentences:
                if link in raw_sentence:
                    sentence = extract_sentence(raw_sentence)
                    entity = extract_entity(link)
                    write_file(title, entity, sentence, resulting_file)
                    break

    end = time.time()
    print('AMOUNT OF ARTICLES {}'.format(amount_articles))
    print('--- TIME {}'.format(end - start))


