import duckdb

conn = duckdb.connect('data/blocklist.duckdb')

# Sprawdź, co jest w tabeli blocklist
print("Sprawdzam zawartość tabeli blocklist:")
result = conn.execute("SELECT * FROM blocklist").fetchdf()
print(result)

# Analiza - grupowanie po kraju
query = """
SELECT country, COUNT(*) as count
FROM blocklist
GROUP BY country
ORDER BY count DESC
"""

result = conn.execute(query).fetchdf()
print("Wynik analizy:")
print(result)

# Eksport do CSV
result.to_csv('data/blocklist_report.csv', index=False)
print("[INFO] Raport został zapisany.")
