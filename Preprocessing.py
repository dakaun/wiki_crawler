import math
import os
import time
import fileinput


# counts the number lines of a file
def count_lines(file_dir):
    with open(file_dir) as wiki_dump: #, encoding='cp65001'
        nb_lines = sum(1 for line in wiki_dump)
    return nb_lines


# splits the file into n subfiles
# and extracts the header which is necessary to process the files with WikiExtractor.py
def split_file(file, nb_lines, nb_subfiles, time_start, OUTPUT_PATH):
    # split into n files
    split_line = math.ceil(nb_lines / nb_subfiles)

    sub_file = ""
    line_counter = 0
    header = ""
    file_counter = 1

    # iterate through wikidump and split it after have of the file and end of an article
    split = split_line
    for file_line in file:
        sub_file += file_line
        # extracts header, since this is necessary for WikiExtractory to process the different files
        if (line_counter < 44):
            header += file_line
        if (line_counter == split):
            if ('</page>' in file_line):
                add_header_file(OUTPUT_PATH, sub_file, header, file_counter)
                sub_file = ""
                split = split + split_line
                file_counter += 1
                print('1 -- ' + str(file_counter) + '/' + str(nb_subfiles) +
                      ' time: ' + str(time.time() - time_start))
            else:
                split += 1
        line_counter += 1
    add_header_file(OUTPUT_PATH, sub_file, header, file_counter)

# adds header to every subfile which is necessary to process the files with WikiExtractor.py later
def add_header_file(PATH, file, header, file_count):
    if '<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi' not in file:
        file = header + file
    write_subfile_file(PATH, file, file_count)


# writes subfiles in given directory
def write_subfile_file(PATH, file, filename):
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    with open(PATH + 'wikisub_' + str(filename) + '.txt', 'w') as subfile: # , encoding='cp65001'
        subfile.write(file)


def pre_process(input_file, nb_subfiles, subfile_path):
    """
    :param input_file: input directory as given from command line
    :param nb_subfiles: nb of subfiles the wiki dump should be split. nb is given from command line
    :param subfile_path: dir for subfiles as given from commandline
    :return: creates the subfiles as result in dir subfile_path
    """
    # count the number of lines of a file
    start_preprocessing = time.time()
    # open file
    input = fileinput.FileInput(input_file,
                                openhook=fileinput.hook_compressed)  # openhook=fileinput.hook_compressed openhook=fileinput.hook_encoded('cp65001')

    nb_lines = count_lines(input_file)

    # splits wikidump into n subfiles
    split_file(input, nb_lines, nb_subfiles, start_preprocessing, subfile_path)
    input.close()

    #print('1 -- Subfiles are saved in given directory: ' + FILEPATH + ' and it took ' + str(
    #    time.time() - start_preprocessing))

