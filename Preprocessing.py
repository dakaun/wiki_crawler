import math
import os
import time


# TODO catch exceptions

# counts the number lines of a file
def count_lines(file):
    nb_lines = sum(1 for line in file)
    # for i, l in enumerate(file):
    #     pass
    return nb_lines  # i + 1


# splits the file into n subfiles
# and extracts the header which is necessary to process the files with WikiExtractor.py
def split_file(file, nb_lines, nb_subfiles):
    # split into n files
    split_line = math.ceil(nb_lines / nb_subfiles)

    sub_file = ""
    file_list = []
    line_counter = 0
    header = ""

    # iterate through wikidump and split it after have of the file and end of an article
    print('1 -- start iterating through lines')
    split = split_line
    file_line = file.readline()
    while (file_line):
        print('1 -- each line')
        sub_file += file_line
        print('1 -- added to sub_file. Split is ' + str(split))
        if (line_counter < 44):  # extracts header, since this is necessary for WikiExtractory to process the different files
            header += file_line
        if (line_counter == split):
            if ('</page>' in file_line):
                file_list.append(sub_file)
                sub_file = ""
                split = split + split_line
            else:
                split += 1
        line_counter += 1
        file_line = file.readline()
    file_list.append(sub_file)
    return file_list, header


# adds header to every subfile which is necessary to process the files with WikiExtractor.py later
def add_header(file_list, header):
    new_file_list = []
    for file in file_list[1:]:
        new_file_list.append(header + file)
    new_file_list.insert(0, file_list[0])
    return new_file_list


# writes subfiles in given directory
def write_subfile(PATH, file_list):
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    counter = 1
    for file in file_list:
        with open(PATH + 'wikisub_' + str(counter) + '.txt', 'w') as new_subfile: #, encoding='cp65001'
            new_subfile.write(file)
            counter += 1


def pre_process(wiki_dump, NB_OF_SUBFILES, FILEPATH):
    # count the number of lines of a file
    start_preprocessing = time.time()
    nb_lines = count_lines(wiki_dump)
    print('1 -- Number of Lines of Wikidump ' + str(nb_lines) + ' and it took ' + str(time.time()- start_preprocessing))

    # splits wikidump into n subfiles
    wiki_dump.seek(0)
    print('1 -- start splitting')
    dump_subfile_list = split_file(wiki_dump, nb_lines, NB_OF_SUBFILES)
    print('1 -- Wikidump splitted into ' + str(NB_OF_SUBFILES) + ' Files' + ' and it took ' + str(time.time()- start_preprocessing))
    # dumpf_subfile_list is tuple which contains list with subfiles as elements + str which is the header

    # add header to every subfile
    new_subfile_list = add_header(dump_subfile_list[0], dump_subfile_list[1])
    print('1 -- Header added to every subfile'+ ' and it took ' + str(time.time()- start_preprocessing))

    # writes subfiles in folder
    # path for subfiles
    write_subfile(FILEPATH, new_subfile_list)
    print('1 -- Subfiles are saved in given directory: ' + FILEPATH + ' and it took ' + str(time.time()- start_preprocessing))

# with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump/wiki_dump.txt',
#               encoding='cp65001') as wiki_dump:
#     # number of subfiles of wikidump to create
#     NB_OF_SUBFILES = 2
#     # path to save created subfiles of wikidump
#     FILEPATH = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump/sub_files/'
#     # Preprocessing,
#     pre_process(wiki_dump, NB_OF_SUBFILES, FILEPATH)
