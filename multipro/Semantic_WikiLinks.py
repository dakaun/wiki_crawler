from multipro import Preprocessing
from wikiextractor import WikiExtractor
from multipro import Extract_Sentences
from multipro import Post_WikiExtractor
import argparse
import os

# MAIN FILE TO CONNECT ALL PROCESS - IF POSSIBLE

parser = argparse.ArgumentParser(
    description='Process wikidumps to extract all links from the articles and the according sentences')
parser.add_argument('input', help='XML wiki dump file')
parser.add_argument('-o', '-- output', default='directory for RESULTFILE')
args = parser.parse_args()
input_file = args.input
output_path = args.output #'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# import initial wikidump and do preprocessing
with open(input_file, encoding='cp65001') as wiki_dump:
    # number of subfiles of wikidump to create
    NB_OF_SUBFILES = 2
    # path to save created subfiles of wikidump
    FILEPATH = output_path+'/sub_files/'
    # Preprocessing
    Preprocessing.pre_process(wiki_dump, NB_OF_SUBFILES, FILEPATH)
print('1 PREPROPESSING COMPLETE')

# run WikiExtractor on each files
for i in range(NB_OF_SUBFILES):
    print('2 -- WikiExtractor called for File' + str(i + 1))
    INPUT_FILE = output_path + '/sub_files/wikisub_' + str(i + 1) + '.txt'
    OUTPUT_FILE = output_path + '/result/' + str(i + 1)
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    if __name__ == '__main__':
        WikiExtractor.main(['-o', OUTPUT_FILE, '-l', INPUT_FILE])

print('2 WIKIEXTRACTOR COMPLETE')

# summing up result files of WikiExtractor to one file
# After the processing with WikiExtractor.py the articles are in several subdirectories and subfiles with the following structure


ROOTDIR = output_path + '/result/'
PATH_COMPLETE_WIKI = output_path + '/result_complete/'
Post_WikiExtractor.sum_up(ROOTDIR, PATH_COMPLETE_WIKI)
print('3 ALL FILES SUMMED UP')

# run script to extract sentences
Extract_Sentences.result_file(output_path + 'wiki_1+2.txt', )
print('COMPLETE')
