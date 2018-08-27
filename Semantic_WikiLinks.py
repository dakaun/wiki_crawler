import Preprocessing
from wikiextractor import WikiExtractor
import Extract_Sentences
import Post_WikiExtractor
import argparse
import os
import time
from multiprocessing import Process, cpu_count, Queue, Pool

# TODO catch exceptions
start = time.time()

if __name__ == '__main__':
    # process commandline input
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
        nb_subfiles = cpu_count() - 1
    else:
        nb_subfiles = args.nbsplitting

    # import initial wikidump and start preprocessing
    with open(input_file) as wiki_dump: #, encoding='cp65001'
        Preprocessing.pre_process(input_file, wiki_dump, nb_subfiles, output_path + '/sub_files/')
    #print('1 PREPROPESSING COMPLETE in {}'.format(time.time() - start))
    start_preprocess = time.time()

    # run WikiExtractor on each files
    for i in range(nb_subfiles):
        #print('2 -- WikiExtractor called for File' + str(i + 1))
        INPUT_FILE = output_path + '/sub_files/wikisub_' + str(i + 1) + '.txt'
        OUTPUT_FILE = output_path + '/step2/' + str(i + 1)
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        WikiExtractor.main(['-o', OUTPUT_FILE, '-l', INPUT_FILE])
    #print('2 WIKIEXTRACTOR COMPLETE in {}'.format(time.time() - start))
    start_wikextr = time.time()
    # summing up result files of WikiExtractor to one file
    # After the processing with WikiExtractor.py the articles are in several subdirectories and subfiles with the following structure

    ROOTDIR = output_path + '/step2/'
    PATH_COMPLETE_WIKI = output_path + '/step3/'
    Post_WikiExtractor.sum_up(ROOTDIR, PATH_COMPLETE_WIKI)

    Extract_Sentences.result_file([PATH_COMPLETE_WIKI + '/wiki_sum.txt', output_path])


    # jobs = []
    # dir_data = []
    # start_multi = time.time()
    # for root, dirs, files in os.walk(output_path + '/step2/'):
    #     for subfile in files:
    #         dir_data.append([root + '/' + subfile, root])
    #
    # p = Pool(processes=(1))
    # p.map(Extract_Sentences.result_file, dir_data)
    # start_sum = time.time()
    # ROOTDIR = output_path + '/step2/'
    # Post_WikiExtractor.sum_up(ROOTDIR, output_path)

    #print('3 ALL FILES SUMMED UP in {}'.format(time.time() - start))
    # run script to extract sentences
    #Extract_Sentences.result_file(PATH_COMPLETE_WIKI + '/wiki_sum.txt', output_path)
    end = time.time()

    print('COMPLETE. IT TOOK {}'.format(end - start))
    print('PREPROCESS TOOK {}'.format(start_preprocess-start))
    print('WIKIEXTRACTOR TOOK {}'.format(start_wikextr - start_preprocess))
    print('MULTIPROCESS TOOK {}'.format(start_multi - start_wikextr))
    print('SUM FILES UP TOOK {}'.format(start_sum -start_multi))
