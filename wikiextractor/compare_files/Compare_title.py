
title_file_after = open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/compare_title/result_compare_test/title_after.txt', 'w+')
def treat_after():
    title = []
    with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/compare_title/after_extraction.txt') as after_extraction:
        after_extract = after_extraction.readlines()
        for line in after_extract:
            title_split = line.split('"')
            title.append(title_split[5])
            #title_file_after.write(title + '\n')
    print('After List created')
    return title #title_file_after

title_file_before = open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/compare_title/result_compare_test/title_before.txt', 'w+')
def treat_before():
    title = []
    with open('C:/Users/danielak/Desktop/Dokumente Daniela/UNI/FIZ/First Task/compare_title/before_extraction.txt') as before_extraction:
        before_extract = before_extraction.readlines()
        for line in before_extract:
            seps = ['<', '>']
            title_split = [line]
            for sep in seps:
                line, title_split = title_split, []
                for seq in line:
                    title_split += seq.split(sep)
            title.append(title_split[2])
            #title_file_before.write(title + '\n')
    print('Before List created')
    return title #title_file_before


def sort_alph(list):
    list.sort() #sort only works with lists
    return list

def write_file(list, file):
    for element in list:
        file.write(element + '\n')
    print("file written")
    return file

title_list_before = treat_before()
sorted_list_before = sort_alph(title_list_before)
print("List Before has {} items".format(len(sorted_list_before)))
title_result_before = write_file(sorted_list_before, title_file_before)
before_line = title_result_before.readline()

title_list_after = treat_after()
sorted_list_after = sort_alph(title_list_after)
print("List After has {} items".format(len(sorted_list_after)))
title_result_after = write_file(sorted_list_after, title_file_after)
after_line = title_result_after.readline()

line_no = 1

while before_line != '' or after_line != '':
    before_line = before_line.rstrip()
    after_line = after_line.rstrip()
    if before_line != after_line:
        if before_line == '' and after_line != '':
            # If a line does not exist on file2 then mark the output with + sign
            print(">+", "Line-%d" % line_no, after_line)
            # otherwise output the line on file1 and mark it with > sign
        elif after_line != '':
            print(">", "Line-%d" % line_no, after_line)

            # If a line does not exist on file1 then mark the output with + sign
        if after_line == '' and before_line != '':
            print("<+", "Line-%d" % line_no, before_line)
            # otherwise output the line on file2 and mark it with < sign
        elif before_line != '':
            print("<", "Line-%d" % line_no, before_line)

        # Print a blank line
        print()

        # Read the next line from the file
    before_line = title_result_before.readline()
    after_line = title_result_after.readline()

        # Increment line counter
    line_no += 1

        # Close the files
title_result_before.close()
title_result_after.close()