import re
import requests
from bs4 import BeautifulSoup

#adapting tripe_object for regex
def enhance_entity(triple_object):
    triple_object = triple_object.replace('_', ' ')
    triple_object = triple_object.replace('(', '\(')
    triple_object = triple_object.replace(')', '\)')
    return triple_object

#enhancing wiki_file - remove all links, references, title
def enhance_wikifile(wiki_file):
    re_remove = re.findall(r"\&lt\;ref.*?\&lt\;/ref\&gt\;", wiki_file, re.IGNORECASE)
    for element in re_remove:
        wiki_file = wiki_file.replace(element, '')
    return wiki_file

# open file of wikipedia article and extract sentence
def extract_sentence(triple_object):
    with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/Cyrano_de_Bergerac.xml',
              encoding='cp65001') as wiki_f:
        wiki_file = wiki_f.read()

        #enhance_entity(triple_object)
        triple_object = triple_object.replace('_', ' ')
        triple_object = triple_object.replace('(', '\(')
        triple_object = triple_object.replace(')', '\)')

        #enhance_wikifile(wiki_file)
        #<ref></ref>
        re_links = re.findall(r"\&lt\;ref.*?\&lt\;/ref\&gt\;", wiki_file, re.IGNORECASE) #TODO modify
        for element in re_links:
            wiki_file = wiki_file.replace(element, '')
        #{{refn|}}
        re_reference = re.findall(r"\{\{refn\|.*?\}\}", wiki_file, re.IGNORECASE) #TODO modify to {{refn|as{{sk}}sl}}
        for element in re_reference:
            wiki_file = wiki_file.replace(element, '')
        #====heading====
        re_heading = re.findall(r"={2,4}.*?={2,4}", wiki_file, re.IGNORECASE)
        for element in re_heading:
            wiki_file = wiki_file.replace(element, '')

        #search only where line does not start with |
        re_match = re.search(r'([^.]*\[\[' + triple_object + '[^.]*\.)', wiki_file, #(\#.+)?(\|.+)?\]\]
                            re.IGNORECASE)  

    if not re_match:
        sentence = 'NO SENTENCE FOUND'
    else:
        sentence = re_match.group()
        sentence = sentence.replace('\n', ' ')
        print('### Sentence with containing object: \n{}'.format(sentence))
    return sentence


file = open("file_result_split_period_advanced.txt", "w+", encoding='cp65001')

# write triple to file 'file_result.txt
def write_file(ttl_triple, sentence, i):
    file.write(ttl_triple[i-2] +' '+ ttl_triple[i] +' \"'+ sentence +'\"\n')
    print('### Successfully wrote to File')

# open file of links
with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/Cyrano_links.ttl', encoding='cp65001') as ttl_f:
    ttl_file = ttl_f.read()

    # spliting each triples of ttl file in subj, pred, obj
    ttl_triple = ttl_file.split(" ")

    # extracting the object and extracting sentence from file
    i = 2
    for line in ttl_file:
        print('### Iterating through ttf_file with index: {}'.format(i))
        triple_object = ttl_triple[i].split('/')[4][:-1]
        print('### Tripple Object: \n{}'.format(triple_object))
        if triple_object:
            sentence = extract_sentence(triple_object)
        else:
            print("No Triple Object")
        if sentence:
            write_file(ttl_triple, sentence, i)
        else:
            print('No sentence')
        i += 3

# NOT USING: extracting sentence from wikipedia
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

