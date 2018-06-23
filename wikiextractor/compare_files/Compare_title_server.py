def treat_after():
    title = []
    with open(
            '/home/daniela/wikipedia20180401/wikiextractor/result_wikiextractor_1_links/wiki_1_title') as after_extraction:
        after_extract = after_extraction.readlines()
        for line in after_extract:
            title_split = line.split('"')
            if (len(title_split) > 5):
                #title_split[5] = title_split[5].replace('&quot;', '\"')
                title.append(title_split[5])
    # print('After List created')
    return title


def treat_before():
    title = []
    with open(
            '/home/daniela/wikipedia20180401/enwiki-20180401-pages-articles-multistream_1_title') as before_extraction:
        before_extract = before_extraction.readlines()
        for line in before_extract:
            seps = ['<', '>']
            title_split = [line]
            for sep in seps:
                line, title_split = title_split, []
                for seq in line:
                    title_split += seq.split(sep)
            if (len(title_split) > 2):
                title.append(title_split[2])
    # print('Before List created')
    return title


def sort_alph(list):
    list.sort()  # sort only works with lists
    return list


def write_file(list, file):
    for element in list:
        file.write(element + '\n')
    # print("file written")
    return file


def compare_tit():
    line_no = 1
    counter = 0
    with open('/home/daniela/wikipedia20180401/compare_title/title_before',
              'r') as before_f:
        before_line = before_f.readline()
        with open(
                '/home/daniela/wikipedia20180401/compare_title/title_after',
                'r') as after_f:
            after_line = after_f.readline()
            while before_line != '':
                before_line = before_line.rstrip()
                after_line = after_line.rstrip()
                if before_line != after_line:
                    counter += 1
                    print('> Line-{} '.format(line_no) + before_line)
                    line_no += 1
                    before_line = before_f.readline()
                elif before_line == after_line:
                    # print('= Line -{} are the same ='.format(line_no) + before_line)
                    before_line = before_f.readline()
                    after_line = after_f.readline()
                    line_no += 1
                else:
                    print('came across here !?')
    print('counter for different files {}'.format(counter))
    return 'readyfready'


title_list_before = treat_before()
sorted_list_before = sort_alph(title_list_before)
print("List Before has {} items".format(len(sorted_list_before)))
with open('/home/daniela/wikipedia20180401/compare_title/title_before', 'w') as title_result_before:
    for elementb in sorted_list_before:
        title_result_before.write(elementb + '\n')

title_list_after = treat_after()
sorted_list_after = sort_alph(title_list_after)
print("List After has {} items".format(len(sorted_list_after)))
with open('/home/daniela/wikipedia20180401/compare_title/title_after', 'w') as title_result_after:
    for elementa in sorted_list_after:
        title_result_after.write(elementa + '\n')

compare_tit()
print('--COMAPARISON COMPLETED')
