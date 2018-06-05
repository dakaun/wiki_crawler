import shutil
import os

ROOTDIR = '/home/daniela/wiki_pagelinks_2016-10/wikipedia20180401/wikiextractor/result_wikiextractor_1/'

wiki_AA = open('/home/daniela/wiki_pagelinks_2016-10/wikipedia20180401/wikiextractor/result_wikiextractor_1/wiki_1.txt', 'wb')
for root, dirs, files in os.walk(ROOTDIR):
    print('---root {}'.format(root))
    for tempfile in files:
        print('---file {}'.format(tempfile))
        tempfile_dir = os.path.join(root, tempfile)
        open_tempfile = open(tempfile_dir, 'rb')
        shutil.copyfileobj(open_tempfile, wiki_AA)

print('--finished with all files')