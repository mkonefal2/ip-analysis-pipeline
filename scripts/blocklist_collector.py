import os
import csv
import requests

def fetch_blocklist(output_file='../data/blocklist.csv'):
    url = "https://lists.blocklist.de/lists/all.txt"
    response = requests.get(url)

    if response.status_code == 200:
        ip_list = response.text.strip().split("\n")
        
        # Upewnij się, że katalog istnieje
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ip_address"])
            for ip in ip_list:
                writer.writerow([ip])

        print(f"[INFO] Zapisano {len(ip_list)} adresów IP do {output_file}.")
        return output_file
    else:
        print(f"[ERROR] Nie udało się pobrać listy. Kod: {response.status_code}")
        return None

if __name__ == "__main__":
    fetch_blocklist()