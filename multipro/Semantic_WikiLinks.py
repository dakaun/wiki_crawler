from multipro import Preprocessing
from wikiextractor import WikiExtractor

# MAIN FILE TO CONNECT ALL PROCESS - IF POSSIBLE

# import initial wikidump and do preprocessing
# with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump/wiki_dump.txt',
#               encoding='cp65001') as wiki_dump:
#     # number of subfiles of wikidump to create
#     NB_OF_SUBFILES = 2
#     # path to save created subfiles of wikidump
#     FILEPATH = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump/sub_files/'
#     # Preprocessing
#     Preprocessing.pre_process(wiki_dump, NB_OF_SUBFILES, FILEPATH)

# run WikiExtractor on each files


# import shutil
# import os
#
# ROOTDIR = '/home/daniela/wikipedia20180401/wikiextraction/result_wikipart_5/result_wikiextractor_5/'
#
# complete_wiki = open('/home/daniela/wikipedia20180401/wikiextraction/result_wikipart_5/result_wikiextractor_5/wiki_5.txt', 'wb')
# for root, dirs, files in os.walk(ROOTDIR):
#     print('---root {}'.format(root))
#     for tempfile in files:
#         print('---file {}'.format(tempfile))
#         tempfile_dir = os.path.join(root, tempfile)
#         open_tempfile = open(tempfile_dir, 'rb')
#         shutil.copyfileobj(open_tempfile, complete_wiki)
#
# print('--finished with all files')
# summing up result files of WikiExtractor to one file
# run script to extract sentences

