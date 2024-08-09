import csv
import re

def remove_quotes(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        # CSV dosyasını okurken tırnak karakterlerini özel olarak işle
        reader = csv.reader(infile, quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        writer = csv.writer(outfile, quoting=csv.QUOTE_NONE, escapechar='\\')
        
        for row in reader:
            # Her bir hücredeki tırnak işaretlerini kaldır
            cleaned_row = [re.sub(r'^"|"$', '', field.strip()) for field in row]
            
            # Hücre içindeki çift tırnakları tek tırnağa çevir
            cleaned_row = [re.sub(r'""', "'", field) for field in cleaned_row]
            
            # Kalan tüm tırnak işaretlerini kaldır
            cleaned_row = [re.sub(r'"', '', field) for field in cleaned_row]
            
            # Temizlenmiş satırı yaz
            writer.writerow(cleaned_row)

    print(f"Tırnak işaretleri temizlenmiş CSV dosyası '{output_file}' olarak kaydedildi.")

# Script'i çalıştır
input_file = 'formatlanms.csv'  # Giriş dosyanızın adı
output_file = 'tirnaksiz.csv'    # Çıkış dosyanızın adı

remove_quotes(input_file, output_file)