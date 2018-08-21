import shutil
import os

# After the processing with WikiExtractor.py the articles are in several subdirectories and subfiles with the following structure

ROOTDIR = '/home/daniela/wikipedia20180401/wikiextractor/test_wikipart_5/'
PATH_COMPLETE_WIKI = '/home/daniela/wikipedia20180401/wikiextractor/test_wikipart_5/'

os.makedirs(os.path.dirname(PATH_COMPLETE_WIKI), exist_ok=True)
complete_wiki = open(PATH_COMPLETE_WIKI + 'wiki_1+2.txt', 'wb')
for root, dirs, files in os.walk(ROOTDIR):
    print('---root {}'.format(root))
    for tempfile in files:
        print('---file {}'.format(tempfile))
        tempfile_dir = os.path.join(root, tempfile)
        open_tempfile = open(tempfile_dir, 'rb')
        shutil.copyfileobj(open_tempfile, complete_wiki)

print('--finished with all files')