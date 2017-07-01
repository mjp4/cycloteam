from bs4 import BeautifulSoup
from fuzzywuzzy import process, fuzz

from library import get_with_cache, fuzzy_value, normalise_name

def download_results(year, race, stage):
    return get_with_cache(
            "http://www.cyclingnews.com/races/{race}-{year}/{stage}/results/".format(
                race=race, year=year, stage=stage),
            "cache/{race}-{year}_{stage}".format(
                race=race, year=year, stage=stage))


def result_tables(page_text):
    soup = BeautifulSoup(page_text)
    for div_results in soup.find_all("div", class_="results"):
        caption = div_results.caption.string if div_results.caption else "Stage"
        yield (caption, dict(tbody2seq(div_results.tbody)))


def tbody2seq(tbody):
    for tr in tbody.find_all('tr'):
        tds = tr.find_all('td')
        if tds:
            try:
                rank = int(tds[0].string)
            except ValueError:
                continue
            name = normalise_name(tds[1].string, filter_apply=True)
            if name is not None:
                yield (name, rank)

selected_races = [
        (0, "criterium-du-dauphine", 8, {2016}),
        (0, "tour-de-suisse", 9, set())
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

            for stage in stages[:-1]:
                stage_page = download_results(year, race, stage)
                stage_results = dict(result_tables(stage_page))
                yield ("{race}-{year}_{stage}".format(race=race, stage=stage, year=year),
                        stage_results["Stage"])
            stage = stages[-1]
            stage_page = download_results(year, race, stage)
            stage_results = dict(result_tables(stage_page))
            yield ("{race}-{year}_{stage}".format(race=race, stage=stage, year=year),
                    stage_results["Stage"])
            yield ("{race}-{year}_mountain".format(race=race, stage=stage, year=year),
                    fuzzy_value(stage_results, "Mountains classification", scorer=fuzz.partial_ratio))
            yield ("{race}-{year}_gc".format(race=race, stage=stage, year=year),
                    fuzzy_value(stage_results, "General classification", scorer=fuzz.partial_ratio))
            yield ("{race}-{year}_points".format(race=race, stage=stage, year=year),
                    fuzzy_value(stage_results, "Points classification", scorer=fuzz.partial_ratio))

