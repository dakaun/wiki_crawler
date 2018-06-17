import shutil
import os

ROOTDIR = '/home/daniela/wikipedia20180401/wikiextractor/result_wikiextractor_1_links/'

complete_wiki = open('/home/daniela/wikipedia20180401/wikiextractor/result_wikiextractor_1_links/wiki_1.txt', 'wb')
for root, dirs, files in os.walk(ROOTDIR):
    print('---root {}'.format(root))
    for tempfile in files:
        print('---file {}'.format(tempfile))
        tempfile_dir = os.path.join(root, tempfile)
        open_tempfile = open(tempfile_dir, 'rb')
        shutil.copyfileobj(open_tempfile, complete_wiki)

print('--finished with all files')