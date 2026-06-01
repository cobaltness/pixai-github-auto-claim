import os
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Ortam değişkenlerinden credentials al
EMAIL = os.getenv('PIXAI_EMAIL')
PASSWORD = os.getenv('PIXAI_PASSWORD')

if not EMAIL or not PASSWORD:
    print("❌ PIXAI_EMAIL veya PIXAI_PASSWORD ortam değişkenleri ayarlanmadı!")
    exit(1)

print(f"📧 Email: {EMAIL}")

# Chrome seçenekleri
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # Yeni headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--lang=en")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

driver = None

try:
    # Tarayıcıyı başlat
    print("🌐 Chrome başlatılıyor...")
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Driver timeout ayarları
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(3)
    
    # Pixai login sayfasına git
    print("🔗 pixai.art login sayfasına gidiliyor...")
    driver.get("https://pixai.art/login")
    time.sleep(5)  # JavaScript yüklensin
    
    # 1️⃣ POPUP/MODAL KAPATMA
    print("🔘 Popup kontrol ediliyor...")
    try:
        popup_buttons = [
            ("form > div > div > button:nth-of-type(4)", By.CSS_SELECTOR),
            ("/html/body/div[4]/div/div/button", By.XPATH),
            ("button[aria-label='Dismiss']", By.CSS_SELECTOR),
        ]
        
        popup_closed = False
        for selector, by_type in popup_buttons:
            try:
                popup_btn = driver.find_element(by_type, selector)
                popup_btn.click()
                print("✅ Popup kapatıldı")
                popup_closed = True
                time.sleep(1)
                break
            except:
                continue
                
        if not popup_closed:
            print("⚠️ Popup bulunamadı, devam ediliyor...")
    except Exception as e:
        print(f"⚠️ Popup kapatma hatası: {e}")
    
    time.sleep(2)
    
    # 2️⃣ EMAIL GİRİŞİ - ID ile eriş
    print("📝 Email giriliyör...")
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email-input"))
    )
    email_input.clear()
    email_input.send_keys(EMAIL)
    time.sleep(1)
    
    # 3️⃣ PASSWORD GİRİŞİ - ID ile eriş
    print("🔐 Şifre giriliyör...")
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password-input"))
    )
    password_input.clear()
    password_input.send_keys(PASSWORD)
    time.sleep(1)
    
    # 4️⃣ LOGIN BUTONU - İki kez tıkla
    print("✅ Login yapılıyor...")
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    login_button.click()
    time.sleep(1)
    login_button.click()  # İkinci tıklama (BySuspect'in yöntemi)
    
    # 5️⃣ LOGIN BAŞARI KONTROLÜ
    print("⏳ Login doğrulanıyor...")
    WebDriverWait(driver, 20).until(
        EC.url_matches(r"https://pixai\.art/?$")
    )
    print("✅ Login başarılı!")
    time.sleep(3)
    
    # 6️⃣ POPUP TEKRAR KONTROL
    try:
        popup_buttons = [
            ("form > div > div > button:nth-of-type(4)", By.CSS_SELECTOR),
            ("/html/body/div[4]/div/div/button", By.XPATH),
        ]
        
        for selector, by_type in popup_buttons:
            try:
                popup_btn = driver.find_element(by_type, selector)
                popup_btn.click()
                print("✅ Popup tekrar kapatıldı")
                time.sleep(1)
                break
            except:
                continue
    except:
        pass
    
    time.sleep(2)
    
    # 7️⃣ CLAIM BUTONUNU BUL VE TIKLA
    print("🎁 Claim butonu aranıyor...")
    try:
        claim_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//*[@id='root']/div/div[2]/div/div/div/div/div[1]/section/div/div[2]/div[2]/button"))
        )
        
        # Button textini kontrol et
        button_span = claim_button.find_element(By.TAG_NAME, "span")
        button_text = button_span.get_attribute("innerHTML").lower()
        
        if "claimed" not in button_text:
            claim_button.click()
            print("✨ Claim butonu tıklandı, bekleniyor...")
            
            # Claim başarısını doğrula
            for i in range(30):
                try:
                    time.sleep(1)
                    current_text = claim_button.find_element(By.TAG_NAME, "span").get_attribute("innerHTML").lower()
                    if "claimed" in current_text:
                        print("✨ Credit başarıyla claim edildi!")
                        break
                except:
                    pass
                    
                if i == 29:
                    print("⚠️ Claim işlemi tamamlanamadı")
        else:
            print("⚠️ Credit daha önceden claim edilmiş")
            
    except Exception as e:
        print(f"❌ Claim butonu hatası: {e}")
        traceback.print_exc()
    
    print("✅ İşlem tamamlandı!")
    time.sleep(2)
    
except Exception as e:
    print(f"❌ Hata oluştu: {str(e)}")
    traceback.print_exc()
    exit(1)
    
finally:
    if driver:
        driver.quit()
    print("🔌 Tarayıcı kapatıldı")
