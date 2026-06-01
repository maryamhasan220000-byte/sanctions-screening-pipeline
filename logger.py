import json
import os
from datetime import datetime
with open('config.json', 'r') as f:
    config = json.load(f)
    def get_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def load_existing_log(filepath):
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    
                    return json.load(f)
            except json.JSONDecodeError:
                print('[WARNING] Log file was corrupted. Startimg fresh')
                return[]
        return[]
    def build_log_entry( exact_matches, partial_matches, watchlist_count, sanctions_count, status= 'SUCCESS'):
        return{ 'timestamp': get_timestamp(),
                 'pipeline_name': config['pipeline']['name'],
                 'pipeline_version': config['pipeline']['version'],
                 'status': status,
                 'screening_summary': {
                     'watchlist_count': watchlist_count,
                     'sanctions_count': sanctions_count,
                     'exact_matches': len(exact_matches),
                     'partial_matches': len(partial_matches)},
                 'exact_matches': [{
                         'case_id': m['case_id'],
                         'input_name': m['input_name'],
                         'matched_name': m['matched_name'],
                         'score': m['score'],
                         'sources': m['sources'],
                         'country': m['country']}
                         for m in exact_matches],
                 'partial_matches':[{
                            'case_id': m['case_id'],
                         'input_name': m['input_name'],
                         'matched_name': m['matched_name'],
                         'score': m['score'],
                         'sources': m['sources'],
                         'country': m['country']}
                         for m in partial_matches]}
    def write_log(exact_matches, partial_matches, watchlist_count, sanctions_count):
        filepath = config['logging']['filepath']
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        existing_log = load_existing_log(filepath)
        new_entry = build_log_entry(exact_matches, partial_matches, watchlist_count, sanctions_count)
        existing_log.append(new_entry)
        with open(filepath,'w', encoding= 'utf-8' ) as f:
            json.dump(existing_log, f, indent=4, ensure_ascii=False)
        print(f'     [log] run logged successfully:{filepath}')
        print(f'     [log] total runs recorded:{len(existing_log)}')
    if __name__ == '__main__':
        from loader import load_watchlist, load_all_sanctions
        from matcher import run_screening

        print("\n--- Loading Data ---")
        watchlist = load_watchlist()
        sanctions = load_all_sanctions()

        print("\n--- Running Screening ---")
        exact_matches, partial_matches = run_screening(watchlist, sanctions)

        print("\n--- Writing Log ---")
        write_log(
        exact_matches,
        partial_matches,
        watchlist_count=len(watchlist),
        sanctions_count=len(sanctions)
    )

    print("\n--- Done. Check logs/screening_log.json ---")
   
    


                            

                        
                     
                     
                    
    

                     
                 
               
                 
            

            
    
