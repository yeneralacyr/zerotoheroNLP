import csv

# Giriş CSV dosyasının adı
input_csv = 'zibabo.csv'

# Çıkış CSV dosyasının adı
output_csv = 'zibaboelek.csv'

# Çıkışı saklayacağımız liste
output_data = []

# Giriş dosyasını okuma
with open(input_csv, mode='r', encoding='utf-8', newline='') as infile:
    reader = csv.DictReader(infile)
    # Çıkış dosyasının başlıkları
    fieldnames = ['comment']
    
    for row in reader:
        # Üçüncü sütun (Eslesme) değeri 0 olan satırın ikinci sütununu (comment) kontrol et
        if row['Eslesme'] == '0':
            output_data.append([row['comment']])

# Çıkış dosyasına yazma
with open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(fieldnames)  # Başlık satırını yaz
    writer.writerows(output_data)

print(f"İşlem tamamlandı. Çıkış dosyası '{output_csv}' olarak kaydedildi.")