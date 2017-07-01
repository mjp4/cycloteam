import velogames
import cyclingnews
from pprint import pprint

from library import fuzzy_value

def get_initial_data(years):
    for year in years:
        riders, scores = zip(*list(velogames.rider_table(year, 'tour-de-france')))

        results_table = [list() for r in riders]

        for event, results in cyclingnews.all_candidate_results(year):
            print(event)

            for i in range(len(results_table)):
                try:
                    results_table[i].append(results[riders[i]])
                except KeyError:
                    results_table[i].append(999)


        yield scores, riders, results_table

all_scores, all_riders, all_results_table = list(), list(), list()

for scores, riders, results_table in get_initial_data([2014, 2015, 2016]):
    all_scores.extend(scores)
    all_riders.extend(riders)
    all_results_table.extend(results_table)

pprint(list(zip(all_scores, all_riders, all_results_table)))
