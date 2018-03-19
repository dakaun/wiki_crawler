import re
import requests
from bs4 import BeautifulSoup

triple_object = []
ttl_triple = []

# open file of wikipedia article and extract sentence
def extract_sentence(triple_object):
    with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/Cyrano_de_Bergerac_modified.xml',
              encoding='cp65001') as wiki_f:
        # ENCODING: cp437, cp850, cp852, cp858, cp1250, cp65001 !, latin_1, iso8859_2, iso8859_15
        wiki_file = wiki_f.read()
        re_match = re.search(r'([^.]*\[\[' + triple_object + '\]\][^.]*\.)', wiki_file,
                            re.IGNORECASE)  # TODO adapting regex to sentence strucutre
        sentence = re_match.group()
        print('### Sentence with containing object: \n{}'.format(sentence))

# open file of links
with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/Cyrano_links.ttl') as ttl_f:
    ttl_file = ttl_f.read()
    # print(ttl_file)
    # print(f.readlines())

    # spliting each triples of ttl file in subj, pred, obj
    ttl_triple = ttl_file.split(" ")
    # print('1' + ttl_triple[0])     print('2' + ttl_triple[1])     print('3' + ttl_triple[2])

    # extracting the object and extracting sentence from file
    i = 2
    # for ttl_triple in ttl_file:
    while i <= 11:
        print('### Iterating through ttf_file with index: {}'.format(i))
        triple_object = ttl_triple[i].split('/')[4][:-1]
        print('### Tripple Object: \n{}'.format(triple_object))
        extract_sentence(triple_object)
        i += 3

# extracting sentence from wikipedia
def extract_wiki(url):
    # url = "https://en.wikipedia.org/wiki/Cyrano_de_Bergerac"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")
    for element in content_div.find_all('p', recursive=False):
        for child_element in element.find_all(title='Sannois', recursive=False, href=True):
            print(element)
            print(re.search(r"[^.]*Sannois[^.]*\.",
                            str(element)))  # alternative no regex, split(".") + if 'sannois' in element; RE
# extract_wiki("https://en.wikipedia.org/wiki/Cyrano_de_Bergerac")

# TODO creating file
