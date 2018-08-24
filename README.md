# Script to extract sentences from Wikipedia articles which contain a link

##### Input: Wikipedia dump 
##### Output: File with triples: 
<http://dbpedia.org/resource/Cyrano_de_Bergerac> <http://dbpedia.org/resource/Sannois> "He died over a year later on July 28, 1655, aged 36, at the house of his cousin, Pierre De Cyrano, in [[Sannois]]."

## Usage:
    usage: Semantic_WikiLinks.py [-h] [-o OUTPUT] [-nbsplitting NBSPLITTING] input

    Process wikidumps to extract all links from the articles and the according sentences

    positional arguments:
      input                 XML wiki dump file

    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT, --output OUTPUT
                            directory for RESULTFILE
      -nbsplitting NBSPLITTING
                            Nb of desired subfiles (default = 2)
## Files
Preprocessing.py : Splits the input Wiki dump into subfiles and saves those subfiles in OUTPUT/sub_files/

wikiextractor/WikiExtractor.py : cleans the subfiles for further processing and saves the articles in OUTPUT/step2/

Post_WikiExtractor.py : the result of WikiExtractor.py are several subdirectories and files which contain the articles. Post_WikiExtractor sums those files up and saves them in OUTPUT/step3/

Extract_Sentences.py : Extracts the links and the according sentences and creates the RESULTFILE in OUTPUT 