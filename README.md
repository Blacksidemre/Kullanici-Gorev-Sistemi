# **📋 Çok Kullanıcılı Görev Yönetim Uygulaması**

Bu proje, birden fazla kullanıcının kendi görevlerini ekleyebildiği, düzenleyebildiği, tamamlayabildiği ve silebildiği basit bir görev yönetim uygulamasıdır.
Arayüz Gradio ile geliştirilmiştir ve her kullanıcıya ait görevler yerel JSON dosyalarında saklanır.

---

## 🚀 **Özellikler**

* Kullanıcı kaydı ve giriş sistemi
* Her kullanıcı için ayrı görev dosyası
* Görev ekleme
* Görev düzenleme
* Görev silme
* Görev tamamla / geri al
* Tamamlanan görev istatistikleri

  * Tamamlanan görev sayısı
  * Ortalama tamamlama süresi (dakika cinsinden)
* Temiz, kullanışlı Gradio arayüzü

---

## 📦 **Kurulum**

Bu projeyi çalıştırmak için Python 3.9+ tavsiye edilir.

### 1. Gerekli kütüphaneleri yükle:

```bash
pip install -r requirements.txt
```

### 2. Uygulamayı başlat:

```bash
python app.py
```

Terminal çıktı olarak Gradio’nun verdiği URL’yi gösterir.
Tarayıcıda açarak uygulamayı kullanmaya başlayabilirsiniz.

---

## 🗂️ **Proje Yapısı**

```text
.
├── app.py                # Ana uygulama dosyası
├── requirements.txt      # Bağımlılıklar
└── README.md             # Proje açıklaması
```

Uygulama çalıştıkça, aynı klasörde kullanıcıya göre şu dosyalar oluşur:

```
users.json
<kullanici_adi>_gorevler.json
```

---

## 🔒 **Veri Saklama Mantığı**

* `users.json` içinde kullanıcı adı → şifre eşleşmeleri bulunur.
* Her kullanıcı için `kullaniciadi_gorevler.json` oluşturulur.
* Görevler şu bilgileri içerir:

  * id
  * metin
  * oluşturulma zamanı
  * tamamlanma durumu
  * tamamlanma zamanı

---

## 📊 **İstatistik Hesaplama**

Tamamlanmış görevler üzerinden:

* Toplam kaç görev tamamlandığı
* Görevlerin ortalama tamamlanma süresi

otomatik hesaplanır.

---

## 🔧 **Geliştirme Notları**

* Veritabanı yerine JSON kullanıldığı için kullanım yerel veri saklama mantığıyla çalışır.
* Arayüz kolayca genişletilebilir yapıdadır.
* Auth sistemi temel düzeydedir; profesyonel kullanım için geliştirilmesi gerekir.

---

## 📄 Lisans

Bu proje eğitim amaçlı hazırlanmıştır. Serbestçe değiştirilebilir ve dağıtılabilir.

---


