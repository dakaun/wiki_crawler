import Extract_Sentences
import Post_WikiExtractor
import os
import time
from multiprocessing import Pool
import shutil

# TODO catch exceptions
start = time.time()

def main(output_path, nb_processes):
    '''
    The WikiExtractor splits the articles in thousands of files, which will be first used to parallelize
    (Pool multiprocessing) the creation of the triples for each article. In Post_WikiExtractor.sum_up() the result file
    will be summed up to one result file /wiki_triples.txt
    :param output_path: output path, which is given via command input
    :param nb_processes: number of processes to parallelize
    '''
    dir_data = []
    seen = set(dir_data)
    for root, dirs, files in os.walk(output_path):
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
    ROOTDIR = output_path
    Post_WikiExtractor.sum_up(ROOTDIR, output_path)

    # print('3 ALL FILES SUMMED UP in {}'.format(time.time() - start))
    end = time.time()

    # time tracking
    print('Time tracking: complete process {}'.format(end - start))
    print('Time tracking: Summing up {}'.format(end - end_multi))

if __name__ == '__main__':
    main()
