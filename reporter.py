import csv
import json
import os
import datetime

with open('config.json', 'r') as f:
    config = json.load(f)

def write_exact_matches(exact_matches):
    filepath = config['output']['exact_match_filepath']
    encoding = config['output']['encoding']
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not exact_matches:
        with open(filepath, 'w', newline='', encoding=encoding) as f:
            writer = csv.DictWriter(f, fieldnames=['case_id',
                     'input_name', 'matched_name', 'score',
                     'sources', 'country'])
            writer.writeheader()
            print(f'   [OUTPUT] No exact matches yet, Empty file created:{filepath}')
        return
    with open(filepath, 'w', newline='', encoding=encoding) as f:
        fieldnames = ['case_id', 'input_name', 'matched_name', 'score', 'sources', 'country']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for match in exact_matches:
            writer.writerow(match)
    print(f'     [OUTPUT]  exact matches written: {filepath} ({len(exact_matches)} rows)')


def write_partial_matches(partial_matches):
    filepath = config['output']['partial_match_filepath']
    encoding = config['output']['encoding']
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not partial_matches:
        with open(filepath, 'w', newline='', encoding=encoding) as f:
            writer = csv.DictWriter(f, fieldnames=['case_id', 'input_name', 'matched_name', 'score', 'sources', 'country'])
            writer.writeheader()
            print(f'     [OUTPUT] no partial matches. empty file created {filepath} ')
        return
    with open(filepath, 'w', newline='', encoding=encoding) as f:
        fieldnames = ['case_id', 'input_name', 'matched_name', 'score', 'sources', 'country']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for match in partial_matches:
            writer.writerow(match)
    print(f'       [OUTPUT]  Partial matches written: {filepath} ({len(partial_matches)} rows)')


def write_summary(exact_matches, partial_matches, watchlist_count, sanctions_count):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    summary_folder = 'data/output'
    os.makedirs(summary_folder, exist_ok=True)
    summary_filepath = f'{summary_folder}/screening_summary.txt'
    with open(summary_filepath, 'w', encoding='utf-8') as f:
        f.write('=' * 60 + '\n')
        f.write('     SANCTIONS SCREENING SUMMARY REPORT\n')
        f.write('=' * 60 + '\n\n')

        f.write(f'generated   : {timestamp}\n')
        f.write(f'watchlist   : {watchlist_count} entries screened\n')
        f.write(f'Sanctions   : {sanctions_count} sanctioned entries checked \n')
        f.write(f'exact matches: {len(exact_matches)}\n')
        f.write(f'partial matches:{len(partial_matches)}\n\n')
        if exact_matches:
            f.write('=' * 60 + '\n')
            f.write('EXACT MATCHES\n')
            f.write('=' * 60 + '\n')
            for match in exact_matches:
                f.write(f'    CASE ID     :{match["case_id"]}\n')
                f.write(f'    INPUT       :{match["input_name"]}\n')
                f.write(f'    MATCHED     :{match["matched_name"]}\n')
                f.write(f'    SCORE       :{match["score"]}\n')
                f.write(f'    SOURCE      :{match["sources"]}\n')
                f.write(f'    COUNTRY     :{match["country"]}\n')
        if partial_matches:
            f.write('=' * 60 + '\n')
            f.write('PARTIAL MATCHES\n')
            f.write('=' * 60 + '\n')
            for match in partial_matches:
                f.write(f'    CASE ID     :{match["case_id"]}\n')
                f.write(f'    INPUT       :{match["input_name"]}\n')
                f.write(f'    MATCHED     :{match["matched_name"]}\n')
                f.write(f'    SCORE       :{match["score"]}\n')
                f.write(f'    SOURCE      :{match["sources"]}\n')
                f.write(f'    COUNTRY     :{match["country"]}\n')
                f.write('\n')
        f.write('=' * 60 + '\n')
        f.write('end of report\n')
        f.write('=' * 60 + '\n')
    print(f'   [OUTPUT] Summary written :{summary_filepath}')


def run_reporter(exact_matches, partial_matches, watchlist_count, sanctions_count):
    write_exact_matches(exact_matches)
    write_partial_matches(partial_matches)
    write_summary(exact_matches, partial_matches, watchlist_count, sanctions_count)
    print('\n ---- ALL REPORTS COMPLETE---')
    print(f'       CHECK data/output/ for your results')


if __name__ == '__main__':
    from loader import load_watchlist, load_all_sanctions
    from matcher import run_screening

    print('--- Loading Data ---')
    watchlist = load_watchlist()
    sanctions = load_all_sanctions()

    print('--- Running Screening ---')
    exact_matches, partial_matches = run_screening(watchlist, sanctions)

    print('--- Running Reporter ---')
    run_reporter(
        exact_matches,
        partial_matches,
        watchlist_count=len(watchlist),
        sanctions_count=len(sanctions)
    )
    
    


            



    