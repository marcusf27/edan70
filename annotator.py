import argparse
import keyboard
import time
import json


def convert_keys_to_int(json_dict):

    return {(int(key) if key.isdigit() else key): value
            for key, value in json_dict.items()}


def filter_entries(entries, edition=None, articles=None):

    if edition:
        entries = entries.get(edition, {})

        if articles:
            entries = {article: item for article, item in entries.items()
                       if article in articles}

    return entries


def load_json(path, edition=None, articles=None):

    try:
        with open(path + '.json', 'r', encoding='utf-8') as file:
            return filter_entries(json.load(
                file, object_hook=convert_keys_to_int), edition, articles)

    except (FileNotFoundError, json.JSONDecodeError):
        with open(path + '.json', 'w', encoding='utf-8') as file:
            json.dump({}, file, ensure_ascii=False, indent=4)
        return {}


def save_json(path, entries, edition=None, reset=False, sort_keys=False):

    temp_entries = entries
    entries = ({edition: {}} if edition else {}) if reset else load_json(path)
    entries.setdefault(edition, {})

    (entries[edition] if edition else entries).update(temp_entries)

    try:
        with open(path + '.json', 'w', encoding='utf-8') as file:
            json.dump(entries, file, ensure_ascii=False,
                      indent=4, sort_keys=sort_keys)
    except:
        pass


def parse_range(range_str):

    start, end = map(int, range_str.split('-'))
    return range(start, end + 1)


def main():
    parser = argparse.ArgumentParser(
        description="Example Python script that accepts command-line arguments")

    parser.add_argument(
        '--edition', type=int, help='Edition', required=True)

    parser.add_argument(
        '--articles', type=str, help='Articles in format \'start-end\'',
        required=True)

    args = parser.parse_args()

    edition = args.edition
    articles = parse_range(args.articles)

    entries = load_json('segments', edition, articles)
    last_article = 0
    article = 1

    actions = {
        '1': 'Label as a person',
        '2': 'Label as a location',
        '3': 'Label as other',
        '4': 'Go back one step',
        '5': 'Save',
        '6': 'Exit'
    }

    idx2cat = {
        None: 'Undefined',
        0: 'Person',
        1: 'Location',
        2: 'Other'
    }

    print('Inputs:\n')

    for key, action in actions.items():
        print(f'{key}. {action}')

    exit = False
    
    while (not exit):

        sub_entries = entries[article]

        for i, entry in enumerate(sub_entries):
            text = entry['text']
            label = entry['label']

            if last_article != article:
                print(f"{article}/{len(entries)}:\nText: {text}\nLabel: {label if label else 'Undefined'}\n")

            last_article = article

            key_press = keyboard.read_key()

            if key_press in actions.keys():
                print(f'You chose \'{actions[key_press]}\'\n')

            if key_press in {'1', '2', '3'}:
                entries[article][i]['label'] = idx2cat[int(key_press) - 1]
                article = min(article + 1, len(entries))
                print(article)

            if key_press == '4':
                article = max(article - 1, 1)

            if key_press == '5':
                save_json('segments', entries, edition)

            if key_press == "6":
                exit = True

            time.sleep(0.2)


if __name__ == "__main__":
    main()
