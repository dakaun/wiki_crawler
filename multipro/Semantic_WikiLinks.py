from multipro import Preprocessing
from wikiextractor import WikiExtractor
from multipro import Extract_Sentences
import shutil
import os

# MAIN FILE TO CONNECT ALL PROCESS - IF POSSIBLE

# import initial wikidump and do preprocessing
# with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump/wiki_dump.txt',
#           encoding='cp65001') as wiki_dump:
#     # number of subfiles of wikidump to create
#     NB_OF_SUBFILES = 2
#     # path to save created subfiles of wikidump
#     FILEPATH = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump/sub_files/'
#     # Preprocessing
#     Preprocessing.pre_process(wiki_dump, NB_OF_SUBFILES, FILEPATH)
# print('PREPROPESSING COMPLETE')

# # run WikiExtractor on each files
# INPUT_FILE = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump/sub_files/wikisub_1.txt'
# OUTPUT_FILE = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump/result/1'
# os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
# WikiExtractor.main(['-o', OUTPUT_FILE, '-l', INPUT_FILE])
# print('WIKIEXTRACTOR COMPLETE')

# summing up result files of WikiExtractor to one file
# After the processing with WikiExtractor.py the articles are in several subdirectories and subfiles with the following structure

print('-- Start')

def sum_up(dir_root, path_dir):
    os.makedirs(os.path.dirname(path_dir), exist_ok=True)
    complete_wiki = open(path_dir + 'wiki_1+2.txt', 'wb')
    for root, dirs, files in os.walk(dir_root):
        print('---root {}'.format(root))
        for tempfile in files:
            print('---file {}'.format(tempfile))
            tempfile_dir = os.path.join(root, tempfile)
            open_tempfile = open(tempfile_dir, 'rb')
            shutil.copyfileobj(open_tempfile, complete_wiki)
    print('ALL FILES SUMMED UP')

ROOTDIR = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump/result/'
PATH_COMPLETE_WIKI = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump/result_complete/'
sum_up(ROOTDIR, PATH_COMPLETE_WIKI)

# run script to extract sentences
Extract_Sentences.result_file(PATH_COMPLETE_WIKI  + 'wiki_1+2.txt', )
print('COMPLETE')
