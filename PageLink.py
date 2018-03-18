import xml.etree.ElementTree as ET
import re
import requests
from bs4 import BeautifulSoup

triple_element = []
ttl_triple =[]


with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/Cyrano_links.ttl') as ttl_f:
    ttl_file = ttl_f.read()
    #print(ttl_file)
    #print(f.readlines())
    #spliting each triples of ttl file in subj, pred, obj
    ttl_triple = ttl_file.split(" ")
    print('1' + ttl_triple[0])
    print('2' + ttl_triple[1])
    print('3' + ttl_triple[2])

    #extracting the object for further research - object to extract the sentence from wikipedia
    triple_element = ttl_triple[2].split('/')
    print(triple_element[4][:-1]) #tripe without http content

#extracting sentence from wikipedia
url = "https://en.wikipedia.org/wiki/Cyrano_de_Bergerac"
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")
for element in content_div.find_all('p', recursive=False):
    for child_element in element.find_all(title='Sannois', recursive=False, href=True):
        print(element)
        #element = str(element)
        re_sent = re.match('some', "something") #answer: <_sre.SRE_Match object; span=(0, 4), match='some'>
        print(re_sent)
        #print(re.match(r"[^.]*Sannois[^.]*\.", str(element))) #alternative no regex, split(".") + if 'sannois' in element; RE


#fileparsing
 with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/Cyrano_de_Bergerac.xml') as wiki_f:
     wiki_file = wiki_f.read()
     print(wiki_file)


#et
# tree = ET.parse('C:/Users/danielak/Desktop/country_data.xml')
#                 #'Dokumente Daniela/UNI/FIZ/First Task/Cyrano_de_Bergerac.xml')
# print(tree)


#creating file
