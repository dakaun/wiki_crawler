import Preprocessing
from wikiextractor import WikiExtractor
import Extract_Sentences
import Post_WikiExtractor
import argparse
import os
import time
from multiprocessing import cpu_count, Pool
import shutil
import fileinput

# TODO catch exceptions
start = time.time()

if __name__ == '__main__':
    # process commandline input
    parser = argparse.ArgumentParser(
        description='Process wikidumps to extract all links from the articles and the according sentences')
    parser.add_argument('input', help='XML wiki dump file')
    parser.add_argument('-o', '--output', help='directory for RESULTFILE', default='text')
    #parser.add_argument('-split', type=int, help='Nb of desired subfiles (default =2)', default=2)
    default_processes = max(1, cpu_count()-2)
    parser.add_argument('-processes', type=int, help ='Number of processes to use', default=default_processes)

    args = parser.parse_args()  # ['-o', 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/testest/res2808', '-split', '5', '-processes', '3', 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/testest/wiki_dump.txt']
    input_file = args.input
    output_path = args.output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    nb_processes = args.processes
    #if args.split > (cpu_count() - 1):  # number of subfiles of wikidump to create
    #    nb_subfiles = cpu_count() - 1
    #else:
    #    nb_subfiles = args.split

    # import initial wikidump and start preprocessing
    # with open(input_file) as wiki_dump: #, encoding='cp65001'
    #Preprocessing.pre_process(input_file, nb_subfiles, output_path + '/sub_files/')
    #print('1 PREPROPESSING COMPLETE in {}'.format(time.time() - start))
    #end_preprocess = time.time()


    # run WikiExtractor on each files
    #for i in range(nb_subfiles):
        #print('2 -- WikiExtractor called for File' + str(i + 1))
        #INPUT_FILE =  + '/sub_files/wikisub_' + str(i + 1) + '.txt'
    OUTPUT_FILE = output_path + '/step2/'
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    WikiExtractor.main(['-o', OUTPUT_FILE, '-l', input_file])
    #print('2 WIKIEXTRACTOR COMPLETE in {}'.format(time.time() - start))
    end_wikextr = time.time()

    # append subfiles_dir in list to extract sentences by multiprocessing
    jobs = []
    dir_data = []
    seen = set(dir_data)
    for root, dirs, files in os.walk(output_path + '/step2/'):
        if files:
            complete_sub_wiki = open(root + '/wiki_sum.txt', 'wb')
            for subfile in files:
                subfile_dir = os.path.join(root, subfile)
                open_subfile = open(subfile_dir, 'rb')
                shutil.copyfileobj(open_subfile, complete_sub_wiki)
                if root not in seen:
                    seen.add(root)
                    dir_data.append([root + '/wiki_sum.txt', root])
    # use Pool for multiprocessing
    p = Pool(processes=nb_processes)
    p.map(Extract_Sentences.result_file, dir_data)
    end_multi = time.time()

    # sum files up to result file
    ROOTDIR = output_path + '/step2/'
    Post_WikiExtractor.sum_up(ROOTDIR, output_path)

    #print('3 ALL FILES SUMMED UP in {}'.format(time.time() - start))
    end = time.time()

    # time tracking
    print('Time tracking: complete process {}'.format(end - start))
    #print('Time tracking: Preprocessing {}'.format(end_preprocess - start))
    print('Time tracking: Wikiextraction {}'.format(end_wikextr - start))
    print('Time tracking: Multiprocessing {}'.format(end_multi - end_wikextr))
    print('Time tracking: Summing up {}'.format(end - end_multi))
