import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Ortam değişkenlerinden credentials al
EMAIL = os.getenv('PIXAI_EMAIL')
PASSWORD = os.getenv('PIXAI_PASSWORD')

if not EMAIL or not PASSWORD:
    print("❌ PIXAI_EMAIL veya PIXAI_PASSWORD ortam değişkenleri ayarlanmadı!")
    exit(1)

print(f"📧 Email: {EMAIL}")

# Chrome seçenekleri
chrome_options = Options()
chrome_options.add_argument("--headless")  # GUI olmadan çalış
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

try:
    # Tarayıcıyı başlat
    print("🌐 Chrome başlatılıyor...")
    driver = webdriver.Chrome(options=chrome_options)
    
    # Pixai'ye git
    print("🔗 pixai.art'a gidiliyor...")
    driver.get("https://pixai.art/")
    time.sleep(3)
    
    # Login butonunu bul ve tıkla
    print("🔑 Login butonuna tıklanıyor...")
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))
        )
        login_button.click()
    except:
        try:
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Login')]"))
            )
            login_button.click()
        except:
            print("⚠️ Login butonu bulunamadı, devam ediliyor...")
    
    time.sleep(2)
    
    # Email input'una tıkla ve yazı yaz
    print("📝 Email giriliyör...")
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='email' or @placeholder='Email']"))
    )
    email_input.clear()
    email_input.send_keys(EMAIL)
    time.sleep(1)
    
    # Password input'una tıkla ve yazı yaz
    print("🔐 Şifre giriliyör...")
    password_input = driver.find_element(By.XPATH, "//input[@type='password']")
    password_input.clear()
    password_input.send_keys(PASSWORD)
    time.sleep(1)
    
    # Login butonuna tıkla
    print("✅ Login yapılıyor...")
    login_submit = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
    login_submit.click()
    
    # Login'in tamamlanmasını bekle
    time.sleep(5)
    
    # Claim sayfasına git
    print("🎁 Claim sayfasına gidiliyor...")
    driver.get("https://pixai.art/user/sign-in")
    time.sleep(2)
    
    # Profile veya Dashboard'a git
    driver.get("https://pixai.art/user")
    time.sleep(3)
    
    # Claim butonu ara ve tıkla
    print("🔘 Claim butonu aranıyor...")
    try:
        claim_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Claim')] | //button[contains(text(), 'claim')]"))
        )
        claim_button.click()
        print("✨ Credit başarıyla claim edildi!")
        time.sleep(2)
    except:
        print("⚠️ Claim butonu bulunamadı veya zaten claim edilmiş olabilir")
    
    print("✅ İşlem tamamlandı!")
    
except Exception as e:
    print(f"❌ Hata oluştu: {str(e)}")
    exit(1)
finally:
    driver.quit()
    print("🔌 Tarayıcı kapatıldı")
