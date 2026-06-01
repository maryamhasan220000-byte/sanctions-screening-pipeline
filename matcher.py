import json
import string
from difflib import SequenceMatcher

with open('config.json','r') as f:
    config = json.load(f)
    def clean_name(name):
        name = name.lower()
        if config['matching']['strip_punctuation']: 
            name = name.translate(
                str.maketrans('','', string.punctuation))
        name = ' '.join(name.split())
        return name
    
    def get_similarity(name_a, name_b):
        return SequenceMatcher(None, name_a, name_b).ratio()
    def match_name(input_entry, sanctioned_list):
        exact_threshold = config['matching']['exact_match_threshold']
        partial_threshold = config['matching']['partial_match_threshold']
        input_name_raw = input_entry['name']
        input_name_clean = clean_name(input_name_raw)
        exact_matches=[]
        partial_matches =[]
        for sanctioned_entry in sanctioned_list:
            sanctioned_name_raw = sanctioned_entry['name']
            sanctioned_name_clean = clean_name(sanctioned_name_raw)
            score = get_similarity(input_name_clean, sanctioned_name_clean)
            if score >= exact_threshold:
                exact_matches.append({
                    'case_id': input_entry['name'],
                    'input_name': input_name_raw,
                    'matched_name': sanctioned_name_raw,
                    'score': round(score, 4),
                    'sources': sanctioned_entry['source'],
                    'country': input_entry['country'] })
            elif score >= partial_threshold:
                partial_matches.append({
                    'case_id': input_entry['name'],
                    'input_name': input_name_raw,
                    'matched_name': sanctioned_name_raw,
                    'score': round(score, 4),
                    'sources': sanctioned_entry['source'],
                    'country': input_entry['country'] })
        return exact_matches, partial_matches
    def run_screening(watchlist, sanctioned_list):
        all_exact=[]
        all_partial=[]
        total = len(watchlist)
        for i, entry in enumerate(watchlist, start=1):
            print(f'      [SCREENING] {i}/{total}:{entry['name']}' )
            exact, partial = match_name(entry, sanctioned_list)
            if exact:
                print(f'     [EXACT MATCH FOUND] {len(exact)} matche(es)')
            if partial:
                print(f'     [PARTIAL MATCH FOUND] {len(partial)} match(es)')

                all_exact.extend(exact)
                all_partial.extend(partial)
        return all_exact, all_partial
    if __name__ == '__main__':
        from loader import load_watchlist, load_all_sanctions
        print("\n--- Loading Data ---")
        watchlist = load_watchlist()
        sanctions = load_all_sanctions()

        print("\n--- Starting Screening ---")
        print(f"Names to screen: {len(watchlist)}")
        print(sanctions)
        print(type(sanctions))
        print(f"Sanctioned entries: {len(sanctions)}")
        print()

        exact_matches, partial_matches = run_screening(
        watchlist,
        sanctions )

        print("\n--- Screening Complete ---")
        print(f"Exact matches found: {len(exact_matches)}")
        print(f"Partial matches found: {len(partial_matches)}")

        if exact_matches:
            print("\nEXACT MATCHES:")
            for m in exact_matches:
                print(
                f"{m['case_id']} | "
                f"{m['input_name']} -> "
                f"{m['matched_name']} | "
                f"Score: {m['score']} | "
                f"{m['sources']}"
            )
        if partial_matches:
             print("\nPARTIAL MATCHES:")
             for m in partial_matches:
                 print(
                f"{m['case_id']} | "
                f"{m['input_name']} -> "
                f"{m['matched_name']} | "
                f"Score: {m['score']} | "
                f"{m['sources']}"
            )
            
       
                

   
           
    
        

   

    
    
        

                


            
            