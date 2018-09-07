# Script to extract sentences from Wikipedia articles which contain a link

##### Input: Wikipedia dump 
##### Output: File with triples as following: 
\<http://dbpedia.org/resource/Cyrano_de_Bergerac> \<http://dbpedia.org/resource/Sannois> "He died over a year later on July 28, 1655, aged 36, at the house of his cousin, Pierre De Cyrano, in [[Sannois]]." \
*Subject:* Link to the current article in dbpedia \
*Predicate:* Page Link \
*Object:* Sentence with link in brackets 

## Usage:
**CHANGE TO FOLDER \wikiextractor**
    
    usage: WikiExtractor.py [-h] [-o OUTPUT] -l input

    Process wikidumps to extract all links from the articles and the according sentences
    (There is much more possible with the WikiExtractor, but this is enough for this use)

    positional arguments:
      input                 XML wiki dump file

    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT, --output OUTPUT
                            directory for RESULTFILE
      
## Files

wikiextractor/WikiExtractor.py : cleans the subfiles for further processing 

Extract_Sentences.py : Extracts the links and the according sentences and creates files for each folder which is created by the WikiExtractor.py 

Post_WikiExtractor.py : Sums all files up to one RESULT FILE

### Running on Windows
To run the script on Windows the encoding needs to be changed at following locations: \
*WikiExtractor.py:* Line 2843 change encoding to:input = fileinput.FileInput(input_file, openhook=fileinput.hook_encoded('cp65001')) \
*Extract_Sentence.py:* Line 18 add following encoding: with open(INPUT_PATH, encoding='cp65001') as wiki_f: \
*Extract_Sentence.py:* Line 97 add following encoding: resulting_file= open(resulting_path+ '/res' + str(now.month) + str(now.day) + '.txt', "w+", encoding='cp65001') \

 



