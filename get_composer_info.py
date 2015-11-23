"""Reads an html table detailing classical composers on wikipedia and stores data in an sqlite db. 
Links are given below."""

from bs4 import BeautifulSoup
import urllib
import sqlite3
import sys


def get_data(link):
    """Yields a tuple consisting of composer info. (name, link, dob, dod, origin)."""

    html = urllib.urlopen(link)
    file_ = html.read()
    soup = BeautifulSoup(file_, 'html.parser')
    soup.prettify()

    name = ''
    link = ''
    dob = ''
    dod = ''
    origin = ''

    for row in soup.find_all('tr'):

        if len(row.contents) == 11:  # unique number of contents to desired table

            columns = row.find_all('td')  

            for i, column in enumerate(columns):
                column = repr(column)

                if i == 0:
                    _, _, link_ = column.partition('<td><a href="')
                    link, _, _, = link_.partition('" ')

                    _, _, name_ = column.partition('">')
                    name, _, _, = name_.partition('</a>')

                if i == 1:
                    if column[:26] == '<td><span class="sortkey">':
                        _, _, dob_ = column.partition('class="sortkey">')
                        dob, _, _, = dob_.partition('</span')

                    else:
                        _, _, dob_ = column.partition('<td>')
                        dob, _, _, = dob_.partition('</td>')

                if i == 2:
                    if column[:26] == '<td><span class="sortkey">':
                        _, _, dod_ = column.partition('class="sortkey">')
                        dod, _, _, = dod_.partition('</span')

                    else:
                        _, _, dod_ = column.partition('<td>')
                        dod, _, _, = dod_.partition('</td>')

                if i == 3:
                    _, _, origin_ = column.partition('<td>')
                    origin, _, _, = origin_.partition('</td>')

                if i == 4:
                    yield name, link, dob, dod, origin

def main():
    "Main function. Saves to Sqlite database"
        connection = sqlite3.connect('test.db')

    with connection:

        cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS composer')
        cursor.execute(
            'CREATE TABLE composer(Name TEXT, Link TEXT, DOB TEXT, DOD TEXT, Origin TEXT)')

        for link in links:
            cursor.executemany(
                "INSERT INTO composer VALUES (?,?,?,?,?)", get_data(link))


if __name__ == '__main__':

    links = [
        'https://en.wikipedia.org/wiki/List_of_Medieval_composers#Early_medieval_composers_.28born_before_1150.29',
        'https://en.wikipedia.org/wiki/List_of_Medieval_composers#Middle_medieval_composers_.28born_1150.E2.80.931300.29',
        'https://en.wikipedia.org/wiki/List_of_Medieval_composers#Late_medieval_and_transitional_composers_.28born_1300.E2.80.931400.29',
        'https://en.wikipedia.org/wiki/List_of_Romantic-era_composers'
    ]

    main()
