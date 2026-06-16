# Yapay Zeka Destekli CV Skorlama ve Filtreleme Sistemi

## 1. Proje Özeti

Bu proje, yazılım geliştirme pozisyonlarına başvuran adayların CV dosyalarını merkezi bir web arayüzü üzerinden kabul eden, PDF içeriklerini işleyen ve yerel bir yapay zeka modeli yardımıyla çok kriterli aday değerlendirmesi yapan full-stack bir uygulamadır.

Sistem, yüklenen CV dosyalarından metin çıkarır, her adayı beş temel kriter altında puanlar, ortalama başarı skorunu hesaplar ve en yüksek skora sahip adayları sıralı şekilde kullanıcıya sunar.

Temel hedef, çok sayıda CV arasından uygun adayları daha hızlı, tutarlı ve ölçülebilir şekilde ön değerlendirmeye almaktır.

## 2. Kapsam ve Temel Yetenekler

Uygulama aşağıdaki temel işlevleri sağlar:

- Çoklu PDF CV yükleme
- PDF metin çıkarma
- Yerel Ollama modeli ile aday analizi
- Beş kriterli aday skorlama
- Ortalama skor hesaplama
- En yüksek skorlu adayların sıralanması
- Web arayüzünde sonuçların görselleştirilmesi
- Sistem sağlık kontrolü
- Model bağlantı kontrolü
- Hatalı dosya, boş içerik ve model yanıtı problemleri için hata toleransı

## 3. Proje Ödevi Gereksinim Uyumluluğu

Proje, `Yapay Zeka Mülakat Proje Ödevi.pdf` dosyasında belirtilen işlevsel ve teknik beklentiler dikkate alınarak geliştirilmiştir. Aşağıdaki tablo, ödev dokümanındaki ana gereksinimlerin projede nasıl karşılandığını özetler.

| Ödev Beklentisi | Projedeki Karşılığı | İlgili Dosya veya Bölüm | Durum |
| --- | --- | --- | --- |
| Merkezi web arayüzü üzerinden CV kabul edilmesi | Kullanıcı PDF CV dosyalarını web arayüzünden yükleyebilir. | `frontend/index.html`, `frontend/app.js` | Karşılandı |
| PDF formatında en az 10 gerçekçi mock CV üretilmesi | `mock_cvs` klasöründe farklı deneyim seviyelerine sahip 10 adet CV PDF'i bulunmaktadır. | `mock_cvs/generate_cvs.py`, `mock_cvs/*.pdf` | Karşılandı |
| Çoklu dosya yükleme desteği | Arayüz birden fazla PDF dosyasını aynı anda seçip backend'e gönderebilir. | `frontend/app.js` | Karşılandı |
| Backend ile asenkron iletişim | Frontend, `fetch` ve `FormData` kullanarak analiz isteğini asenkron olarak gönderir. | `frontend/app.js` | Karşılandı |
| Analizi tetikleyen kontrol mekanizması | Arayüzde `Analyze CVs` butonu ile analiz süreci başlatılır. | `frontend/index.html`, `frontend/app.js` | Karşılandı |
| PDF metin çıkarma | Backend, PyMuPDF ile PDF dosyalarından metin çıkarır. | `backend/app/services/pdf_service.py` | Karşılandı |
| Yerel LLM ile haberleşme | Çıkarılan metinler Ollama üzerinde çalışan `llama3` modeline gönderilir. | `backend/app/services/scoring_service.py` | Karşılandı |
| Prompt mühendisliği şablonu | CV metni kontrollü bir prompt şablonuna yerleştirilir. | `backend/app/utils/prompt_builder.py` | Karşılandı |
| Beş kriterli skorlama | Eğitim, yabancı dil, proje, staj ve AI yetkinliği için ayrı skorlar üretilir. | `backend/app/models/candidate.py`, `backend/app/services/scoring_service.py` | Karşılandı |
| Skorların 1-100 aralığında olması | Backend skorları normalize ederek 1-100 aralığında tutar. | `backend/app/services/scoring_service.py` | Karşılandı |
| Ortalama skor hesaplama | Beş skorun aritmetik ortalaması backend'de hesaplanır. | `DetailedScores.average()` | Karşılandı |
| Adayların ortalama skora göre sıralanması | Adaylar `averageScore` değerine göre büyükten küçüğe sıralanır. | `backend/app/services/scoring_service.py` | Karşılandı |
| İlk 5 adayın listelenmesi | `top_n=5` parametresiyle en iyi 5 aday döndürülür. | `/api/v1/analyze?top_n=5` | Karşılandı |
| Beklenen JSON çıktı formatı | Response içinde `status`, `processedCVCount`, `topCandidates`, `rank`, `candidateName`, `pdfFileName`, `detailedScores`, `averageScore`, `shortEvaluation` alanları bulunur. | `backend/app/dto/response_dto.py` | Karşılandı |
| Controller, Service, DTO ve Model katmanları | Backend katmanlı mimariyle ayrıştırılmıştır. | `backend/app/controllers`, `services`, `dto`, `models` | Karşılandı |
| Prompt kararlılığı | Modelden yalnızca yapılandırılmış JSON ve sayısal skorlar istenir; backend parse ve normalize işlemi yapar. | `prompt_builder.py`, `scoring_service.py` | Karşılandı |
| Asenkron işlem ve loading göstergesi | Frontend analiz sürecinde progress bar, aşama göstergeleri ve loading state gösterir. | `frontend/app.js`, `frontend/index.html` | Karşılandı |
| Hata ve istisna yönetimi | PDF, dosya boyutu, boş içerik, Ollama bağlantısı, model timeout ve beklenmeyen cevap durumları yönetilir. | `cv_controller.py`, `pdf_service.py`, `scoring_service.py` | Karşılandı |
| Kod temizliği ve okunabilirlik | Sorumluluklar ayrı katmanlara bölünmüş, API şemaları ve servisler ayrıştırılmıştır. | Proje geneli | Karşılandı |

Bu değerlendirmeye göre ödev dokümanında açıkça belirtilen zorunlu maddeler proje kapsamında karşılanmıştır. Ek olarak GPU hızlandırma, demo başlangıç scriptleri, sağlık kontrol endpointleri ve doğrulama raporu gibi teslim kalitesini artıran destekleyici geliştirmeler de eklenmiştir.

## 4. Kullanılan Teknolojiler

### Backend

- Python
- FastAPI
- Pydantic
- PyMuPDF
- httpx
- python-dotenv
- Ollama
- Llama3

### Frontend

- HTML
- CSS
- Vanilla JavaScript

### PDF Üretimi

- ReportLab
- Unicode destekli TrueType font gömme

### Çalıştırma ve Demo Ortamı

- PowerShell yardımcı scriptleri
- NVIDIA GPU hızlandırma
- Ollama local inference

## 5. Sistem Mimarisi

Proje katmanlı bir mimariyle yapılandırılmıştır. Backend tarafında controller, service, model, DTO ve utility katmanları ayrıştırılmıştır.

```text
CV_Analysis/
  backend/
    main.py
    app/
      controllers/
      services/
      models/
      dto/
      utils/
  frontend/
    index.html
    styles.css
    app.js
  mock_cvs/
    generate_cvs.py
    *.pdf
  scripts/
    start_demo.ps1
    check_ollama_gpu.ps1
```

Bu yapı, HTTP katmanı, iş mantığı, veri modelleri ve yardımcı fonksiyonların birbirinden ayrılmasını sağlar.

## 6. Önemli Dosyalar

| Dosya | Açıklama |
| --- | --- |
| `backend/main.py` | FastAPI uygulamasının başlangıç noktasıdır. |
| `backend/app/controllers/cv_controller.py` | API endpointlerini içerir. |
| `backend/app/services/pdf_service.py` | PDF dosyalarından metin çıkarma işlemini yapar. |
| `backend/app/services/scoring_service.py` | Ollama entegrasyonu, skor işleme ve aday sıralama mantığını içerir. |
| `backend/app/utils/prompt_builder.py` | LLM'e gönderilen prompt şablonunu üretir. |
| `backend/app/models/candidate.py` | Aday ve skor veri modellerini içerir. |
| `backend/app/dto/response_dto.py` | API response şemalarını tanımlar. |
| `frontend/index.html` | Web arayüzünün HTML yapısıdır. |
| `frontend/styles.css` | Arayüz tasarım ve responsive stil kurallarını içerir. |
| `frontend/app.js` | Dosya yükleme, API çağrısı ve sonuç render işlemlerini yönetir. |
| `mock_cvs/generate_cvs.py` | Örnek CV PDF dosyalarını üretir. |
| `scripts/start_demo.ps1` | Demo için Ollama ve backend servislerini hazırlar. |
| `scripts/check_ollama_gpu.ps1` | Ollama GPU kullanımını doğrular. |

## 7. Çalışma Akışı

Sistem aşağıdaki işlem sırasına göre çalışır:

1. Kullanıcı web arayüzünden bir veya birden fazla PDF CV seçer.
2. Frontend, seçilen dosyaları `FormData` ile backend API'ye gönderir.
3. Backend dosyaları doğrular:
   - Dosya PDF formatında mı?
   - Dosya boş mu?
   - Dosya boyutu limitler içinde mi?
4. `PDFService`, PyMuPDF kullanarak PDF içeriğinden metin çıkarır.
5. Çıkarılan CV metni prompt şablonuna yerleştirilir.
6. `ScoringService`, prompt'u Ollama üzerinde çalışan `llama3` modeline gönderir.
7. Modelden aday adı ve detay skorları beklenir.
8. Backend skorları normalize eder.
9. Beş kriterin aritmetik ortalaması alınarak `averageScore` hesaplanır.
10. Backend, skorlara göre profesyonel kısa değerlendirme metnini oluşturur.
11. Adaylar ortalama skora göre büyükten küçüğe sıralanır.
12. İstenen sayıda aday frontend'e JSON olarak döndürülür.
13. Frontend sonuçları aday kartları ve skor barlarıyla gösterir.

## 8. Skorlama Kriterleri

Her aday aşağıdaki beş kriter altında 1 ile 100 arasında puanlanır:

| Kriter | Açıklama |
| --- | --- |
| `universityAndDepartment` | Üniversite, bölüm uygunluğu, akademik başarı |
| `foreignLanguages` | İngilizce seviyesi ve ek yabancı diller |
| `projects` | Kişisel projeler, takım projeleri, GitHub veya açık kaynak katkıları |
| `internships` | Staj sayısı, staj kalitesi, sektör deneyimi |
| `aiCompetency` | Yapay zeka, makine öğrenmesi, LLM, RAG veya ilgili teknik deneyim |

Ortalama skor backend tarafında hesaplanır:

```text
averageScore = (universityAndDepartment + foreignLanguages + projects + internships + aiCompetency) / 5
```

## 9. API Endpointleri

### Tarayıcıda Açılabilecek Bağlantılar

Demo veya teknik kontrol sırasında aşağıdaki bağlantılar doğrudan tarayıcıda açılabilir:

| Bağlantı | Ne İşe Yarar |
| --- | --- |
| `http://127.0.0.1:8000` | Ana web arayüzünü açar. CV yükleme ve analiz işlemi buradan yapılır. |
| `http://127.0.0.1:8000/docs` | FastAPI Swagger arayüzünü açar. API endpointleri buradan test edilebilir. |
| `http://127.0.0.1:8000/redoc` | Alternatif FastAPI API dokümantasyon ekranıdır. |
| `http://127.0.0.1:8000/openapi.json` | Backend'in OpenAPI şemasını JSON formatında gösterir. |
| `http://127.0.0.1:8000/api/v1/health` | Backend ve Ollama bağlantı durumunu gösterir. |
| `http://127.0.0.1:8000/api/v1/models` | Backend üzerinden erişilebilen Ollama modellerini listeler. |
| `http://127.0.0.1:11434` | Ollama servisinin çalışıp çalışmadığını gösterir. |
| `http://127.0.0.1:11434/api/tags` | Ollama üzerinde yüklü modelleri doğrudan listeler. |

Analiz endpoint'i `POST` isteği beklediği için tarayıcı adres çubuğundan doğrudan kullanılmaz. Analiz için ana arayüz veya Swagger kullanılmalıdır:

```text
POST http://127.0.0.1:8000/api/v1/analyze?top_n=5
```

### Ana Arayüz

```text
GET http://127.0.0.1:8000
```

Web arayüzünü açar.

### Swagger Dokümantasyonu

```text
GET http://127.0.0.1:8000/docs
```

FastAPI tarafından otomatik oluşturulan API dokümantasyonunu gösterir.

### Sağlık Kontrolü

```text
GET http://127.0.0.1:8000/api/v1/health
```

Backend ve Ollama bağlantı durumunu döndürür.

Örnek yanıt:

```json
{
  "status": "ok",
  "ollama_connected": true,
  "available_models": ["llama3:latest"],
  "active_model": "llama3:latest"
}
```

### Model Listesi

```text
GET http://127.0.0.1:8000/api/v1/models
```

Ollama üzerinde yüklü modelleri listeler.

### CV Analizi

```text
POST http://127.0.0.1:8000/api/v1/analyze?top_n=5
```

PDF CV dosyalarını analiz eder ve en yüksek skorlu adayları döndürür.

Örnek response yapısı:

```json
{
  "status": "success",
  "processedCVCount": 10,
  "topCandidates": [
    {
      "rank": 1,
      "candidateName": "Berk Kaya",
      "pdfFileName": "cv_berk_kaya.pdf",
      "detailedScores": {
        "universityAndDepartment": 90,
        "foreignLanguages": 90,
        "projects": 95,
        "internships": 85,
        "aiCompetency": 88
      },
      "averageScore": 89.6,
      "shortEvaluation": "Aday güçlü proje ve yapay zeka deneyimiyle öne çıkıyor."
    }
  ]
}
```

## 10. Kurulum ve Çalıştırma

### 10.1. Proje Klasörüne Gitme

```powershell
cd C:\Users\Mehmet\Desktop\CV_Analysis
```

### 10.2. Demo Ortamını Başlatma

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_demo.ps1
```

Başarılı çıktı:

```text
Demo is ready: http://127.0.0.1:8000
```

### 10.3. GPU Kullanımını Kontrol Etme

```powershell
ollama ps
```

Beklenen örnek çıktı:

```text
PROCESSOR
22%/78% CPU/GPU
```

Bu çıktı, modelin GPU hızlandırmasından yararlandığını gösterir.

### 10.4. Manuel Başlatma

Yardımcı script kullanılmadan manuel başlatmak için:

```powershell
ollama serve
```

Ayrı bir PowerShell penceresinde:

```powershell
cd C:\Users\Mehmet\Desktop\CV_Analysis\backend
uvicorn main:app --reload --port 8000
```

Ardından tarayıcıda:

```text
http://127.0.0.1:8000
```

## 11. Demo Akışı

1. `scripts/start_demo.ps1` ile servisleri başlat.
2. Tarayıcıda `http://127.0.0.1:8000` adresini aç.
3. Sağ üstte Ollama bağlantı durumunun başarılı olduğunu kontrol et.
4. `mock_cvs` klasöründeki PDF CV dosyalarını seç.
5. `Top candidates` değerini 5 olarak bırak.
6. `Analyze CVs` butonuna bas.
7. Analiz tamamlandığında ilk 5 adayın sıralandığını göster.
8. Aday kartlarında ortalama skor, detay skorları ve kısa değerlendirme alanlarını açıkla.

## 12. Hata Yönetimi ve Dayanıklılık

Uygulama aşağıdaki durumlara karşı kontrollü davranır:

- PDF olmayan dosya yüklenmesi
- Boş dosya yüklenmesi
- Dosya boyutu limitinin aşılması
- PDF metninin çıkarılamaması
- Ollama servisinin kapalı olması
- Modelin beklenmeyen formatta yanıt üretmesi
- GPU/CUDA tarafında runtime hatası oluşması

GPU tarafında hata oluşursa backend CPU fallback mekanizmasıyla analiz sürecini devam ettirebilir. Bu sayede tek bir model veya GPU hatası tüm analiz sürecini durdurmaz.

## 13. PDF Üretimi ve Türkçe Karakter Desteği

Mock CV dosyaları `mock_cvs/generate_cvs.py` ile üretilir. PDF üretiminde ReportLab kullanılır.

Türkçe karakterlerin doğru görünmesi ve PDF metin çıkarma sırasında bozulmaması için Unicode destekli TrueType font gömülür. Bu sayede aşağıdaki gibi isimler doğru şekilde işlenir:

```text
Ayşe Kılıç
Furkan Doğan
Merve Yıldız
Selin Çelik
Simge Aktaş
```

## 14. Teknik Kararlar

### FastAPI Kullanımı

FastAPI; dosya yükleme, asenkron endpoint yapısı, otomatik Swagger dokümantasyonu ve Pydantic entegrasyonu nedeniyle tercih edilmiştir.

### Ollama Kullanımı

Ollama, yerel LLM çalıştırmayı sağladığı için tercih edilmiştir. Bu yaklaşım CV içeriklerinin dış bir servise gönderilmeden analiz edilmesini sağlar.

### PyMuPDF Kullanımı

PDF metin çıkarma için PyMuPDF kullanılmıştır. Text-based PDF CV dosyalarında hızlı ve yeterli doğrulukta metin çıkarımı sağlar.

### Veritabanı Eklenmemesi

Case kapsamında kalıcı analiz geçmişi veya kullanıcı yönetimi istenmediği için veritabanı eklenmemiştir. Sistem stateless çalışır: dosyalar yüklenir, analiz edilir ve sonuç döndürülür.

Bu karar, proje kapsamını sade tutar ve ana iş akışının güvenilirliğine odaklanır.

## 15. Performans Durumu

NVIDIA driver güncellemesi sonrası Ollama GPU hızlandırması aktif hale getirilmiştir. Tam demo senaryosunda 10 PDF analizi yaklaşık 1 dakika civarında tamamlanabilmektedir.

Kontrol komutu:

```powershell
ollama ps
```

GPU kullanımını gösteren örnek:

```text
22%/78% CPU/GPU
```

## 16. Doğrulama Özeti

Proje aşağıdaki açılardan doğrulanmıştır:

- 10 PDF dosyası üretildi.
- PDF dosyaları açıldı ve metinleri çıkarıldı.
- Türkçe karakterler doğru işlendi.
- Ollama bağlantısı doğrulandı.
- GPU kullanımı doğrulandı.
- API health endpoint'i başarılı döndü.
- CV analiz endpoint'i 10 PDF ile test edildi.
- Ortalama skorların doğru hesaplandığı kontrol edildi.
- Aday sıralamasının ortalama skora göre yapıldığı doğrulandı.

## 17. Sık Sorulabilecek Sorular

### Projenin amacı nedir?

Yüklenen CV dosyalarını yerel yapay zeka modeliyle analiz ederek adayları objektif kriterlere göre puanlamak ve en iyi adayları sıralamaktır.

### PDF metni nerede çıkarılıyor?

`backend/app/services/pdf_service.py` dosyasında PyMuPDF kullanılarak çıkarılır.

### Yapay zeka analizi nerede yapılıyor?

`backend/app/services/scoring_service.py` dosyasında Ollama API çağrısı yapılır ve model yanıtı işlenir.

### Prompt nerede tanımlı?

`backend/app/utils/prompt_builder.py` dosyasında tanımlıdır.

### Ortalama skor nerede hesaplanıyor?

`backend/app/models/candidate.py` içindeki `DetailedScores.average()` metodu ile hesaplanır.

### Neden veritabanı yok?

Case kapsamında kalıcı veri saklama istenmediği için veritabanı eklenmemiştir. Uygulama analiz isteğine yanıt üretir ve stateless çalışır.

### GPU çalışıyor mu nasıl kontrol edilir?

`ollama ps` komutu çalıştırılır. `PROCESSOR` kolonunda `CPU/GPU` ifadesi görülüyorsa GPU kullanılmaktadır.

### Ollama kapalıysa ne olur?

Health endpoint `degraded` durumunu döndürür ve frontend kullanıcıya bağlantı problemi gösterir.

## 18. Kısa Sunum Metni

Bu proje, yazılım geliştirici adaylarının CV dosyalarını toplu şekilde analiz eden bir full-stack uygulamadır. Kullanıcı arayüzünden PDF CV dosyaları yüklenir. Backend tarafında dosyalar doğrulanır ve PyMuPDF ile metin içerikleri çıkarılır. Çıkarılan metinler, belirli bir prompt şablonuyla Ollama üzerinde çalışan Llama3 modeline gönderilir.

Model her adayı eğitim, yabancı dil, proje deneyimi, staj/sektör tecrübesi ve yapay zeka yetkinliği kriterlerine göre puanlar. Backend bu puanların ortalamasını hesaplar, adayları büyükten küçüğe sıralar ve en iyi adayları frontend'e döndürür.

Uygulamada katmanlı backend mimarisi, çoklu dosya yükleme, hata yönetimi, yerel LLM entegrasyonu, GPU hızlandırma ve Türkçe karakter destekli PDF üretimi bulunmaktadır.
