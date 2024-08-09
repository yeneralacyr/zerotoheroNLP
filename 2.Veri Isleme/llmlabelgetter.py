import os
import csv
from bs4 import BeautifulSoup

def extract_csv_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    csv_data = []
    for div in soup.find_all('div', class_='group/conversation-turn'):
        code = div.find('code', class_='!whitespace-pre hljs language-csv')
        if code:
            csv_content = code.get_text().strip()
            csv_data.extend(csv.reader(csv_content.splitlines()))
    return csv_data

def process_files(directory):
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                html_content = file.read()
                csv_data = extract_csv_content(html_content)
                all_data.extend(csv_data)
    
    return all_data

def write_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Kullanım
directory = 'D:\Teknofest2024\cokluetiketlemeler'  # HTML dosyalarınızın bulunduğu dizin
output_file = 'combined_output.csv'  # Birleştirilmiş CSV dosyasının adı

combined_data = process_files(directory)
write_csv(combined_data, output_file)

print(f"Birleştirilmiş veriler {output_file} dosyasına kaydedildi.")