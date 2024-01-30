#! /opt/local/bin/python

import json
from collections import OrderedDict

f = open('dart-publications.json')

publications = json.load(f)

publications = sorted(publications, key=lambda x:x['issued']['date-parts'][0][0], reverse=True)

current_year = '3000'
print('current_year', current_year)

before_dart_string = 'BD ... Before DART'

page_string = """---
title       : "Publications"
aliases     :
   - /pages/Publications.html
---

The following publication list contains known publications that use DART.

Please contact [dart@ucar.edu](mailto:dart@ucar.edu) to add your publication
to the list.

Recent publications coauthored by NCAR staff should be freely available in the
NSF NCAR online database known as [Opensky](https://opensky.ucar.edu/) by
searching for a given publication's title.

To cite DART in your publication, please use this citation updating the DART
version and year as appropriate:

> The Data Assimilation Research Testbed (Version X.Y.Z) [Software]. (2024). Boulder, Colorado: NSF NCAR/CISL/DAReS. [http://doi.org/10.5065/D6WQ0202](http://doi.org/10.5065/D6WQ0202)

The seminal reference is:

**Anderson, J. L., T. Hoar, K. Raeder, H. Liu, N. Collins, R. Torn
and A. Arellano**, 2009
The Data Assimilation Research Testbed: A Community Facility.
*Bulletin of the American Meteorological Society*, **90**, 1283-1296,
[doi:10.1175/2009BAMS2618.1](http://dx.doi.org/10.1175/2009BAMS2618.1)

"""

year_header = """
---
## {current_year}
---
"""

article_string = """
![](/images/pin4.gif) **{authors}**, {publication_year}  
    {title}  
    *{journal}*,{volume}{page}[{doi}]({url})
"""

chapter_string = """
![](/images/pin4.gif) **{authors}**, {publication_year}  
    {title}  
    *{book}*.  
    {editors}, {publisher}, ISBN: {isbn}
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

        if iauthor == 0:
            authors = this_author['family'] + ' ' + initials
        elif iauthor + 1 == len(publication['author']):
            authors += ' & ' + initials + ' ' + this_author['family']
        else:
            authors += ', ' + initials + ' ' + this_author['family']

    if publication['type'] == 'article-journal':

        if title[-1] != '?' and title[-1] != '.':
            title += '.'            

        journal = publication['container-title']

        try:
            volume = ' **' + publication['volume']+'**, '
        except:
            volume = ' '
        try:
            page = publication['page']+', '
        except:
            page = ' '
        try:
            doi = 'doi:' + publication['DOI']
            url = 'https://doi.org/' + doi
        except:
            print(title)
            doi = ' '
            url = ' '

        page_string += article_string.format(authors=authors, publication_year=publication_year, title=title, journal=journal, volume=volume, page=page, doi=doi, url=url)

    elif publication['type'] == 'chapter':

        if title[-1] != '?' and title[-1] != '.':
            title += ','

        book = publication['container-title']
        publisher = publication['publisher']
        isbn = publication['ISBN']

        for ieditor, this_editor in enumerate(publication['editor']):
            initials = ''
            first_middle = this_editor['given'].split(' ')
            for name in first_middle:
                initials += name[0] + '.'
            if ieditor == 0:
                editors = this_editor['family'] + ' ' + initials
            elif ieditor + 1 == len(publication['editor']):
                editors += ' & ' + initials + ' ' + this_editor['family']
            else:
                editors += ', ' + initials + ' ' + this_editor['family']

        page_string += chapter_string.format(authors=authors, publication_year=publication_year, title=title, book=book, editors=editors, publisher=publisher, isbn=isbn)

page_string += """

----

"""

print(page_string)

output_file = '../dart-web/content/publications/_index.md'

f = open(output_file, 'w')
f.write(page_string)
f.close()
