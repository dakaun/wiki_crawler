import math
import os
import time
import fileinput


# counts the number lines of a file
def count_lines(file):
    nb_lines = sum(1 for line in file)
    # for i, l in enumerate(file):
    #     pass
    return nb_lines  # i + 1


# splits the file into n subfiles
# and extracts the header which is necessary to process the files with WikiExtractor.py
def split_file(file, nb_lines, nb_subfiles, time_start, OUTPUT_PATH):
    # split into n files
    split_line = math.ceil(nb_lines / nb_subfiles)

    sub_file = ""
    file_list = []
    line_counter = 0
    header = ""
    file_counter = 1

    # iterate through wikidump and split it after have of the file and end of an article
    #print('1 -- start iterating through lines')
    split = split_line
    # file_line = file.readline()
    for file_line in file:
        sub_file += file_line
        if (
                line_counter < 44):  # extracts header, since this is necessary for WikiExtractory to process the different files
            header += file_line
        if (line_counter == split):
            if ('</page>' in file_line):
                # print('1 -- ' + str(math.ceil(split / split_line)) + '/' + str(nb_subfiles))
                add_header_file(OUTPUT_PATH, sub_file, header, file_counter)
                sub_file = ""
                split = split + split_line
                file_counter += 1
                print(
                    '1 -- ' + str(file_counter) + '/' + str(nb_subfiles) + ' time: ' + str(time.time() - time_start))
            else:
                split += 1
        line_counter += 1
        # file_line = file.readline()
    add_header_file(OUTPUT_PATH, sub_file, header, file_counter)
    return file_counter  # TODO necessary?


def add_header_file(PATH, file, header, file_count):
    if '<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi' not in file:
        file = header + file
    write_subfile_file(PATH, file, file_count)


def write_subfile_file(PATH, file, filename):
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    with open(PATH + 'wikisub_' + str(filename) + '.txt', 'w', encoding='cp65001') as subfile: # , encoding='cp65001'
        subfile.write(file)


# adds header to every subfile which is necessary to process the files with WikiExtractor.py later
def add_header_list(file_list, header):
    new_file_list = []
    for file in file_list[1:]:
        new_file_list.append(header + file)
    new_file_list.insert(0, file_list[0])
    return new_file_list


# writes subfiles in given directory
def write_subfile_list(PATH, file_list):
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    counter = 1
    for file in file_list:
        with open(PATH + 'wikisub_' + str(counter) + '.txt', 'w') as new_subfile:  # , encoding='cp65001'
            new_subfile.write(file)
            counter += 1


def pre_process(input_file, wiki_file, NB_OF_SUBFILES, FILEPATH):
    # count the number of lines of a file
    start_preprocessing = time.time()
    # open file
    input = fileinput.FileInput(input_file,
                                openhook=fileinput.hook_encoded('cp65001'))  # openhook=fileinput.hook_compressed openhook=fileinput.hook_encoded('cp65001')

    nb_lines = count_lines(wiki_file)
    #print('1 -- Number of Lines of Wikidump ' + str(nb_lines) +
    #      ' and it took ' + str(time.time() - start_preprocessing))

    # splits wikidump into n subfiles
    # input.seek(0)
    #print('1 -- start splitting')
    dump_subfile_list = split_file(input, nb_lines, NB_OF_SUBFILES, start_preprocessing, FILEPATH)
    #print('1 -- Wikidump splitted into ' + str(NB_OF_SUBFILES) + ' Files' + ' and it took ' + str(
    #    time.time() - start_preprocessing))
    input.close()
    # dumpf_subfile_list is tuple which contains list with subfiles as elements + str which is the header

    # add header to every subfile
    #new_subfile_list = add_header_list(dump_subfile_list[0], dump_subfile_list[1])
    #print('1 -- Header added to every subfile' + ' and it took ' + str(time.time() - start_preprocessing))

    # writes subfiles in folder
    # path for subfiles
    #write_subfile_list(FILEPATH, new_subfile_list)
    #print('1 -- Subfiles are saved in given directory: ' + FILEPATH + ' and it took ' + str(
    #    time.time() - start_preprocessing))

# with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump/wiki_dump.txt',
#               encoding='cp65001') as wiki_dump:
#     # number of subfiles of wikidump to create
#     NB_OF_SUBFILES = 2
#     # path to save created subfiles of wikidump
#     FILEPATH = 'C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump/sub_files/'
#     # Preprocessing,
#     pre_process(wiki_dump, NB_OF_SUBFILES, FILEPATH)
