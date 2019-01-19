import re
import datetime
import time
from nltk.tokenize import sent_tokenize
import nltk
import urllib
import pandas as pd

# this script extracts all links and the according sentences from the wikidump files (after parsing with WikiExtractor.py
# input: parsed wiki file
# output: result file with triples like: subject as article name, predicate as entity, object as the according sentence

amount_articles = 0

# input --> result_file from wikiExtractor
# wiki articles, splitted by <doc id='' url='' title='' ></doc>
def open_wiki_files(INPUT_PATH):
    article_list = []
    article = ""
    with open(INPUT_PATH, encoding='cp65001') as wiki_f: #, encoding='cp65001'
        wiki_file_line = wiki_f.readline()
        while (wiki_file_line):
            article += wiki_file_line
            if '</doc>' in wiki_file_line:
                article_list.append(article)
                article = ""
            wiki_file_line = wiki_f.readline()
    return article_list, len(article_list)

def write_file(title, entity, sentence, df):
    title = title.replace(' ', '_')
    entity = entity.replace(' ', '_')
    #file.write(
    #        '<http://dbpedia.org/resource/' + title + '> ' + '<http://dbpedia.org/resource/' + entity + '> ' + '\"' + sentence + '\" \n')
    article_title = '<http://dbpedia.org/resource/' + title + '> '
    link = '<http://dbpedia.org/resource/' + entity + '> '
    whole_sentence = '\"' + sentence + '\"'
    df = df.append({'article_title': article_title, 'link': link, 'sentence': whole_sentence}, ignore_index=True)


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


def parse_entity(entity):
    entity = urllib.parse.unquote(entity)
    entity = entity.replace('&amp;', '&')
    return entity


def extract_sentence(sentence):
    '''
    This function replaces the links with its entity and gives back two lists: one containing the entities for the
    resulting triple and the other list containing the matching sentence.
    :param sentence: the raw sentence containing the raw links indicated by <a href= >
    :return: one list containing the entities of the sentence, the other list containing the sentence with the according
    entity in brackets
    '''
    sentence = sentence.replace('\n', '')
    sentence_list = []
    entity_list = []
    sentence_link = re.findall(r'<a href=.*?</a>', sentence)
    for link_element in sentence_link:
        # extract entity from links and replace every entity in the sentence
        link_entity = link_element.replace('>', '<').split('<')[2]
        sentence = sentence.replace(link_element, link_entity)
    for link_element in sentence_link:
        # mark iteratively each entity in the sentence as entity and save sentence + entity
        link_entity_obj = link_element.replace('>', '<').split('<')[2]
        sentence_entity = sentence.replace(link_entity_obj, '[[' + link_entity_obj + ']]')
        link_entity_pred = link_element.split('"')[1]  # <--------------
        link_entity_pred = parse_entity(link_entity_pred)  # <--------------
        sentence_list.append(sentence_entity)
        entity_list.append(link_entity_pred)
    return entity_list, sentence_list


def result_file(path):
    '''
    splits file into its articles and safes into a list (def open_wiki_files()). By iterating through the articles
    first all links are extracted via regex and replaced (since often periods are in the links, it was a source of
    mistakes for splitting it into sentences). After splitting the article into its sentences via
    nltk library (https://www.nltk.org/), the wildcards for the links are replaced by the links again. Finally the
    according sentences and the including entities are extracted and saved into the result_file.
    :param path: array of input and output directory
    :return: a file with all sentences which contain a link. The sentences are saved in triples:
    the article link as subject, the link (entity) as predicate, and the sentence which contained the entity as object
    e.g. <http://dbpedia.org/resource/Cyrano_de_Bergerac> <http://dbpedia.org/resource/Sannois> "He died over a year
    later on July 28, 1655, aged 36, at the house of his cousin, Pierre De Cyrano, in [[Sannois]]."
    '''
    INPUT_PATH = path[0] # path to wiki_sum.txt
    resulting_path = path[1] # path to folder of wiki_sum.txt
    start = time.time()
    # add e.g. as abbreviation to set
    extra_abbreviation = ['e.g', 'co', 'st', 'mr']
    sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentence_tokenizer._params.abbrev_types.update(extra_abbreviation)

    now = datetime.datetime.now()
    #resulting_file= open(resulting_path+ '/res' + str(now.month) + str(now.day) + '.txt', "w+") #, encoding='cp65001'
    df = pd.DataFrame(columns={'article_title', 'link', 'sentence'})

    articles = open_wiki_files(INPUT_PATH)
    amount_articles =articles[1]
    for article in articles[0]:
        i = 0
        nb_entities = 0
        header = extract_header(article)
        title = extract_title(article)
        article = article.replace(header, '').replace(title, '', 1)
        re_links = re.findall(r'<a href=.*?</a>', article)
        for link in re_links:
            article = article.replace(link, '[[entity]]')
        article_in_sentences = sent_tokenize(article) # split into sentence with nltk library
        for raw_sentence in article_in_sentences:
            while '[[entity]]' in raw_sentence:
                raw_sentence = raw_sentence.replace('[[entity]]', re_links[i], 1)
                i+=1
            elements = extract_sentence(raw_sentence)
            nb_entities = len(elements[0])
            for e in range(nb_entities):
                write_file(title, elements[0][e], elements[1][e], df)


    df.to_csv(resulting_path + '/res' + str(now.month) + str(now.day) + '.csv', sep=';', index=False) # zu spät geschrieben
    end = time.time()

    print('AMOUNT OF ARTICLES {}'.format(amount_articles))
    print('--- TIME {}'.format(end - start))

if __name__ == '__main__':
    result_file([r'C:\Users\danielak\Desktop\Dokumente Daniela\UNI\FIZ\Second_Task\test_wiki_crawler\test_1801\AA\wiki_sum.txt', r'C:\Users\danielak\Desktop\Dokumente Daniela\UNI\FIZ\Second_Task\test_wiki_crawler\test_1801\AA'] )
