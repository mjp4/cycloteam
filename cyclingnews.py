from bs4 import BeautifulSoup
import requests

def download_results(year, race, stage):
    try:
        with open("cache/{race}-{year}_{stage}".format(
                race=race, year=year, stage=stage), 'r') as f:
            return f.read()
    except OSError:
        page = requests.get("http://www.cyclingnews.com/races/{race}-{year}/{stage}/results".format(year=year, race=race, stage=stage))
        with open("cache/{race}-{year}_{stage}".format(
                race=race, year=year, stage=stage), 'w') as f:
            f.write(page.text)
        return page.text

def result_tables(page_text):
    soup = BeautifulSoup(page_text)
    for div_results in soup.find_all("div", class_="results"):
        caption = div_results.caption.string if div_results.caption else "Stage"
        yield (caption, dict(tbody2seq(div_results.tbody)))

def normalise_name(name):
    return name.partition("(")[0].rstrip()

def tbody2seq(tbody):
    for tr in tbody.find_all('tr'):
        if tr.td:
            try:
                rank = int(tr.td.string)
            except ValueError:
                continue
            name = normalise_name(tr.td.next_sibling.string)
            yield (name, rank)

selected_races = [
        (0, "criterium-du-dauphine", 8, {2016})
        ]

def all_candidate_results(tdf_year):
    for selected_race in selected_races:
        year = tdf_year + selected_race[0]
        race = selected_race[1]
        if selected_race[2] > 1:
            if year in selected_race[3]:
                stages = (['prologue'] +
                          ['stage-' + str(n) for n in range(1, selected_race[2])])
            else:
                stages = ['stage-' + str(n) for n in range(1, selected_race[2] + 1)]

            print(stages)
            for stage in stages:
                stage_page = download_results(year, race, stage)
                stage_results = dict(result_tables(stage_page))
                print(stage_results.keys())
                if "Stage" in stage_results:
                    yield ("{race}-{year}_{stage}".format(race=race, stage=stage, year=year),
                            stage_results["Stage"])
                if "Mountains classification" in stage_results:
                    yield ("{race}-{year}_mountain".format(race=race, stage=stage, year=year),
                            stage_results["Mountains classification"])
                if "Points classification" in stage_results:
                    yield ("{race}-{year}_point".format(race=race, stage=stage, year=year),
                            stage_results["Points classification"])
                if "Final general classification" in stage_results:
                    yield ("{race}-{year}_gc".format(race=race, stage=stage, year=year),
                            stage_results["Final general classification"])

from pprint import pprint

pprint(dict(all_candidate_results(2016)))
