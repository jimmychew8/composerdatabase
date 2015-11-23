"""Returns a public domain composer's works from the IMLSP databse."""

from bs4 import BeautifulSoup
import urllib2
import re
import sqlite3 as lite
import sys


def double_partition(string, start, end):
    """Returns the desired string between 'start' and 'end', but not including 'start' and 'end'."""

    _, _, string = string.partition(start)
    string, _, _ = string.partition(end)

    return string


def find_composer(soup):
    """Returns composer's first and last name from soup from <title> tag."""

    title = soup.html.head.title.string
    composer_name, _, _ = title[9:].partition(' - IMSLP/Petrucci')
    last, _, first = composer_name.partition(',')

    return first.strip() + ' ' + last.strip()


def find_works(soup):
    """Yields the title of each composition and url path where we can find details about each work."""

    # Iterates through all <li> tags. Stops at the tag detailing the number of compositions.
    # Iterates through the subsequent tags until all compositions are found.

    works = soup.find_all('li')

    count = None
    end = 0

    for work in works:

        number_works = None
        pattern = re.compile(r'Compositions \(\d*\)')

        if re.search(pattern, str(work)):

            result = re.findall(pattern, str(work))

            if len(result) > 0:

                works_string, _, _ = result[0].partition(')')
                _, _, number_works = works_string.partition('(')

                count = 0
                end = int(number_works)

                print 'Number of works on IMSLP: {}'.format(end)

        if count <= end and isinstance(count, int):

            pattern = re.compile(r'href="/wiki')
            exist_work_info = re.findall(pattern, str(work))

            # <li> not containing information about a composition
            if not exist_work_info:

                end += 1
                count += 1
            # Clean what you yield before you yield it. 
            yield work

        if count >= end:

            break


def find_work_details(path):
    """Returns a tuple that details the date of completion, style, key, genre, language of the work as specificed by the path.
    The path that is taken as argument should lead to the specific page on IMLSP that gives details on the work."""

    root = 'http://imslp.org'
    url = root + path

    f = urllib2.urlopen(url)
    f_ = f.read()
    soup = BeautifulSoup(f_, 'html.parser')
    soup.prettify()

    title = None
    date_completion = None
    instrumentation = None
    style = None
    key = None
    opus = None
    language = None

    rows = soup.find_all('tr')

    # Enumerate for debugging purposes

    for count, row in enumerate(rows):

        headers = row.find_all('th')
        values = row.find_all('td')

        if len(headers) > 0:

            if str(headers[0]) == '<th>Work Title\n</th>':

                title = double_partition(str(values[0]), '<td>', '</td>')

            if str(headers[0]) == '<th>Composition Year\n</th>':

                date_completion = double_partition(
                    str(values[0]), '<td>', '</td>')

            if str(headers[0]) == '<th>Instrumentation\n</th>':

                instrumentation = double_partition(
                    str(values[0]), '<td>', '</td>')

            if str(headers[0]) == '<th>Piece Style\n</th>':

                style = double_partition(str(values[0]), '">', '</a>')

            if str(headers[0]) == '<th>Key\n</th>':

                key = double_partition(str(values[0]), '<td>', '</td>')

            if str(headers[0]) == '<th>Opus/Catalogue Number\n</th>':

                opus = double_partition(str(values[0]), '<td>', '</td>')

            if str(headers[0]) == '<th>Language\n</th>':

                language = double_partition(str(values[0]), '<th>', '</th>')

    return title, date_completion, instrumentation, style, key, opus, language


def collect_findings_for_composer(first_name, last_name):
    """Returns a tuple consisting of work details of the specific composer taken as argument."""

    base = 'http://imslp.org/wiki/Category:'
    url = base + last_name.strip().title() + ',_' + first_name.strip().title()
    print url

    f = urllib2.urlopen(url)
    f_ = f.read()
    soup = BeautifulSoup(f_, 'html.parser')

    composer = find_composer(soup)
    work_list = list(find_works(soup))

    for i, work in enumerate(work_list[1:]):

        w = re.findall(r'href=".*?\)|">.*?\s\(', str(work), re.DOTALL) # url to find work details and title of work

        if len(w) == 2:

            path = w[0][6:]

            title, date_completion, instrumentation, style, key, opus, language = find_work_details(path)

            yield title, date_completion, instrumentation, style, key, opus, language, path, composer


def clean(string):
    """Returns a clean version of string for use in database."""


def main(first_name, last_name):
    """Main function. Handles scraping for data and writing to the Work database."""

    conn = lite.connect('Work.db')
    conn.text_factory = str

    data = list(collect_findings_for_composer(first_name, last_name))

    for d in data:

        print d

    with conn:

        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS Works')
        cursor.execute(
            'CREATE TABLE Works(Title TEXT, Date_Completion TEXT, Instrumentation TEXT, Style TEXT, Key TEXT, Opus TEXT, Language TEXT, Url TEXT, Composer TEXT)')
        cursor.executemany(
            'INSERT INTO Works VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', data)


if __name__ == '__main__':

    if not len(sys.argv) == 3:

        print '>>>Error must have 2 arguments: first name, last name.'

    else:

        main(sys.argv[1], sys.argv[2])
