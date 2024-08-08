from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# WebDriver'ı başlat
PATH = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH)

# Sikayet.com adresine git
driver.get("https://www.sikayet.com/")

# Örneğin bir marka veya kategoriye tıklayın (bu adım site yapısına göre değişebilir)
# Örneğin bir arama yaparak belirli bir markanın şikayetlerine gitmek

search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("turkcell")  # Arama terimini girin
search_box.send_keys(Keys.RETURN)  # Aramayı gönderin

# Tüm sayfalardaki linkleri toplayacak liste
all_links = []

# Sayfa numarasını başlat
page_num = 13

while page_num < 100:  # 100. sayfaya kadar devam et
    try:
        # Sayfa yüklendiğinde şikayet bağlantılarını bul
        ul_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "list-five.clear"))
        )
        
        # Find all 'a' tags within this ul element
        a_tags = ul_element.find_elements(By.CSS_SELECTOR, "a.title")
        
        # Print the 'href' attributes of each 'a' tag
        for a in a_tags:
            all_links.append(a.get_attribute("href"))

        # Sonraki sayfaya git
        page_num += 1
        next_page_url = f"https://www.sikayet.com/sikayetler/{page_num}?q=turkcell"
        driver.get(next_page_url)
        
        # Kısa bir bekleme süresi ekleyin
        time.sleep(10)

    except TimeoutException:
        # Daha fazla sayfa olmadığında döngüden çık
        break

# 100. sayfayı da işle
if page_num == 100:
    try:
        # Sayfa yüklendiğinde şikayet bağlantılarını bul
        ul_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "list-five.clear"))
        )
        
        # Find all 'a' tags within this ul element
        a_tags = ul_element.find_elements(By.CSS_SELECTOR, "a.title")
        
        # Print the 'href' attributes of each 'a' tag
        for a in a_tags:
            all_links.append(a.get_attribute("href"))

    except TimeoutException:
        pass

print(all_links)
driver.quit()