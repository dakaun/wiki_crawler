import re
import time

start = time.time()

def open_wiki_file():
    with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/Cyrano_de_Bergerac.xml',
              encoding='cp65001') as wiki_f:
        xml_page = wiki_f.read()
        # enhance_wikifile
        # <ref></ref>
        re_links = re.findall(r"\&lt\;ref.*?/\&gt\;|\&lt\;ref.*?\&lt\;/ref\&gt\;", xml_page, re.IGNORECASE)
        for element_links in re_links:
            xml_page = xml_page.replace(element_links, '')
        print('§§§ re_links with ref: {}'.format(re_links))
        # {{refn|}}
        re_reference = re.findall(r"\{\{refn\|.*?\}\}", xml_page, re.IGNORECASE)
        for element_reference in re_reference:
            xml_page = xml_page.replace(element_reference, '')
        print('§§§ re_reference with refn: {}'.format(re_reference))
        # ====heading====
        re_heading = re.findall(r"={2,}.*?={2,}", xml_page, re.IGNORECASE)  # removed upper limit --> still working?
        for element_heading in re_heading:
            xml_page = xml_page.replace(element_heading, '')
        print('§§§ re_heading with ==header==: {}'.format(re_heading))
        # "<!--[^-]*-->"
        re_notes = re.findall(r"&lt;!--[^-]*--&gt;", xml_page)
        # re_notes = re.findall(r"<!--[^-]*-->", xml_page) #???????
        for element_notes in re_notes:
            xml_page = xml_page.replace(element_notes, '')
        print('§§§ re_notes with <!--: {}'.format(re_notes))
        # # file
        re_file = re.findall(r'\[\[File:[^]]+\]\]', xml_page)
        for element_file in re_file:
            xml_page = xml_page.replace(element_file, '')
        print('§§§ re_files as File {}'.format(re_file))
        # infobox
        re_info = re.findall(r'(\{\{Infobox.*?(\{\{.*?\}\}.*?)*}})', xml_page, re.DOTALL)
        xml_page = xml_page.replace(re_info[0][0], '.')
        print('§§§ re_info with Infobox: {}'.format(re_info))
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
        print('### Sentence with containing object: \n{}'.format(sentence))
    return sentence


# resulting file
file = open("result/file_result_split_period_advanced1105.txt", "w+", encoding='cp65001')


# write triple to file 'file_result.txt
def write_file(ttl_triple, sentence):
    file.write(ttl_triple[0] + ' ' + ttl_triple[2] + ' \"' + sentence + '\" \n')
    print('### Successfully wrote to File')


# open file of links
with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/Cyrano_links.ttl',
          encoding='cp65001') as ttl_f:
    ttl_file = ttl_f.readlines()
    # get wikifile
    wiki_pages = open_wiki_file()
    # extracting the object and extracting sentence from file
    for line in ttl_file:
        print('### LINE: {} '.format(line))
        ttl_triple = line.split(" ")    # spliting each triples of ttl file in subj, pred, obj
        triple_object = ttl_triple[2].split('/')[4][:-1]
        print('### Tripple Object: \n{}'.format(triple_object))
        if triple_object:
            sentence = extract_sentence(triple_object, wiki_pages)
        else:
            print("No Triple Object")
        if sentence:
            write_file(ttl_triple, sentence)
        else:
            print('No sentence')
        #i += 3

end = time.time()
print('### TIME {}'.format(end-start))
