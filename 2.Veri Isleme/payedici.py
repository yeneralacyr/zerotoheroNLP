import csv
import re

def kategorize_tweet(tweet, hashtags, kategori_hashtag_map, kategori_count_map):
    # Tweet'teki hashtag'leri bul
    tweet_hashtags = set(hashtags.lower().split())
    
    # Her kategori için puan hesapla
    kategori_puanlar = {}
    for kategori, hashtag_list in kategori_hashtag_map.items():
        puan = sum(1 for tag in tweet_hashtags if tag in hashtag_list)
        if puan > 0:
            kategori_puanlar[kategori] = puan
    
    if not kategori_puanlar:
        return "Kategorize Edilemedi"
    
    # En yüksek puanı alan kategorileri bul
    max_puan = max(kategori_puanlar.values())
    en_yuksek_kategoriler = [k for k, v in kategori_puanlar.items() if v == max_puan]
    
    if len(en_yuksek_kategoriler) == 1:
        return en_yuksek_kategoriler[0]
    else:
        # Eşitlik durumunda, daha az tweet'e sahip kategoriye öncelik ver
        return min(en_yuksek_kategoriler, key=lambda k: kategori_count_map[k])

# Kategori-hashtag eşleşmeleri
kategori_hashtag_map = {
    "Müşteri Hizmetleri Şikayetleri": ["#müşterihizmetleri", "#müşterihizmeti", "#müşterimemnuniyeti", "#ilgisizlik", "#yanlışbilgilendirme", "#müşteritemsilcisi", "#çağrımerkezi"],
    "Teknik Şikayetler": ["#internetsorunu", "#şebekesorunu", "#bağlantısorunu", "#sinyalsorunu", "#altyapısorunu", "#arıza", "#internethızı", "#çekimsorunu", "#arızasorunu", "#modemsorunu", "#internetarızası", "#hızsorunu", "#yavaşinternet"],
    "Fatura ve Ödeme Şikayetleri": ["#faturasorunu", "#haksızücret", "#yüksekfatura", "#tarifesorunu", "#haksızkesinti", "#fiyatartışı", "#haksızfatura", "#ödemesorunu", "#haksızkazanç", "#faturahatası", "#fazlaücret", "#ücretsorunu", "#faturaartışı", "#yüksekücret", "#ücretiadesi", "#borçsorunu", "#ekstraücret", "#faturaşoku"],
    "Sözleşme ve Taahhüt Şikayetleri": ["#caymabedeli", "#taahhütsorunu", "#taahhüt", "#sözleşmesorunu", "#taahhütyenileme"],
    "Abonelik ve İşlem Şikayetleri": ["#nakilsorunu", "#numarataşıma", "#iptalsorunu", "#aboneliksorunu", "#abonelikiptali", "#hattkapatma", "#izinsizüyelik", "#üyelikiptali", "#izinsizabonelik"],
    "Ürün ve Hizmet Spesifik Şikayetler": ["#mobiloperatör", "#mobilinternet", "#fiberinternet", "#mobilşikayet", "#mobilödeme", "#internetpaketi", "#superbox", "#evinternet"],
    "Paket ve Kampanya Şikayetleri": ["#paketsorunu", "#kampanyasorunu", "#tlyükleme", "#paketyenileme", "#paketdeğişikliği", "#paketyükleme", "#ekpaketsorunu"]
}

# Kategori-tweet sayısı eşleşmeleri
kategori_count_map = {
    "Müşteri Hizmetleri Şikayetleri": 918,
    "Teknik Şikayetler": 773,
    "Fatura ve Ödeme Şikayetleri": 1105,
    "Sözleşme ve Taahhüt Şikayetleri": 207,
    "Abonelik ve İşlem Şikayetleri": 211,
    "Ürün ve Hizmet Spesifik Şikayetler": 704,
    "Paket ve Kampanya Şikayetleri": 233
}

# CSV dosyasını oku ve işle
input_file = 'yeni_dosya.csv'  # Giriş dosyanızın adı
output_file = 'outputto.csv'  # Çıkış dosyanızın adı

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # Başlık satırını yaz
    writer.writerow(['text', 'hashtag', 'anabaslik'])
    
    # Her satırı oku ve işle
    for row in reader:
        if len(row) >= 2:  # En az iki sütun olduğundan emin ol
            text, hashtags = row[:2]
            kategori = kategorize_tweet(text, hashtags, kategori_hashtag_map, kategori_count_map)
            writer.writerow([text, hashtags, kategori])

print(f"İşlem tamamlandı. Sonuçlar {output_file} dosyasına yazıldı.")