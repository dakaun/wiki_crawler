import shutil
import os

# After the processing with WikiExtractor.py the articles are in several subdirectories and subfiles with the following structure
def sum_up(dir_root, path_dir):
    '''
    sums up subfiles to result file
    :param dir_root: root directory of subfiles
    :param path_dir: result directory
    :return: result file
    '''
    os.makedirs(os.path.dirname(path_dir), exist_ok=True)
    complete_wiki = open(path_dir + '/wiki_triples.txt', 'wb')
    for root, dirs, files in os.walk(dir_root):
        for tempfile in files:
            if 'res' in tempfile:
                tempfile_dir = os.path.join(root, tempfile)
                open_tempfile = open(tempfile_dir, 'rb')
                shutil.copyfileobj(open_tempfile, complete_wiki)