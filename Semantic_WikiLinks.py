import Preprocessing
from wikiextractor import WikiExtractor
import Extract_Sentences
import Post_WikiExtractor
import argparse
import os
import time
from multiprocessing import Process, cpu_count

# TODO catch exceptions
start = time.time()

parser = argparse.ArgumentParser(
    description='Process wikidumps to extract all links from the articles and the according sentences')
parser.add_argument('input', help='XML wiki dump file')
parser.add_argument('-o', '--output', help='directory for RESULTFILE', default='text')
parser.add_argument('-nbsplitting', type=int, help='Nb of desired subfiles (default =2)', default=2)
args = parser.parse_args()  # ['-o', 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/testest/res', '-nbsplitting', '5', 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/testest/wiki_dump.txt']
input_file = args.input
output_path = args.output  # 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
if args.nbsplitting > (cpu_count() - 1):  # number of subfiles of wikidump to create
    NB_OF_SUBFILES = cpu_count() - 1
else:
    NB_OF_SUBFILES = args.nbsplitting

# import initial wikidump and do preprocessing
with open(input_file) as wiki_dump: #, encoding='cp65001'
# path to save created subfiles of wikidump
    FILEPATH = output_path + '/sub_files/'
# Preprocessing
    Preprocessing.pre_process(input_file, wiki_dump, NB_OF_SUBFILES, FILEPATH)
print('1 PREPROPESSING COMPLETE in {}'.format(time.time() - start))

# run WikiExtractor on each files
for i in range(NB_OF_SUBFILES):
    print('2 -- WikiExtractor called for File' + str(i + 1))
    INPUT_FILE = output_path + '/sub_files/wikisub_' + str(i + 1) + '.txt'
    OUTPUT_FILE = output_path + '/step2/' + str(i + 1)
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    if __name__ == '__main__':
        WikiExtractor.main(['-o', OUTPUT_FILE, '-l', INPUT_FILE])
print('2 WIKIEXTRACTOR COMPLETE in {}'.format(time.time() - start))
# TODO change order ? first Extract sentences of subfiles and then sum up --> makes it easier to parallize
# summing up result files of WikiExtractor to one file
# After the processing with WikiExtractor.py the articles are in several subdirectories and subfiles with the following structure

if __name__ == '__main__':
    for root, dirs, files in os.walk(output_path + '/step2/'):
        for subfile in files:
            extract = Process(target=Extract_Sentences.result_file,
                              args=(root + '/' + subfile, root))
            extract.start()
            extract.join()

ROOTDIR = output_path + '/step2/'
Post_WikiExtractor.sum_up(ROOTDIR, output_path)
print('3 ALL FILES SUMMED UP in {}'.format(time.time() - start))

# run script to extract sentences
#Extract_Sentences.result_file(PATH_COMPLETE_WIKI + '/wiki_sum.txt', output_path)
end = time.time()

print('COMPLETE. IT TOOK {}'.format(end - start))
