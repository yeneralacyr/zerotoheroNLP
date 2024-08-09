import csv

def compare_and_mark_files(large_file, small_file, output_file, large_target_column, small_target_column):
    # Küçük dosyadaki satırları bir kümeye ekle
    small_file_rows = set()
    with open(small_file, 'r', newline='', encoding='utf-8') as small:
        reader = csv.DictReader(small, quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            small_file_rows.add(row[small_target_column].strip('"'))

    # Büyük dosyayı oku, işaretle ve yeni dosyaya yaz
    with open(large_file, 'r', newline='', encoding='utf-8') as large, \
         open(output_file, 'w', newline='', encoding='utf-8') as output:
        reader = csv.DictReader(large, quoting=csv.QUOTE_MINIMAL)
        fieldnames = reader.fieldnames + ['Eslesme']
        writer = csv.DictWriter(output, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()

        for row in reader:
            # Tırnak işaretlerini kaldır ve karşılaştır
            if row[large_target_column].strip('"') in small_file_rows:
                row['Eslesme'] = '1'
                print(f"Eşleşme bulundu: {row[large_target_column]}")
            else:
                row['Eslesme'] = '0'
                print(f"Eşleşme bulunamadı: {row[large_target_column]}")
            writer.writerow(row)

# Kullanım
large_file = 'tersameri.csv'  # Büyük CSV dosyasının adı
small_file = 'cleaned000111_output.csv'  # Küçük CSV dosyasının adı
output_file = 'zibabo.csv'  # İşaretlenmiş verilerin yazılacağı yeni CSV dosyası
large_target_column = 'comment'  # Büyük dosyadaki hedef sütun başlığı
small_target_column = 'memento'  # Küçük dosyadaki hedef sütun başlığı

compare_and_mark_files(large_file, small_file, output_file, large_target_column, small_target_column)
print(f"İşaretlenmiş veriler {output_file} dosyasına kaydedildi.")