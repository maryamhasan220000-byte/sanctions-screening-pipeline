import csv
import json
import os

with open('config.json', 'r') as f:
    config = json.load(f)

def load_watchlist():
    filepath = config['input']['filepath']
    encoding = config['input']['encoding']
    name_column = config['input']['name_column']
    min_length = config['input']['skip_below_length']
    watchlist = []

    try:
        with open(filepath, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get(name_column, '').strip()
                if not name:
                    print(f'[skip] empty name in row:{row}')
                    continue
                if len(name) < min_length:
                    print(f'[skip] name too short:{name}')
                    continue
                watchlist.append({
                    'name': name,
                    'country': row.get('country', '').strip(),
                    'case_id': row.get('case_study', '').strip()
                })
    except FileNotFoundError:
        print(f"[ERROR] watchlist file not found:{filepath}")
    except UnicodeDecodeError:
        print(f'[ERROR] encoding error reading watchlist')
    return watchlist


def load_sanctions_list(source_key):
    source = config['data_sources'][source_key]
    filepath = source['filepath']
    encoding = source['encoding']
    name_col = source['name_column_index']
    label = source['label']
    sanctioned_list = []

    try:
        with open(filepath, 'r', encoding=encoding) as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > name_col:
                    name = row[name_col].strip()
                    if name and name != '-0-':
                        sanctioned_list.append({
                            'name': name,
                            'source': label
                        })
    except FileNotFoundError:
        print(f'    [ERROR] sanctions file not found{filepath}')
    except UnicodeDecodeError:
        print(f'    [ERROR] encoding error reading{label}')
    return sanctioned_list


def load_all_sanctions():
    all_sanctioned = []
    for source_key, source_config in config['data_sources'].items():
        if source_config['enabled']:
            print(f'[LOADING]{source_config["label"]}.....')
            name = load_sanctions_list(source_key)
            all_sanctioned.extend(name)
            print(f"  [LOADED]{len(name)} entries from {source_config['label']}")
    return all_sanctioned


if __name__ == '__main__':
    print('\n------Loading Watchlist-------')
    watchlist = load_watchlist()
    print(f'Valid name to screen:{len(watchlist)}')
    for entry in watchlist:
        print(f'   {entry["case_id"]}: {entry["name"]}')
    print('\n------LOADING SANCTIONS LIST')
    sanctions = load_all_sanctions()

                       


                    
       
