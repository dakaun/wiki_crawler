#testing nltk library to split sentences

#period in entity - check
#double nb - check
#e.g - not working

import nltk.data
from nltk.tokenize import sent_tokenize

test = 'Anarchism is a <a href="political%20philosophy">political.philosophy</a> that advocates <a href="Self-governance">self-governed</a> societies based on voluntary institutions. These are often described as <a href="Stateless%20society">stateless societies</a>, although several authors have defined them more specifically as institutions based on non-<a href="Hierarchy">hierarchical</a> or <a href="Free%20association%20%28communism%20and%20anarchism%29">free associations</a>. Anarchism holds the <a href="State%20%28polity%29">state</a> to be undesirable, unnecessary and harmful. In e.g.criminal and family - related proceedings in local courts, the panel of judges may include both <a href=\"lay%20judge\">lay judge</a> s and professional judges, while all appeals courts and administrative courts consist only of professional judges. These include e.g. <a href =\"Neste%20Oil\">Neste Oil</a>, <a href=\"VR%20Group\">VR Group</a> (rail), <ahref=\"Finnair\">Finnair</a>, <a href=\"VTT\">VTT</a> (research) and <a href =\"Itella\">Itella</a> (mail). Before the 1940s, the CNT was the major force in Spanish working class politics, attracting 1.58 million members at one point and playing a major role in the <a href=\"Spanish%20Civil%20War\">Spanish Civil War</a>. In 2012, the <a href=\"National%20Health%20Service\">NHS</a> estimated that the overall prevalence of autism among adults aged 18 years and over in the UK was 1.1. '
# tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
# print('\n----\n'.join(tokenizer.tokenize(test)))

result = sent_tokenize(test) #list
print(type(result))

