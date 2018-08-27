import shutil
import os

# After the processing with WikiExtractor.py the articles are in several subdirectories and subfiles with the following structure


def sum_up(dir_root, path_dir):
    os.makedirs(os.path.dirname(path_dir), exist_ok=True)
    complete_wiki = open(path_dir + '/wiki_sum.txt', 'wb')
    for root, dirs, files in os.walk(dir_root):
        for tempfile in files:
            tempfile_dir = os.path.join(root, tempfile)
            open_tempfile = open(tempfile_dir, 'rb')
            shutil.copyfileobj(open_tempfile, complete_wiki)
        # #print('---root {}'.format(root))
        # for tempfile in files:
        #     if 'res' in tempfile:
        #         #print('---file {}'.format(tempfile))
        #         tempfile_dir = os.path.join(root, tempfile)
        #         open_tempfile = open(tempfile_dir, 'rb')
        #         shutil.copyfileobj(open_tempfile, complete_wiki)