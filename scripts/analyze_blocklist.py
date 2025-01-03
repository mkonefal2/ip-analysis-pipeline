import pandas as pd
import os

def analyze_blocklist(enriched_file='../data/blocklist_enriched.csv', output_report='../data/blocklist_report.csv'):
    enriched_file = os.path.abspath(os.path.join(os.path.dirname(__file__), enriched_file))
    output_report = os.path.abspath(os.path.join(os.path.dirname(__file__), output_report))
    
    if not os.path.exists(enriched_file):
        # Tworzenie pustego pliku CSV z nagłówkami
        df_empty = pd.DataFrame(columns=['country', 'region'])
        df_empty.to_csv(enriched_file, index=False)
        print(f"[INFO] Utworzono pusty plik: {enriched_file}")
    
    df = pd.read_csv(enriched_file)
    grouped = df.groupby(['country', 'region']).size().reset_index(name='count')
    grouped.to_csv(output_report, index=False)
    print(f"[INFO] Raport zapisany do {output_report}.")
    return grouped

if __name__ == "__main__":
    analyze_blocklist()