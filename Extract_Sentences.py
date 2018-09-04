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
    with open(INPUT_PATH) as wiki_f: #, encoding='cp65001'
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
            '<http://dbpedia.org/resource/' + title + '> ' + '<http://dbpedia.org/resource/' + entity + '> ' + '\"' + sentence + '\" \n')


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


def extract_sentence(sentence, link):
    final_sentence = ""
    sentence_link = re.findall(r'<a href=.*?</a>', sentence)
    entity_link = link.replace('>', '<').split('<')[2]
    for link_element in sentence_link:
        link_entity = link_element.replace('>', '<').split('<')[2]
        sentence = sentence.replace(link_element, link_entity)
    sentence = sentence.replace(entity_link, '[[' + entity_link + ']]')
    sentence = sentence.replace('\n', '')
    return sentence


def result_file(path):
    '''
    splits file into its articles and safes into a list (def open_wiki_files()). Afterwards the articles are split into
    its sentences via nltk library (https://www.nltk.org/) and all links in the articles are extracted via regex.
    Finally the sentences with the links are extracted and saved into the result_file
    :param path: array of input and output directory
    :return: a file with all sentences which contain a link. The sentences are saved in triples:
    the article link as subject, the link (entity) as predicate, and the sentence which contained the entity as object
    e.g. <http://dbpedia.org/resource/Cyrano_de_Bergerac> <http://dbpedia.org/resource/Sannois> "He died over a year
    later on July 28, 1655, aged 36, at the house of his cousin, Pierre De Cyrano, in [[Sannois]]."
    '''
    INPUT_PATH = path[0]
    resulting_path = path[1]
    start = time.time()
    # add e.g. as abbreviation to set
    extra_abbreviation = ['e.g', 'co', 'st', 'mr']
    sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentence_tokenizer._params.abbrev_types.update(extra_abbreviation)

    now = datetime.datetime.now()
    resulting_file= open(resulting_path+ '/res' + str(now.month) + str(now.day) + '.txt', "w+")


    articles = open_wiki_files(INPUT_PATH)
    amount_articles =articles[1]
    for article in articles[0]:
        header = extract_header(article)
        title = extract_title(article)
        article = article.replace(header, '').replace(title, '', 1)
        re_links = re.findall(r'<a href=.*?</a>', article)
        #print('Article: {} has {} links'.format(title, len(re_links)))
        article_in_sentences = sent_tokenize(article)  # find all sentences
        for link in re_links:
            for raw_sentence in article_in_sentences:
                if link in raw_sentence:
                    sentence = extract_sentence(raw_sentence, link)
                    entity = extract_entity(link)
                    write_file(title, entity, sentence, resulting_file)
                    break

    end = time.time()

    print('AMOUNT OF ARTICLES {}'.format(amount_articles))
    print('--- TIME {}'.format(end - start))


