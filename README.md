# Pixai Daily Auto Claim 🎁

GitHub Actions kullanarak her gün otomatik olarak Pixai'de günlük bonusu claim et!

## Özellikler ✨

- ✅ **Tamamen Ücretsiz** - GitHub public repos için sınırsız Actions dakikası
- ✅ **PC Açık Olmasa Da Çalışır** - Cloud'da çalışıyor
- ✅ **Otomatik Zamanlama** - Her gün belirli saatte çalışır
- ✅ **Güvenli** - Credentials repo secrets'te saklanır

## Kurulum 🚀

### 1. Email ve Şifreyi Ekle

1. Reponun **Settings** sekmesine git
2. Sol menüde **Secrets and variables** → **Actions** seç
3. **New repository secret** butonuna tıkla
4. İlk secret:
   - **Name:** `PIXAI_EMAIL`
   - **Value:** Senin Pixai email'in
5. **Add secret** butonuna tıkla

6. Tekrar **New repository secret** butonuna tıkla
7. İkinci secret:
   - **Name:** `PIXAI_PASSWORD`
   - **Value:** Senin Pixai şifresi
8. **Add secret** butonuna tıkla

### 2. Workflow'u Etkinleştir

1. **Actions** sekmesine git
2. "Daily Pixai Claim" workflow'unu göreceksin
3. **Enable workflow** butonuna tıkla (eğer devre dışı ise)

### 3. Test Et (İsteğe Bağlı)

1. **Actions** sekmesine git
2. "Daily Pixai Claim" workflow'unu seç
3. **Run workflow** butonuna tıkla
4. **Run workflow** butonuna tıkla
5. Workflow'un çalışmasını izle

## Zaman Ayarı ⏰

Şu anda **Her gün 06:00 UTC** (Türkiye'de **09:00** - Yazlık saat) çalışıyor.

Farklı bir saate ayarlamak istiyorsan:
1. `.github/workflows/claim.yml` dosyasını düzenle
2. `cron: '0 6 * * *'` satırını değiştir
   - Format: `'dakika saat gün ay haftanıngünü'`
   - Örnek: `'0 8 * * *'` = Her gün 08:00 UTC

[Cron expression açıklaması](https://crontab.guru/)

## Logs Kontrol Et 📊

1. **Actions** sekmesine git
2. Son çalışan workflow'a tıkla
3. **claim** job'unu seç
4. Çalışma loglarını gör

## Güvenlik ⚠️

- ✅ Email ve şifre repo'da depolanmıyor
- ✅ GitHub Secrets'te şifreli olarak tutunuyor
- ✅ Logs'ta şifre görünmüyor
- ✅ Repo public olsa bile secure

## Sorun Giderme 🔧

### Workflow başlamıyor
- Repoyu düzenledikten sonra biraz bekle (5-10 dakika)
- Repoyu refresh et

### Login başarısız
- Email ve şifreyi kontrol et
- 2FA varsa devre dışı bırak
- Pixai adresindeki "Sign In" linkini kontrol et

### Claim yapılmıyor
- Seçici XPath'lar değişmiş olabilir (Pixai UI güncellemeler)
- Script'i güncellemek gerekebilir

## Lisans

MIT