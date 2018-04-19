import re
import requests
from bs4 import BeautifulSoup


# def file_handling(wiki_file, triple_object): #TODO
#     #if object = file     #then extract sentence    #otherwise replace file with ''
#     if triple_object in re_file:
#         sentence = re_file
#     else:
#         sentence = ''
#         for element_file in re_file:
#             wiki_file = wiki_file.replace(element_file, '')
#     return sentence, wiki_file


def open_wiki_file():
    with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/Cyrano_de_Bergerac.xml',
              encoding='cp65001') as wiki_f:
        wiki_file = wiki_f.read()
        # enhance_wikifile
        # <ref></ref>
        re_links = re.findall(r"\&lt\;ref.*?\&lt\;/ref\&gt\;", wiki_file, re.IGNORECASE)
        for element_links in re_links:
            wiki_file = wiki_file.replace(element_links, '')
        print('§§§ re_links with ref: {}'.format(re_links))
        # {{refn|}}
        re_reference = re.findall(r"\{\{refn\|.*?\}\}", wiki_file, re.IGNORECASE)
        for element_reference in re_reference:
            wiki_file = wiki_file.replace(element_reference, '')
        print('§§§ re_reference with refn: {}'.format(re_reference))
        # ====heading====
        re_heading = re.findall(r"={2,}.*?={2,}", wiki_file, re.IGNORECASE)  # removed upper limit --> still working?
        for element_heading in re_heading:
            wiki_file = wiki_file.replace(element_heading, '')
        print('§§§ re_heading with ==header==: {}'.format(re_heading))
        # "<!--[^-]*-->"
        re_notes = re.findall(r"&lt;!--[^-]*--&gt;", wiki_file)
        # re_notes = re.findall(r"<!--[^-]*-->", wiki_file) #???????
        for element_notes in re_notes:
            wiki_file = wiki_file.replace(element_notes, '')
        print('§§§ re_notes with <!--: {}'.format(re_notes))
        # # file
        re_file = re.findall(r'\[\[File:[^]]+\]\]', wiki_file)
        # for element_file in re_file:
        #    wiki_file = wiki_file.replace(element_file, '')
        print('§§§ re_files as File {}'.format(re_file))
        # infobox
        re_info = re.findall(r'(\{\{Infobox.*?(\{\{.*?\}\}.*?)*}})', wiki_file, re.DOTALL)
        wiki_file = wiki_file.replace(re_info[0][0], '.')
        print('§§§ re_info with Infobox: {}'.format(re_info))
        # quote
        wiki_file = wiki_file.replace("&quot;", "\"")
        return wiki_file


# open file of wikipedia article and extract sentence
def extract_sentence(triple_object, wiki_file):
    # enhance_entity
    triple_object = triple_object.replace('_', ' ')
    triple_object = triple_object.replace('(', '\(')
    triple_object = triple_object.replace(')', '\)')

    # exctract sentence with entity
    re_match = re.search(r'([^.]*\[\[' + triple_object + '[^.]*\.)', wiki_file,  # (\#.+)?(\|.+)?\]\]
                         re.IGNORECASE)
    print(re_match)
    if not re_match:
        sentence = 'NO SENTENCE FOUND'
    else:
        sentence = re_match.group()
        sentence = sentence.replace('\n', ' ')
        print('### Sentence with containing object: \n{}'.format(sentence))
    return sentence


# resulting file
file = open("file_result_split_period_advanced1804a.txt", "w+", encoding='cp65001')


# write triple to file 'file_result.txt
def write_file(ttl_triple, sentence, i):
    file.write(ttl_triple[i - 2] + ' ' + ttl_triple[i] + ' \"' + sentence + '\"')
    print('### Successfully wrote to File')


# open file of links
with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/Cyrano_links.ttl',
          encoding='cp65001') as ttl_f:
    ttl_file = ttl_f.read()

    # spliting each triples of ttl file in subj, pred, obj
    ttl_triple = ttl_file.split(" ")
    # get wikifile
    from_wiki_file = open_wiki_file()

    # extracting the object and extracting sentence from file
    i = 65 #2
    for line in ttl_file:
        print('### Iterating through ttf_file with index: {}'.format(i))
        triple_object = ttl_triple[i].split('/')[4][:-1]
        print('### Tripple Object: \n{}'.format(triple_object))
        if triple_object:
            sentence = extract_sentence(triple_object, from_wiki_file)
        else:
            print("No Triple Object")
        if sentence:
            write_file(ttl_triple, sentence, i)
        else:
            print('No sentence')
        i += 3
