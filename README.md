Python Akıllı Sözdizimi (Syntax) Asistanı

SemetonBug, Python programlama dilinde yazılmış kod bloklarını Abstract Syntax Tree (AST) düzeyinde analiz ederek, kod içerisindeki yapısal veya sözdizimsel (Syntax) hataları makine öğrenmesi yöntemleriyle tahmin eden yapay zekâ tabanlı bir web asistanıdır.

Bu proje, bilgisayar mühendisliği mezuniyet/yıl sonu çalışması kapsamında geliştirilmiştir.


 Proje Özellikleri

* **AST Tabanlı Analiz:** Kod bloklarını sadece metin olarak değil, soyut sözdizimi ağaçları (Abstract Syntax Tree) düzeyinde yapısal olarak inceler.
* **Gelişmiş NLP Yöntemleri:** Kod özelliklerinin vektörleştirilmesinde NLP (Doğal Dil İşleme) ve TF-IDF metotları kullanılmıştır.
* **Makine Öğrenmesi Sınıflandırması:** Girdileri "Yüksek Risk (Hatalı)" veya "Düşük Risk (Sağlam)" olarak ayırt etmek için **Random Forest Sınıflandırıcı** algoritmasından yararlanılmıştır.
* **Anlık Kararlılık Oranı (Confidence Score):** Modelin o anki spesifik kod bloğu üzerinde yaptığı tahminin güven derecesini dinamik olarak hesaplar.
* **Kapsam Dışı Girdi Kontrolü:** Python harici diller (örn. Java) veya düz metin girildiğinde kullanıcıyı dostane bir sistem uyarısıyla yönlendirir.
* **Kullanıcı Dostu Streamlit Arayüzü:** Modern, scannable ve karanlık mod destekli interaktif bir web arayüzüne sahiptir.


 Veri Seti ve Başarı Oranı

* **Veri Seti:** Projenin eğitimi ve testi için büyük ölçekli kaynak kod analizlerinde standart kabul edilen **py150 (Sub-sample)** veri seti kullanılmıştır.
* **Model Genel Doğruluk Oranı (Accuracy):** **%87**


Proje Klasör Yapısı

```text
├── archive/               # py150 Ham Veri Seti Klasörü (Büyük boyutlu, repoya dahil edilmemiştir)
├── processed_data/        # İşlenmiş ve öznitelikleri çıkarılmış veri klasörü
├── app.py                 # Streamlit Web Arayüzü ana uygulama dosyası
├── eda.ipynb              # Keşifsel Veri Analizi (Exploratory Data Analysis) notebook'u
├── main_training.ipynb    # Model eğitimi ve boru hattı (pipeline) dosyası
├── model_egitimi.ipynb    # Model hiperparametre optimizasyonu notebook'u
├── preprocessing.ipynb    # Veri ön işleme ve AST dönüşüm adımları
├── shap_analizi.ipynb     # Model kararlarının SHAP ile açıklanabilir yapay zekâ analizi
├── yapay_zeka_modeli.pkl  # Eğitilmiş Random Forest model nesnesi (.pkl formatında)
└── .gitignore             # GitHub'a yüklenmeyecek büyük dosyaların filtresi
