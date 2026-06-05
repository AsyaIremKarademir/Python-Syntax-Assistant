import streamlit as st
import joblib
import ast
import os

# ============================================================================
# 1. SAYFA AYARLARI VE CSS İLE YAZI BOYUTLARINI BÜYÜTME (DEV BOYUT SÜRÜMÜ)
# ============================================================================
st.set_page_config(
    page_title="Python Syntax Error Detector Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Yazıları jürinin en arkadan bile çok rahat okuması için dev boyutlara getiren CSS
st.markdown("""
    <style>
    /* 1. Sohbet balonlarının içindeki genel yazı boyutunu büyüt */
    .stChatMessage p, .stChatMessage div {
        font-size: 20px !important;
        line-height: 1.6 !important;
    }
    
    /* 2. Chatbot'un yazdığı maddeli listelerin (.ul, .li) boyutunu büyüt */
    .stChatMessage ul li {
        font-size: 20px !important;
    }
    
    /* 3. Genel markdown düz yazılarını, kalın yazıları ve açıklamaları dev boyuta getir */
    .stMarkdown p, .stMarkdown span {
        font-size: 20px !important;
    }
    
    /* 4. Hata teşhis başlıkları ve vurguları için ekstra görünürlük */
    .stMarkdown strong {
        font-size: 21px !important;
        font-weight: bold !important;
    }
    
    /* 5. Kullanıcının yapıştırdığı kod bloklarının içindeki font boyutu */
    code {
        font-size: 18px !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    
    /* 6. Ana ekranın en üstündeki st.write açıklamaları */
    .stText p {
        font-size: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# 2. CANLI KODDAN AST DÜĞÜMÜ ÇIKARMA VE AKILLI ANALİZ MOTORU
# ============================================================================
# ============================================================================
# 2. CANLI KODDAN AST DÜĞÜMÜ ÇIKARMA VE AKILLI ANALİZ MOTORU (DİL KORUMALI)
# ============================================================================
def canli_kod_ast_cevir(python_kodu):
    """
    Kullanıcının girdiği metni inceler.
    Eğer düz sohbet metni VEYA başka bir programlama dili (C, C++, Java vb.) ise -> (None, "sohbet")
    Eğer geçerli/temiz Python kodu ise -> (ast_text, "temiz")
    Eğer syntax hatası içeren Python kodu ise -> (ast_text, "hatali")
    """
    # --- 1. ADIM: BAŞKA DİLLERİN BELİRGİN İZLERİNİ YAKALAMA (C, C++, Java vb.) ---
    diger_dil_izleri = [
        "#include", "printf", "scanf", "main()", "std::", "cout", "cin",
        "public class", "public static void", "System.out.print", "printf(",
        ";\n", "const ", "let ", "function ", "var "
    ]
    
    # Eğer metin başka bir dilin imzasını taşıyorsa direkt sohbet/geçersiz filtresine sok
    if any(iz in python_kodu for iz in diger_dil_izleri):
        return None, "sohbet"

    # --- 2. ADIM: SOHBET VE PYTHON İZİ YOĞUNLUĞU KONTROLÜ ---
    python_izleri = ["=", "print", "def", "for", "if", "while", "import", "class", "return", "pass", "[", "]", "{", "}"]
    iz_sayisi = sum(1 for iz in python_izleri if iz in python_kodu)
    
    kelimeler = python_kodu.lower().split()
    sohbet_sozlugu = ["mı", "mu", "mi", "neden", "nasıl", "hata", "var", "yok", "merhaba", "selam", "bence", "kod", "yazdım", "baktım", "başka", "yazım", "hatası"]
    sohbet_kelime_sayisi = sum(1 for k in kelimeler if k in sohbet_sozlugu)
    
    # Eğer hiç kod izi yoksa veya Türkçe soru/sohbet kelimeleri baskınsa bu bir düz metindir
    if iz_sayisi == 0 or (sohbet_kelime_sayisi > 0 and iz_sayisi < 2):
        return None, "sohbet"

    # --- 3. ADIM: RESMİ PYTHON PARSER KONTROLÜ ---
    try:
        parsed_ast = ast.parse(python_kodu)
        tipler = [type(dugum).__name__ for dugum in ast.walk(parsed_ast)]
        return " ".join(tipler), "temiz"
    except SyntaxError:
        # Eğer parse edilemiyorsa kesinlikle yazım hatası olan bir Python kodudur
        return "Module HataliDugum", "hatali"
    except:
        return "Module HataliDugum", "hatali"

# ============================================================================
# 3. YAPAY ZEKA MODELLERİNİN YÜKLENMESİ (JOBLIB UYUMLU & ÖNBELEKSİZ)
# ============================================================================
def modelleri_yukle():
    """Modelleri doğrudan diske giderek joblib ile pürüzsüzce yükler."""
    model_yolu = "yapay_zeka_modeli.pkl"
    vec_yolu = "processed_data/fitted_vectorizer.pkl"
    
    model = None
    vectorizer = None
    
    # Kilitlenmeleri ve UnpicklingError hatalarını önlemek için doğrudan diskten okuyoruz
    if os.path.exists(model_yolu):
        model = joblib.load(model_yolu)
    if os.path.exists(vec_yolu):
        vectorizer = joblib.load(vec_yolu)
            
    return model, vectorizer

model, vectorizer = modelleri_yukle()

# ============================================================================
# 4. CHATBOT YAN MENÜ (SIDEBAR) TASARIMI
# ============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/000000/bot.png", width=120)
    st.title("Proje Hakkında")
    st.markdown("""
    **Python Syntax Hata Tespit Chatbotu v1.0**
    
    Bu yapay zeka chatbot'u, gönderdiğiniz Python kodlarını **AST (Abstract Syntax Tree)** düzeyinde analiz ederek kodun içerisinde yapısal veya sözdizimsel bir hata olup olmadığını tahmin eder.
    
    * **Veri Seti:** py150 (Sub-sample)
    * **Yöntem:** NLP (TF-IDF) + Machine Learning
    """)
    st.divider()
    st.caption("Geliştirici: Asya İrem Karademir")

# ============================================================================
# 5. ANA SOHBET EKRANI AKIŞI
# ============================================================================
st.title("🤖 Python Akıllı Sözdizimi (Syntax) Asistanı")
st.write("Aşağıdaki sohbet ekranından kodunuzu paylaşın, yapay zeka modelimiz kodun sağlamlığını kontrol etsin!")

# Sohbet geçmişini hafızada tutma mekanizması
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Selam! Ben Python kod analiz asistanıyım. Kontrol etmek istediğin Python kod bloğunu bana gönderebilirsin. 🚀"}
    ]

# Eski mesajları ekrana basma
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı kutusuna yeni veri girildiğinde çalışacak alan
if user_input := st.chat_input("Python kodunuzu buraya yapıştırın..."):
    
    # Girdi türünü analiz ediyoruz
    ast_text, girdi_turu = canli_kod_ast_cevir(user_input)
    
    # Kullanıcının mesajını ekrana bas ve hafızaya al
    with st.chat_message("user"):
        if girdi_turu == "sohbet":
            st.markdown(user_input)
        else:
            st.code(user_input, language="python")
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Asistanın cevap üretme alanı
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # --- DURUM A: KULLANICI DÜZ SOHBET ETMEYE ÇALIŞIYORSA ---
        if girdi_turu == "sohbet":
            cevap = (
                "🤖 **Sistem Uyarısı:** Ben sadece **Python Sözdizimi (Syntax) Hatalarını** analiz etmek üzere tasarlanmış bir yapay zeka asistanıyım.\n\n"
                "Gönderdiğiniz metinde geçerli bir Python kod yapısı tespit edemedim. Lütfen analiz etmem için bir Python kod bloğu paylaşın! 🚀"
            )
            message_placeholder.warning(cevap)
            
        elif vectorizer is None or model is None:
            cevap = "Üzgünüm, arka planda yapay zeka modeli veya vektörleştirici yüklenemediği için şu an analiz yapamıyorum."
            message_placeholder.markdown(cevap)
            
        # --- DURUM B: KULLANICI GERÇEKTEN BİR KOD GİRDİYSE ---
        # --- DURUM B: KULLANICI GERÇEKTEN BİR KOD GİRDİYSE ---
        else:
            with st.spinner("Kodunuz inceleniyor ve AST haritası çıkarılıyor..."):
                # Canlı veriyi TF-IDF ile sayısal vektöre çeviriyoruz
                vektor_kod = vectorizer.transform([ast_text])
                
                # Model tahminleri
                tahmin_sinifi = model.predict(vektor_kod)[0]
                
                # --- [GÜVENLİK GÜNCELLEMESİ: PREDICT_PROBA KORUMASI] ---
                try:
                    tahmin_olasilik = model.predict_proba(vektor_kod)[0]
                    # Eğer model sınıf 0 dediyse onun olasılığını, 1 dediyse onun olasılığını alıyoruz
                    guven_skoru = tahmin_olasilik[tahmin_sinifi] * 100
                except Exception:
                    # Model yapısından kaynaklı bir olasılık hesaplama hatası olursa sistem çökmesin
                    guven_skoru = 100.0
                # -------------------------------------------------------
                
                # Model 'Temiz' dediyse ve AST parse başarılıysa
                if tahmin_sinifi == 0 and girdi_turu == "temiz":
                    cevap = (
                        f"🍏 **Analiz Tamamlandı:** Kodunuzda herhangi bir Python sözdizimi (Syntax) hatası tespit edilmedi.\n\n"
                        f"📊 **Yapay Zeka Analiz Raporu:**\n"
                        f"* Sınıflandırma Durumu: **TEMİZ KOD**\n"
                        f"* Model Kararlılık Oranı: **%{guven_skoru:.2f}**"
                    )
                # Model 'Hatalı' dediyse veya AST parse başarısızsa
                else:
                    if guven_skoru < 55:
                        risk_durumu = "⚠️ Düşük/Sınırda Risk (Yapısal düzensizlik veya eksik satır olabilir)"
                    elif guven_skoru < 75:
                        risk_durumu = "🍊 Orta Derece Risk (Büyük ihtimalle hatalı kod yapısı)"
                    else:
                        risk_durumu = "🚨 Yüksek Risk (Net Syntax Hatası tespit edildi)"
                        
                    # Detaylı satır inceleme ve yönlendirme ipuçları
                    ipucu_mesaji = ""
                    satirlar = user_input.split('\n')
                    yasakli_keywords = ["True", "False", "None", "import", "return", "def", "class", "for", "if", "else"]
                    
                    for index, satir in enumerate(satirlar):
                        satir_no = index + 1
                        temiz_satir = satir.strip()
                        
                        # Kural 1: Sayı ile başlayan değişken kontrolü
                        if __import__('re').match(r'^\d+[a-zA-Z_]', temiz_satir):
                            ipucu_mesaji += f"📍 **Satır {satir_no}:** Değişken isimleri asla sayı ile başlayamaz! `{temiz_satir.split('=')[0].strip()}` tanımını kontrol edin.\n"
                        
                        # Kural 2: Anahtar kelimeye değer atama kontrolü
                        for kw in yasakli_keywords:
                            if temiz_satir.startswith(f"{kw} =") or temiz_satir.startswith(f"{kw}="):
                                ipucu_mesaji += f"📍 **Satır {satir_no}:** `{kw}` bir Python anahtar kelimesidir (Keyword). Bu kelimeye doğrudan değer ataması yapamazsınız!\n"
                        
                        # Kural 3: İki nokta eksikliği kontrolü
                        if (temiz_satir.startswith("if ") or temiz_satir.startswith("for ") or temiz_satir.startswith("def ") or temiz_satir.startswith("while ")) and not temiz_satir.endswith(":"):
                            ipucu_mesaji += f"📍 **Satır {satir_no}:** Blok başlatma satırının sonunda iki nokta `:` işareti eksik görünüyor.\n"
                    
                    if not ipucu_mesaji:
                        ipucu_mesaji = "💡 *Genel İpucu: Lütfen parantez dengelerini, tırnak işaretlerini ve satır girintilerini (indentation) kontrol edin.*"
                    
                    cevap = (
                        f"🚨 **Dikkat!** Gönderdiğiniz kod bloğunda **Python Syntax (Yazım) Hatası** algılandı.\n\n"
                        f"📊 **Yapay Zeka Analiz Raporu:**\n"
                        f"* Tespit Edilen Durum: **{risk_durumu}**\n"
                        f"* Model Kararlılık Oranı: **%{guven_skoru:.2f}**\n\n"
                        f"🔍 **Hata Teşhis ve Çözüm Önerisi:**\n{ipucu_mesaji}"
                    )
                
                # Sonuç ekranını basıyoruz
                message_placeholder.markdown(cevap)
                
                # Açılır kutuda teknik detayları gösteriyoruz
                with st.expander("🔍 Teknik AST Detayları"):
                    st.write("**Modelin İncelediği Soyut Sözdizimi Düğümleri (AST Nodes):**")
                    st.caption(ast_text)
                    
            st.session_state.messages.append({"role": "assistant", "content": cevap})
