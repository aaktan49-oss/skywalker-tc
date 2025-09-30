# FTP Yükleme Rehberi - Skywalker.tc

## 📂 FTP Bilgileri (Güzel.net.tr)
```
FTP Host: ftp.güzel.net.tr
Port: 21
Username: DirectAdmin kullanıcı adınız
Password: DirectAdmin şifreniz
```

## 📁 Dosya Yükleme Adımları

### 1. FTP Programı ile Bağlanın
- FileZilla, WinSCP veya benzeri FTP client
- Güzel.net.tr DirectAdmin panelindeki FTP bilgilerini kullanın

### 2. Klasör Yapısı
```
public_html/          ← Buraya yükleyin
├── index.html        ← Ana sayfa
├── .htaccess         ← URL yönlendirmeleri
├── asset-manifest.json
└── static/
    ├── css/
    │   └── main.fceccb93.css
    └── js/
        └── main.9fde6268.js
```

### 3. Yükleme Sırası
1. Önce public_html klasörünü temizleyin (varsa eski dosyalar)
2. ftp-upload klasöründeki TÜM dosyaları public_html'e yükleyin
3. .htaccess dosyasının yüklendiğinden emin olun

### 4. Test Adımları
- https://yourdomain.güzel.net.tr adresini açın
- Sayfa yüklenmiyorsa .htaccess dosyasını kontrol edin
- Admin paneli: https://yourdomain.güzel.net.tr/admin

## 🔧 Sorun Giderme
- 404 Hatası: .htaccess dosyası eksik olabilir
- CSS Yüklenmiyorsa: static klasörü eksik olabilir
- Beyaz sayfa: index.html yüklenmemiş olabilir

## 📞 DirectAdmin Destek
Panel: https://panel.güzel.net.tr
Destek: Güzel.net.tr müşteri hizmetleri