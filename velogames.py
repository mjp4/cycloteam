from pprint import pprint
from bs4 import BeautifulSoup

from library import get_with_cache, normalise_name

def download_scores(year, race):
    return get_with_cache(
        "https://www.velogames.com/{race}/{year}/riders.php".format(
            year=year, race=race),
        "cache/riders_{race}-{year}".format(
            race=race, year=year))


def rider_table(year, race):
    page_text = download_scores(year, race)
    soup = BeautifulSoup(page_text)
    for tr in soup.find('div', class_='content').tbody('tr'):
        tds = tr.find_all('td')
        yield (normalise_name(tds[1].string, filter_add=(year, race)),
                tds[4].string)
