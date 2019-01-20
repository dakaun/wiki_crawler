import shutil
import os
import pandas as pd

# After the processing with WikiExtractor.py the articles are in several subdirectories and subfiles with the following structure
def sum_up(dir_root, path_dir):
    '''
    sums up subfiles to result file
    :param dir_root: root directory of subfiles
    :param path_dir: result directory
    :return: result file
    '''
    os.makedirs(os.path.dirname(path_dir), exist_ok=True)
    #complete_wiki = open(path_dir + '/wiki_triples.txt', 'wb')
    #df_complete = pd.DataFrame(columns={'article_title', 'link', 'sentence'})
    frame = []
    for root, dirs, files in os.walk(dir_root):
        for tempfile in files:
            if 'res' in tempfile:
                tempfile_dir = os.path.join(root, tempfile)
                #open_tempfile = open(tempfile_dir, 'rb')
                df_res = pd.read_csv(tempfile_dir, sep=';') # , encoding='cp65001'
                # frame = [df_res, df_complete]
                frame.append(df_res)
                #df = df.concat(frame, axis=0)
                # shutil.copyfileobj(open_tempfile, complete_wiki) # this adds both files
                #df.tocsv(path_dir + '/wiki_triples.csv', sep=';', index=False)
    df_complete = pd.concat(frame ,ignore_index=True)
    df_complete.to_csv(path_dir + '/wiki_triples.csv', index=False, sep=';')


if __name__ == '__main__':
    sum_up(r"C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/test_wiki_crawler/test_1901",
           r'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/Second_Task/test_wiki_crawler/test_1901')
