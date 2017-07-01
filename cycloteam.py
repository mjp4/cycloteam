import velogames
import cyclingnews
from pprint import pprint

from library import fuzzy_value

results_table = list()

riders, scores = zip(*velogames.rider_table(2014, 'tour-de-france'))

results_table = [list() for r in riders]

for event, results in cyclingnews.all_candidate_results(2016):
    print(event)

    for i in range(len(results_table)):
        try:
            results_table[i].append(results[riders[i]])
        except KeyError:
            results_table[i].append(999)

pprint(list(zip(scores, riders, results_table)))
