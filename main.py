import json
import time
from datetime import datetime
from loader import load_watchlist, load_all_sanctions
from matcher import run_screening
from reporter import run_reporter
from logger import write_log

def print_header():
    print('\n' + "=" * 60)
    print('     SANCTIONS SCREENING PIPELINE')
    print('     Version 1.0.0')
    print(f'    STARTED: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('='* 60 + '\n')
def print_summary(watchlist_count, sanctions_count, exact_matches, partial_matches, duration_seconds):
    print('\n' + '=' * 60)
    print('     SCREENING COMPLETED')
    print('=' * 60)
    print(f'     Names screened     :{watchlist_count}')
    print(f'     Sanctions checked  :{sanctions_count}')
    print(f'     exact matches found:{len(exact_matches)}')
    print(f'     Partial matches found:{len(partial_matches)}')
    print(f'     time taken : {round(duration_seconds, 2)} seconds')
    print('='* 60)
    if exact_matches:
        print('\n HIGH PRIORITY - EXACT MATCHES')
        for m in exact_matches:
            print(f'    {m['case_id']} | {m['input_name']} | {m['matched_name']}')
            print(f'     SCORE:{m['score']} | SOURCES: {m['sources']}')
    if partial_matches:
        print('\n REVIEW REQUIRED - PARTIAL MATCHES')
        for m in partial_matches:
            print(f'    {m['case_id']} | {m['input_name']} | {m['matched_name']}')
            print(f'     SCORE:{m['score']} | SOURCES: {m['sources']}')
    if not exact_matches and partial_matches:
        print('\n NO MATCHES FOUND. ALL NAMES CLEAR')
    print("\n   Output files:")
    print("   data/output/exact_matches.csv")
    print("   data/output/partial_matches.csv")
    print("   data/output/screening_summary.txt")
    print("   logs/screening_log.json")
    print()
def run_pipeline():
    print_header()
    start_time = time.time()
    try:
        print('STEP1: Loading Data')
        print('=' * 40)
        watchlist = load_watchlist()
        sanctions = load_all_sanctions()
        if not watchlist:
            print('[ABORT] watchlist is empty. nothing to screen ')
        if not sanctions:
            print('[ABORT] no sanctions data loaded. check config')
            return
        print(f'READY: {len(watchlist)} names to screen')
        print(f'READY: {len(sanctions)} sanctioned entries loaded\n')

        print('STEP 2: Running screening')
        print('=' * 40)
        exact_matches, partial_matches = run_screening(watchlist, sanctions)
        print(f'\n SCREENING DONE')
        print(f'   exact matches : {len(exact_matches)}')
        print(f'   partial matches: {len(partial_matches)}')

        print('STEP 3: Genrating Reports')
        print('='* 40)
        run_reporter(exact_matches, partial_matches,watchlist_count= len(watchlist), sanctions_count= len(sanctions))
        
        print('STEP 4: Writing audit log')
        print('=' * 40)
        write_log(exact_matches, partial_matches, watchlist_count=len(watchlist), sanctions_count=len(sanctions))
        end_time = time.time()
        duration = end_time - start_time
        print_summary(watchlist_count=len(watchlist), sanctions_count=len(sanctions), exact_matches=exact_matches, partial_matches=partial_matches, duration_seconds=duration)
    except Exception as e:
        print(f' \n [CRITICALERROR] pipleine failed: {str(e)}')
        raise 
if __name__ == '__main__':
    run_pipeline()


    
