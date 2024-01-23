#! /opt/local/bin/python

import json
from collections import OrderedDict

f = open('dart-web.json')

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

This list gets updated as frequently as possible, however some more
recent publications may also be available on the UCAR/NCAR online
database [Opensky](https://opensky.ucar.edu/).
Simply use it and search for "ensemble data assimilation" (for
example). Many, if not most, are related to DART. The following list
also contains some publications from our collaborators. If you would
like to list your publication that uses DART, please let us know!
(dart@ucar.edu)

Please use the folowing to cite DART:

> The Data Assimilation Research Testbed (Version X.Y.Z) [Software]. (2019). Boulder, Colorado: UCAR/NCAR/CISL/DAReS. [http://doi.org/10.5065/D6WQ0202](http://doi.org/10.5065/D6WQ0202)  

Update the DART version and year as appropriate.

The seminal reference is:   

**Anderson, J. L., T. Hoar, K. Raeder, H. Liu, N. Collins, R. Torn
and A. Arellano**, 2009  
The Data Assimilation Research Testbed: A Community Facility.  
*Bulletin of the American Meteorological Society*, **90**, 1283-1296,
[doi:10.1175/2009BAMS2618.1](http://dx.doi.org/10.1175/2009BAMS2618.1)

"""

year_header = """
---
{current_year}
---
"""

publication_string = """
![](/images/pin4.gif) **{authors}**, {publication_year}  
    {title}.  
    *{journal}*,{volume}{page}, [{doi}]({url}).
"""

for publication in publications:

    publication_year = publication['issued']['date-parts'][0][0]
    title = publication['title']
    journal = publication['container-title']
    try:
        volume = ' **' + publication['volume']+'**, '
    except:
        volume = ' '
    try:
        page = publication['page']+', '
    except:
        page = ' '
    
    doi = 'doi.org/' + publication['DOI']
    url = 'https://' + doi

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
            authors = initials + ' ' + this_author['family']
        else:
            authors += ', ' + this_author['family'] + ' ' + initials
    
    page_string += publication_string.format(authors=authors, publication_year=publication_year, title=title, journal=journal, volume=volume, page=page, doi=doi, url=url)
    
print(page_string)
    