import Extract_title_server
import time

# this script compares the title from the wikidump (but file with only titles) with the file after WikiExtractor run
# the wikidump. Since many articles got lost along the way, it needed to be checked which files got lost
# in the end of this script nb all the categories (only those which disapear) are returned
# input:
#       - wikidump file with only article titles after WikiExtractor.py
#       - wikidump file only article titles (before WikiExtractor.py)
#       - Extract_title_server.py : wikidump file
# output: nb of articles for each category listed below --> those articles within those categories are more descriptive
# and formal wikipedia articles (no content) and therefore are not considered in the WikiExtractor

start = time.time()


def treat_after():
    title = []
    with open(
            '/home/daniela/wikipedia20180401/wikiextractor/result_wikipart_5/result_wikiextractor_1/wiki_1_title') as after_extraction: #wiki_dump file after WikiExtractor.py
        after_extract = after_extraction.readlines()
        for line in after_extract:
            title_split = line.split('"')
            if (len(title_split) > 5):
                # title_split[5] = title_split[5].replace('&quot;', '\"')
                title.append(title_split[5])
    # print('After List created')
    return title


def treat_before():
    title = []
    with open(
            '/home/daniela/wikipedia20180401/wikipart_5/enwiki-20180401-pages-articles-multistream_1_title') as before_extraction: # wiki dump file only article titles
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
# with open('/home/daniela/wikipedia20180401/compare_title/title_before', 'w') as title_result_before:
#     for elementb in sorted_list_before:
#         title_result_before.write(elementb + '\n')
before_set = set(sorted_list_before)

title_list_after = treat_after()
sorted_list_after = sort_alph(title_list_after)
print("List After has {} items".format(len(sorted_list_after)))
# with open('/home/daniela/wikipedia20180401/compare_title/title_after', 'w') as title_result_after:
#     for elementa in sorted_list_after:
#         title_result_after.write(elementa + '\n')
after_set = set(sorted_list_after)

red_prev_titles = Extract_title_server.get_titles()
titles_explicable = before_set - red_prev_titles[0] - red_prev_titles[1] - red_prev_titles[2] - after_set
# additionals_in_b = before_set - after_set

wikipedia_list = []
category_list = []
file_list = []
template_list = []
portal_list = []
mediawiki_list = []
help_list = []
draft_list = []
module_list = []
for element in titles_explicable:
    if 'Wikipedia:' in element:
        wikipedia_list.append(element)
    elif 'Category:' in element:
        category_list.append(element)
    elif 'File:' in element:
        file_list.append(element)
    elif 'Template:' in element:
        template_list.append(element)
    elif 'Portal:' in element:
        portal_list.append(element)
    elif 'MediaWiki:' in element:
        mediawiki_list.append(element)
    elif 'Help:' in element:
        help_list.append(element)
    elif 'Draft' in element:
        draft_list.append(element)
    elif 'Module:Location map' in element:
        module_list.append(element)
titles_inexplicable = before_set - red_prev_titles[0] - red_prev_titles[1] - red_prev_titles[2] - after_set - set(
    wikipedia_list) - set(category_list) - set(file_list) - set(template_list) - set(portal_list) - set(
    mediawiki_list) - set(help_list) - set(draft_list) - set(module_list)

# compare_tit()
# include those prints
print('--{} ARTICLES BEFORE'.format(len(title_list_before)))
print('--{} REDIRECT #REDIRECT ARTICLES'.format(len(red_prev_titles[0])))
print('--{} REDIRECT <redirect ARTICLES'.format(len(red_prev_titles[2])))
print('--{} PREVIEW ARTICLES'.format(len(red_prev_titles[1])))
print('--{} ARTICLES - BEFORE - PREVIEW - REDIRECT'.format(len(titles_explicable)))
print('--{} WIKIPEDIA ARTICLES'.format(len(wikipedia_list)))
print('--{} CATEGORY ARTICLES'.format(len(category_list)))
print('--{} FILE ARTICLES'.format(len(file_list)))
print('--{} TEMPLATE ARTICLES'.format(len(template_list)))
print('--{} PORTAL ARTICLES'.format(len(portal_list)))
print('--{} MEDIAWIKI ARTICLES'.format(len(mediawiki_list)))
print('--{} HELP ARTICLES'.format(len(help_list)))
print('--{} DRAFT ARTICLES'.format(len(draft_list)))
print('--{} MODULE:LOCATION ARTICLES'.format(len(module_list)))
print('--{} INEXPLICABLE ARTICLES'.format(len(titles_inexplicable))) #TODO print inexplicable titles

print('--COMPARISON COMPLETED')

if titles_inexplicable > 0:
    print('--{} INEXPLICABLES:')
    for element_inex in titles_inexplicable:
        print(element_inex)

end = time.time()
print('--- TIME {}'.format(end - start))
