# 📌 Proje Başlığı
Öğrenci Bilgi Sistemi

---

## 🧾 Proje Tanıtımı
Bu uygulama, kullanıcıların öğrenci kayıt, not ve iletişim bilgilerini kolayca takip edebileceği bir sistemdir. Flask framework’ü ile geliştirilmiş olup, kullanıcı girişi, kayıt, not ekleme/silme ve ders görüntüleme gibi işlemler yapılabilir.

---

## 🚀 Proje Özellikleri
- 🔐 Kullanıcı kayıt ve giriş işlemleri
- 📚 Yeni veri (not, ders) ekleyebilme
- 📝 Verileri düzenleyebilme ve silebilme
- 🔎 Arama / filtreleme özellikleri
- 📦 Veritabanı bağlantısı ile kalıcı veri saklama

---

## ⚙️ Kurulum ve Çalıştırma

### ✅ Gereksinimler
Bu projeyi çalıştırmak için bilgisayarınızda aşağıdaki yazılımlar kurulu olmalıdır:
- Python 3.x

Ayrıca aşağıdaki kütüphaneler kullanılmaktadır:
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Werkzeug

> Not: Bu kütüphaneleri `requirements.txt` dosyasından otomatik olarak yükleyebilirsiniz.

### 🚀 Uygulamayı Başlatma
Uygulama tarayıcınızda http://127.0.0.1:5000/ adresinde çalışacaktır.

## 📂 Proje Dosya Yapısı
├── app.py                # Ana Python uygulama dosyası
├── templates/            # HTML şablonlarının bulunduğu klasör
│   ├── anasayfa.html     # Anasayfa
│   ├── login.html        # Giriş formu
│   ├── register.html     # Kayıt formu
│   ├── dashboard.html     # Kullanıcı kontrol paneli
│   ├── base.html         # Temel şablon
│   ├── ders_ekle.html    # Ders ekleme formu
│   ├── ders_guncelle.html # Ders güncelleme formu
│   ├── derslerim.html    # Kullanıcının dersleri
│   ├── notlar.html       # Notlar sayfası
│   └── not_ekle.html     # Not ekleme formu
├── static/               # Statik dosyalar (CSS, JS, resimler)
│   └── style.css         # Uygulamaya ait stil dosyası
├── requirements.txt      # Gerekli Python paketlerini içeren dosya
└── final_versiyon.md     # Proje açıklama dosyası