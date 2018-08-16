import multiprocessing
import math


# count the lines of a file
def count_lines(file):
    nb_lines = sum(1 for line in wiki_dump)
    # for i, l in enumerate(file):
    #     pass
    return nb_lines  # i + 1

def split_file(file, nb):
    split = math.ceil(nb_lines/2)
    split_file = ""
    file_list = []
    file_line = file.readline()
    line_counter = 0
    header = ""
    # iterate through wikidump and split it after have of the file and end of an article
    while(file_line):
        split_file += file_line
        if (line_counter < 44): # extracts header, since this is necessary for WikiExtractory to process the different files
            header += file_line
        if (line_counter == split):
            if ('</page>' in file_line):
                file_list.append(split_file)  # safe second part of the file in list - missing
                split_file = ""
            else:
                split +=1
        line_counter += 1
        file_line = file.readline()
        file_list.append(split_file)
    print(file_list)
    return file_list, header

# import initial wikidump
with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/wiki_dump.txt',
          encoding='cp65001') as wiki_dump:

    # count the number of lines of a file
    nb_lines = count_lines(wiki_dump) #to working yet - iteration through file does not work afterwards
    print('-- Number of Lines of Wikidump ' + str(nb_lines))

    #splits file into parts
    wiki_dump.seek(0)
    dump_files = split_file(wiki_dump, nb_lines)
    header = dump_files[1]


# split initial wikidump file
# first lines needs to be added to each wikidump file for WikiExctractor.py
# run WikiExtractor on each files
# summing up result files of WikiExtractor to one file
# run script to extract sentences
