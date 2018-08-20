# Script to extract sentences from Wikipedia articles which contain a link

1. Run Preprocessing.py \
Input: desired number of subfiles of Wikipedia Dump, PATH to save subfiles

2. Run wikiextractor/WikiExtractor.py to extract plain articles from subfiles of Wikipedia Dump

3. Run Post_WikiExtractor --> the result of WikiExtractor.py are several subdirectories and files which contain the articles. Post_WikiExtractor sums those files up.

4. Run Extract_Sentences