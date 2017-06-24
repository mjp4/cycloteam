from bs4 import BeautifulSoup
import requests

def download_scores(year, race):
    try:
        with open("cache/riders_{race}-{year}".format(
                race=race, year=year), 'r') as f:
            return f.read()
    except OSError:
        page = requests.get("https://www.velogames.com/{race}/{year}/riders.php".format(year=year, race=race))
        with open("cache/riders_{race}-{year}".format(
                race=race, year=year), 'w') as f:
            f.write(page.text)
        return page.text

def rider_table(page_text):
    soup = BeautifulSoup(page_text)
    for tr in soup.find('div', class_='content').tbody('tr'):
        tds = tr.find_all('td')
        yield (tds[1].string, tds[4].string)

def normalise_name(name):
    return name.partition("(")[0].rstrip()

from pprint import pprint



pprint(dict(rider_table(download_scores(2014, 'tour-de-france'))))
