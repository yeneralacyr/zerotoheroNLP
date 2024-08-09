import csv

# Giriş CSV dosyasının adı
input_csv = 'cleaned000111_output.csv'

# Çıkış CSV dosyasının adı
output_csv = 'tekrarszislenmis.csv'

# Tekrar eden 'memento' sütun değerlerini takip etmek için bir set
seen_memento = set()

# Çıkışı saklayacağımız liste
output_data = []

# Giriş dosyasını okuma
with open(input_csv, mode='r', encoding='utf-8', newline='') as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames  # Başlık satırlarını al
    
    # Tüm satırları kontrol et
    for row in reader:
        memento_value = row['memento']
        # Eğer 'memento' değeri daha önce görülmemişse
        if memento_value not in seen_memento:
            seen_memento.add(memento_value)
            output_data.append(row)

# Çıkış dosyasına yazma
with open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()  # Başlık satırını yaz
    writer.writerows(output_data)

print(f"İşlem tamamlandı. Çıkış dosyası '{output_csv}' olarak kaydedildi.")