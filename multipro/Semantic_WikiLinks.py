from multipro import Preprocessing
from wikiextractor-master import WikiExtractor

# import initial wikidump and do preprocessing
with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump/wiki_dump.txt',
              encoding='cp65001') as wiki_dump:
    # number of subfiles of wikidump to create
    NB_OF_SUBFILES = 2
    # path to save created subfiles of wikidump
    FILEPATH = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump/sub_files/'
    # Preprocessing,
    Preprocessing.pre_process(wiki_dump, NB_OF_SUBFILES)



# run WikiExtractor on each files
# summing up result files of WikiExtractor to one file
# run script to extract sentences

