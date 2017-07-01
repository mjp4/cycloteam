from fuzzywuzzy import process, fuzz
import requests

from unidecode import unidecode

def get_with_cache(url, cache_path):
    try:
        with open(cache_path, 'r') as f:
            return f.read()
    except OSError:
        page = requests.get(url)
        with open(cache_path, 'w') as f:
            f.write(page.text)
        return page.text


def fuzzy_value(fuzzy_dict, fuzzy_key):
    return fuzzy_dict[fuzzy_name_match(fuzzy_dict.keys(), fuzzy_key)]


def fuzzy_name_match(fuzzy_set, name):
    normalised_name = process.extractOne(
            name, fuzzy_set, scorer=fuzz.partial_token_sort_ratio)
    if normalised_name[1] < 86:
        raise KeyError()
    elif normalised_name[1] < 90:
        print("Potential fuzzy match not used {} == {} ({})".format(
                normalised_name[0], name, normalised_name[1]))
        raise KeyError()
    elif normalised_name[1] < 95:
        print("Fuzzy matched {} == {} ({})".format(
                normalised_name[0], name, normalised_name[1]))
    return normalised_name[0]


name_filter = set()
normalised_names = dict()
def normalise_name(name, filter_add=False, filter_apply=False):
    name = name.partition("(")[0].rstrip()
    name = unidecode(name)
    if filter_add:
        name_filter.add(name)

    if name in normalised_names:
        return normalised_names[name]
    elif filter_apply:
        try:
            if name in name_filter:
                matched_name = name
            else:
                matched_name = fuzzy_name_match(name_filter, name)
            normalised_names[name] = matched_name
            return matched_name
        except KeyError:
            normalised_names[name] = None
            return None
    else:
        return name

