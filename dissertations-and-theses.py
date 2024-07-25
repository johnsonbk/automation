#! /opt/local/bin/python

import json
from collections import OrderedDict

f = open('dart-dissertations-theses.json')

publications = json.load(f)

publications = sorted(publications, key=lambda x:x['issued']['date-parts'][0][0], reverse=True)

current_year = '3000'
print('current_year', current_year)

before_dart_string = 'BD ... Before DART'

page_string = """---
title       : "Dissertations and Theses"
aliases     :
   - /pages/dissertations.html
---

The following list contains known dissertations and theses that use DART.

Please contact [dart@ucar.edu](mailto:dart@ucar.edu) to add your dissertation
or thesis to the list.

"""

year_header = """
---
## {current_year}
---
"""

dissertation_or_thesis_string = """
![](/images/pin4.gif) **{author}**, {publication_year}: {title}  
    {genre}, *{publisher}*, {publisher_place}. [{url}]({url})
"""



for publication in publications:

    publication_year = publication['issued']['date-parts'][0][0]
    title = publication['title']

    if current_year != publication_year and current_year == '2005':
        current_year = before_dart_string
        page_string += year_header.format(current_year = current_year)

    if current_year != publication_year and current_year != before_dart_string:
        current_year = publication_year
        page_string += year_header.format(current_year = current_year)

    for iauthor, this_author in enumerate(publication['author']):

        initials = ''
        first_middle = this_author['given'].split(' ')
        for name in first_middle:
            initials += name[0] + '.'

        author = this_author['family'] + ' ' + initials

    if publication['genre'] == 'Thesis':
        genre = 'Master\'s thesis'
    elif publication['genre'] == 'Dissertation':
        genre = 'Doctoral dissertation'

    if title[-1] != '.' and title[-1] != '?':
        title += '.'

    url = publication['URL']
    publisher = publication['publisher']
    publisher_place = publication['publisher-place']
    
    page_string += dissertation_or_thesis_string.format(author=author, publication_year=publication_year, title=title, genre=genre, publisher=publisher, publisher_place=publisher_place, url=url)

page_string += """

----

"""

print(page_string)

output_file = '../dart-web/content/dissertations-and-theses/_index.md'

f = open(output_file, 'w')
f.write(page_string)
f.close()
