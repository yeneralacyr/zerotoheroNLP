import pandas as pd
from collections import Counter

# CSV dosyasını oku
df = pd.read_csv('output_1.csv')

# Tüm hashtag'leri bir listede topla
all_hashtags = []
for hashtags in df['hashtags'].dropna():
    all_hashtags.extend(hashtags.split())

# Hashtag'leri say ve sözlük oluştur
hashtag_counts = dict(Counter(all_hashtags))

# Sözlüğü kullanım sayısına göre azalan sırayla sırala
sorted_hashtags = dict(sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True))

# Sonuçları yazdır
print("Hashtag kullanım sıklığı:")
for hashtag, count in sorted_hashtags.items():
    print(f"{hashtag}: {count}")

# Sonuçları bir dosyaya kaydet
with open('hashtag_counts3.txt', 'w', encoding='utf-8') as f:
    for hashtag, count in sorted_hashtags.items():
        f.write(f"{hashtag}: {count}\n")

print("\nSonuçlar 'hashtag_counts.txt' dosyasına kaydedildi.")