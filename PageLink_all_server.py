import re
import time
from bs4 import BeautifulSoup

start = time.time()

def open_wiki_file():
    with open('/home/daniela/wiki_pagelinks_2016-10/wikipedia20180401/wikipartfirst6000') as wiki_f: #encoding='cp65001'
        xml_file = wiki_f.read()
        soup = BeautifulSoup(xml_file, "html.parser")
        pages = soup.find_all('page')
    return pages

def enhance_xmlfile(xml_page):
    # enhance_wikifile
    # <ref></ref>
    re_links = re.findall(r"\&lt\;ref.*?\&lt\;/ref\&gt\;", xml_page, re.IGNORECASE)
    for element_links in re_links:
        xml_page = xml_page.replace(element_links, '')
    print('--- re_links with ref: {}'.format(re_links))
    # {{refn|}}
    re_reference = re.findall(r"\{\{refn\|.*?\}\}", xml_page, re.IGNORECASE)
    for element_reference in re_reference:
        xml_page = xml_page.replace(element_reference, '')
    print('--- re_reference with refn: {}'.format(re_reference))
    # ====heading====
    re_heading = re.findall(r"={2,}.*?={2,}", xml_page, re.IGNORECASE)  # removed upper limit --> still working?
    for element_heading in re_heading:
        xml_page = xml_page.replace(element_heading, '')
    print('--- re_heading with ==header==: {}'.format(re_heading))
    # "<!--[^-]*-->"
    re_notes = re.findall(r"&lt;!--[^-]*--&gt;", xml_page)
    # re_notes = re.findall(r"<!--[^-]*-->", xml_file) #???????
    for element_notes in re_notes:
        xml_page = xml_page.replace(element_notes, '')
    print('--- re_notes with <!--: {}'.format(re_notes))
    # # file
    re_file = re.findall(r'\[\[File:[^]]+\]\]', xml_page)
    for element_file in re_file:
        xml_page = xml_page.replace(element_file, '')
    print('--- re_files as File {}'.format(re_file))
    # infobox
    re_info = re.findall(r'(\{\{Infobox.*?(\{\{.*?\}\}.*?)*}})', xml_page, re.DOTALL)
    if re_info:
        xml_page = xml_page.replace(re_info[0][0], '.')
    print('--- re_info with Infobox: {}'.format(re_info))
    # quote
    xml_page = xml_page.replace("&quot;", "\"")
    return xml_page


# open file of wikipedia article and extract sentence
def extract_sentence(triple_object, page):
    # enhance_entity
    triple_object = triple_object.replace('_', ' ')
    triple_object = triple_object.replace('(', '\(')
    triple_object = triple_object.replace(')', '\)')
    triple_object = triple_object.replace('&', '&amp;')

    re_match = re.search(r'([^.]*\[\[' + triple_object + '[^.]*\.)', page,  # (\#.+)?(\|.+)?\]\]
                         re.IGNORECASE)
    if not re_match:
        sentence = 'NO SENTENCE FOUND'
    else:
        sentence = re_match.group()
        sentence = sentence.replace('\n', ' ')
        print('-- Sentence with containing object: \n{}'.format(sentence))
    return sentence


# resulting file
file = open("/home/daniela/wiki_pagelinks_2016-10/results/result_file1405", "w+") #, encoding='cp65001'


# write triple to file 'file_result.txt
def write_file(ttl_triple, sentence):
    file.write(ttl_triple[0] + ' ' + ttl_triple[2] + ' \"' + sentence + '\" \n')
    print('-- Successfully wrote to File')


def enhance_subject(triple_subject):
    triple_subject = triple_subject.replace('_', ' ')
    triple_subject = triple_subject.replace('&', '&amp;')
    return triple_subject


# open file of links
with open('/home/daniela/wiki_pagelinks_2016-10/page_links_en.ttl') as ttl_f: #encoding='cp65001'
    ttl_file = ttl_f.readlines()
    # get wikifile
    wiki_pages = open_wiki_file()
    previous_triple_subject = ""
    previous_page = ""
    # extracting the object and extracting sentence from file
    for line in ttl_file:  # iterate through every triple in the ttl_file
        if "<" in line:
            print('-- LINE: {} '.format(line))
            ttl_triple = line.split(" ")  # spliting each triples of ttl file in subj, pred, obj
            triple_subject = ttl_triple[0].split('/')[4][:-1]
            print('-- SUBJECT: {}'.format(triple_subject))
            triple_subject = enhance_subject(triple_subject)  # adapt triple_subject to match to the name of the article
            triple_object = ttl_triple[2].split('/')[4][:-1]
            print('-- Tripple Object: {}'.format(triple_object))
            if (previous_triple_subject == triple_subject):
                # if subject stays the same, then don't look for the same page again from the beginning, take the previous page
                sentence = extract_sentence(triple_object, previous_page)
                write_file(ttl_triple, sentence)
            else:
                previous_triple_subject = triple_subject
                for page in wiki_pages:  # iterate through all pages
                    if (triple_subject == page.title.string):  # if page with right title is found
                        # in right page - now extract sentences
                        page = str(page)
                        page = enhance_xmlfile(page)  # enhance page
                        previous_page = page
                        sentence = extract_sentence(triple_object, page)
                        write_file(ttl_triple, sentence)
                        break




end = time.time()
print('-- TIME {}'.format(end - start))
