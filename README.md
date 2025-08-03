# MuseumArt: Sanat Eseri Tanıma Web Uygulaması

<img width="500" height="300" alt="Ekran Resmi 2025-08-03 11 44 01" src="https://github.com/user-attachments/assets/05a2fccd-fa8d-42c7-b157-3c8a4cfc7371" />



MuseumArt, görsellerdeki sanat eserlerini tanımlamak ve bunlar hakkında detaylı bilgi sunmak için tasarlanmış bir Flask web uygulamasıdır. Kullanıcılar, bir görsel yükleyerek veya bilgisayarlarının kamerasını kullanarak bir sanat eserini tarayabilirler. Uygulama, tanımlanan sanat eserinin sanatçısı, başlığı, açıklaması gibi bilgileri bir CSV veritabanından getirir ve aynı sanatçıya ait benzer eserleri de önerir.

## Özellikler

* **Görsel Yükleme:** Kullanıcılar, yerel cihazlarından bir sanat eseri görselini yükleyerek tanıma yapabilirler.
* **Kamera ile Tanıma:** Bilgisayarın kamerasını kullanarak anlık olarak sanat eseri taraması yapma imkanı (dağıtım ortamına göre çalışmayabilir).
* **Detaylı Sanat Eseri Bilgisi:** Tanımlanan eserin sanatçısı, başlığı, açıklaması ve görsel URL'si gibi bilgileri görüntüler.
* **Benzer Eser Önerileri:** Tanımlanan sanat eseriyle aynı sanatçıya ait diğer eserleri listeler.
* **Dinamik Sanat Eseri Detay Sayfası:** Başlığa göre belirli bir sanat eserinin detaylarını doğrudan görüntüleyebilme.

## Kullanılan Teknolojiler

Bu proje aşağıdaki temel teknolojiler ve kütüphanelerle geliştirilmiştir:

* **Python:** Uygulamanın ana programlama dili.
* **Flask:** Web uygulamasının çatısı.
* **Ultralytics YOLO:** Sanat eserlerini görsellerde tespit etmek için kullanılan derin öğrenme modeli (YOLOv8).
* **Pandas:** Sanat eserleri verilerini (CSV dosyası) okuma ve işleme için.
* **OpenCV (cv2):** Görsel işleme ve kamera erişimi için.
* **HTML/CSS:** Kullanıcı arayüzü için (Flask'ın `templates` klasörü aracılığıyla).
* **Gunicorn:** (Dağıtım için önerilir) Flask uygulamasını production ortamında çalıştırmak için bir WSGI sunucusu.

## Kurulum ve Çalıştırma (Yerel Ortamda)

Projeyi kendi bilgisayarınızda kurmak ve çalıştırmak için aşağıdaki adımları takip edin:

1.  **Depoyu Klonlayın:**
    ```bash
    git clone [https://github.com/zzeynepcvk/MuseumArt.git](https://github.com/zzeynepcvk/MuseumArt.git)
    cd MuseumArt
    ```

2.  **Sanal Ortam Oluşturun (Önerilir):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # veya
    # venv\Scripts\activate  # Windows
    ```

4.  **Bağımlılıkları Yükleyin:**
    
    ```
    ```bash
    pip install -r requirements.txt
    ```

5.  **Uygulamayı Çalıştırın:**
    ```bash
    python app.py
    ```
   
