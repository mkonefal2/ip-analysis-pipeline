import geoip2.database
import duckdb
import csv
import os

# Ścieżki do plików
GEOIP_DB = os.path.join(os.path.dirname(__file__), '../GeoLite2-Country.mmdb')
DUCKDB_FILE = os.path.join(os.path.dirname(__file__), '../data/blocklist.duckdb')

def enrich_geoip(input_file='../data/blocklist.csv'):
    reader = geoip2.database.Reader(GEOIP_DB)
    conn = duckdb.connect(DUCKDB_FILE)

    # Tworzenie tabeli z klauzulą UNIQUE dla ip_address
    conn.execute("""
    CREATE TABLE IF NOT EXISTS blocklist (
        ip_address VARCHAR,
        country VARCHAR,
        country_code VARCHAR,
        UNIQUE(ip_address)
    )
    """)

    # Pobranie istniejących IP (jedno zapytanie)
    existing_ips = set(conn.execute("SELECT ip_address FROM blocklist").fetchdf()['ip_address'])

    # Przygotowanie danych do wsadowego wstawienia
    data_to_insert = []

    with open(input_file, 'r') as infile:
        csv_reader = csv.reader(infile)
        next(csv_reader)  # Pominięcie nagłówka

        for row in csv_reader:
            ip = row[0]

            if ip not in existing_ips:  # Sprawdzenie w pamięci (set)
                try:
                    response = reader.country(ip)
                    country = response.country.name or "Unknown"
                    country_code = response.country.iso_code or "Unknown"
                except:
                    country, country_code = "Unknown", "Unknown"

                data_to_insert.append((ip, country, country_code))

    # Masowe wstawienie danych (UPSERT - bez duplikatów)
    if data_to_insert:
        conn.executemany("""
        INSERT INTO blocklist (ip_address, country, country_code)
        VALUES (?, ?, ?)
        ON CONFLICT (ip_address) DO NOTHING
        """, data_to_insert)

        print(f"[INFO] Dodano {len(data_to_insert)} nowych adresów IP.")
    else:
        print("[INFO] Brak nowych adresów IP do dodania.")

    reader.close()
    conn.close()
    print("[INFO] Dane wzbogacone i zapisane do DuckDB.")

if __name__ == "__main__":
    enrich_geoip()
