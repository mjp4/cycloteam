from pprint import pprint
from bs4 import BeautifulSoup
import re

from library import get_with_cache, normalise_name

def download_scores(year, race):
    return get_with_cache(
        "https://www.velogames.com/{race}/{year}/ridescore.php".format(
            year=year, race=race),
        "cache/riders_{race}-{year}".format(
            race=race, year=year))


def rider_table(year, race):
    page_text = download_scores(year, race)
    soup = BeautifulSoup(page_text)
    if year == 2014:
        for tr in soup.find('div', class_='content').tbody.find_all('tr'):
            tds = tr.find_all('td')
            yield (normalise_name(tds[1].string, filter_add=(year, race)),
                    tds[4].string)
    else:
        for li in soup.find('div', id='users').find_all('li'):
            yield (normalise_name(li.h3.string, filter_add=(year, race)),
                    re.sub('[^\d]', '', li.b.string))
