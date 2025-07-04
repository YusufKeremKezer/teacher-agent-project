# AI Öğretmen Ajanı Projesi 🎓

Bu proje, ünlü AI uzmanlarının öğretim tarzlarını taklit eden bir yapay zeka sohbet uygulamasıdır. Kullanıcılar farklı AI öğretmenlerinden (Andrej Karpathy, Sam Altman, Andrew Ng, Ramin Hasani, François Chollet) seçim yaparak onların benzersiz öğretim tarzlarında AI ve teknoloji konularında mentorluk alabilirler.

## 🎯 Projenin Amacı

Bu proje, **AI eğitimi ve mentorluğu demokratikleştirmeyi** hedefleyen bir platform olarak tasarlanmıştır. Temel amaçları:

1. **Kişiselleştirilmiş AI Eğitimi**: Kullanıcıların farklı öğrenme stillerine uygun, ünlü AI uzmanlarının yaklaşımlarını taklit eden mentorlar sunmak
2. **Erişilebilir Uzman Bilgisi**: Normalde ulaşılması zor olan dünya çapındaki AI liderlerinin bilgi ve perspektiflerini herkesin erişimine açmak
3. **İnteraktif Öğrenme Deneyimi**: Tek yönlü bilgi aktarımı yerine, sohbet tabanlı interaktif bir öğrenme ortamı sağlamak
4. **Bağlamsal Öğretim**: Her öğretmenin kendi uzmanlık alanı, öğretim stili ve perspektifiyle özelleştirilmiş yanıtlar sunmak

## 🌟 Özellikler

- **5 Farklı AI Öğretmeni**: Her biri kendi uzmanlık alanı ve öğretim tarzına sahip
- **Gerçek Zamanlı Sohbet**: FastAPI backend ile güçlendirilmiş hızlı yanıtlar
- **Kişiselleştirilmiş Öğretim**: Her öğretmenin kendine özgü perspektifi ve yaklaşımı
- **Modern Kullanıcı Arayüzü**: React ve Tailwind CSS ile geliştirilmiş responsive tasarım
- **Konuşma Hafızası**: MongoDB ile kalıcı sohbet geçmişi
- **LangChain/LangGraph Entegrasyonu**: Gelişmiş AI konuşma yönetimi
- **Domain Driven Design**: Temiz, ölçeklenebilir ve bakımı kolay mimari

## 🏗️ Teknoloji Yığını

### Backend (API)
- **FastAPI**: Modern, hızlı web framework
- **LangChain & LangGraph**: AI konuşma orkestrasyon
- **Google Generative AI**: Dil modeli entegrasyonu
- **MongoDB**: Konuşma durumu ve vektör veritabanı
- **Python 3.12+**: Ana programlama dili

### Frontend (UI)
- **React 19**: Kullanıcı arayüzü framework'ü
- **Vite**: Hızlı geliştirme ve build aracı
- **Tailwind CSS**: Utility-first CSS framework
- **JavaScript (ES6+)**: Modern JavaScript özellikleri

## 📋 Gereksinimler

- Python 3.12 veya üzeri
- Node.js 16+ ve npm
- MongoDB (Atlas veya yerel kurulum)
- Google Generative AI API anahtarı

## 🚀 Kurulum

### 1. Projeyi Klonlayın

```bash
git clone <repository-url>
cd teacher-agent-project
```

### 2. Backend Kurulumu

```bash
cd api

# Python sanal ortamını oluşturun
python -m venv .venv

# Sanal ortamı aktifleştirin
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# .env dosyasını oluşturun ve yapılandırın
cp .env.example .env
# .env dosyasını düzenleyerek gerekli API anahtarlarını ekleyin
```

### 3. Frontend Kurulumu

```bash
cd ui

# Bağımlılıkları yükleyin
npm install
```

## 🔧 Yapılandırma

### Backend (.env dosyası)
```env
# MongoDB bağlantı bilgileri
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DB_NAME=teacher_agent_db

# Google AI API anahtarı
GOOGLE_API_KEY=your-google-api-key

# Diğer ayarlar
TOTAL_MESSAGES_SUMMARY_TRIGGER=10
```

## 🎯 Kullanım

### Geliştirme Ortamını Başlatma

#### Tek Komutla (Önerilen)
```bash
./start-dev.sh
```

#### Manuel Başlatma
```bash
# Terminal 1 - Backend
cd api
python -m uvicorn src.maestro.infrastructure.api:app --reload --port 8000

# Terminal 2 - Frontend  
cd ui
npm run dev
```

### Erişim Noktaları

- **Frontend UI**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Dokümantasyonu**: http://localhost:8000/docs

## 👨‍🏫 Mevcut Öğretmenler

### 1. Andrej Karpathy
- **Uzmanlık**: Derin Öğrenme, Bilgisayarlı Görü, Sinir Ağları
- **Tarz**: Pratik mühendis ve hikaye anlatıcı yaklaşımı

### 2. Sam Altman  
- **Uzmanlık**: AI Stratejisi, Startup Geliştirme, AI Yönetişimi
- **Tarz**: Stratejik fütürist ve vizyon sahibi

### 3. Andrew Ng
- **Uzmanlık**: Makine Öğrenmesi Eğitimi, Pratik AI Uygulamaları
- **Tarz**: Sakin ve metodik profesör yaklaşımı

### 4. Ramin Hasani
- **Uzmanlık**: Sıvı Sinir Ağları, Biyo-ilhamlı AI, Robotik
- **Tarz**: Araştırma odaklı, ileri teknoloji yaklaşımı

### 5. François Chollet
- **Uzmanlık**: Derin Öğrenme Teorisi, AI Etiği, Keras Framework
- **Tarz**: Felsefi kodlayıcı ve eleştirel düşünür

## 📡 API Endpoints

### POST /chat
Öğretmenle sohbet mesajı gönderir.

**Request Body:**
```json
{
  "message": "Yapay zeka hakkında ne düşünüyorsunuz?",
  "teacher_id": "karpathy"
}
```

**Response:**
```json
{
  "response": "Öğretmenin yanıtı..."
}
```

### POST /reset-memory
Konuşma durumunu sıfırlar.

## 🏛️ Domain Driven Design (DDD) Mimarisi

Proje, DDD prensiplerini takip eden katmanlı bir mimari kullanır:

### Domain Katmanı (`api/src/maestro/domain/`)
İş mantığının kalbi. Temel domain kavramları:

- **Teacher (Öğretmen)**: Sistemin merkezi domain modeli
  - `id`: Benzersiz tanımlayıcı
  - `name`: Öğretmen adı  
  - `expertise`: Uzmanlık alanları
  - `perspective`: Öğretmenin bakış açısı
  - `style`: Öğretim tarzı

- **Value Objects**:
  - `Prompt`: Öğretmen karakterini tanımlayan prompt şablonları
  - `TeacherExtract`: Dış kaynaklardan çekilen öğretmen verileri

- **Domain Exceptions**: İş kuralı ihlallerini temsil eden özel hatalar

### Application Katmanı (`api/src/maestro/application/`)
Use case'leri ve iş akışlarını yöneten katman:

- **Conversation Service**: Sohbet yönetimi
  - LangGraph tabanlı konuşma akışı
  - Konuşma durumu yönetimi (TeacherState)
  - Akış düğümleri ve LangChain zincirleri

- **RAG (Retrieval Augmented Generation)**: Bilgi erişimi
  - Metin vektörleri ve MongoDB vektör araması
  - Dinamik bilgi erişimi için retriever'lar

### Infrastructure Katmanı (`api/src/maestro/infrastructure/`)
Dış sistemlerle etkileşim:

- **API Layer**: FastAPI REST endpoint'leri
- **Persistence**: MongoDB ve LangGraph checkpoint yönetimi

### DDD Kavramları
1. **Bounded Context**: Teacher, Conversation ve Knowledge bağlamları
2. **Aggregates**: Teacher ve Conversation kümeleri
3. **Factories**: `TeacherFactory` ile tutarlı nesne oluşturma
4. **Domain Services**: Konuşma ve hafıza yönetimi servisleri

## 🔄 Proje Yapısı

```
teacher-agent-project/
├── api/                    # Backend API
│   ├── src/               
│   │   └── maestro/       
│   │       ├── application/    # Uygulama mantığı
│   │       ├── domain/         # Domain modelleri
│   │       └── infrastructure/ # API ve altyapı
│   ├── requirements.txt        # Python bağımlılıkları
│   └── langgraph.json         # LangGraph yapılandırması
│
├── ui/                     # Frontend
│   ├── src/
│   │   ├── components/    # React bileşenleri
│   │   ├── data/         # Öğretmen verileri
│   │   └── services/     # API servisleri
│   ├── package.json      # Node bağımlılıkları
│   └── vite.config.js    # Vite yapılandırması
│
├── start-dev.sh          # Geliştirme başlatma scripti
└── README.md            # Bu dosya
```

## 🛠️ Geliştirme

### Backend Geliştirme
- LangGraph workflow'ları `api/src/maestro/application/conversation_service/workflow/` dizininde
- Öğretmen tanımlamaları `api/src/maestro/domain/teacher_factory.py` dosyasında
- API endpoint'leri `api/src/maestro/infrastructure/api.py` dosyasında

### Frontend Geliştirme
- React bileşenleri `ui/src/components/` dizininde
- Öğretmen verileri `ui/src/data/teachers.js` dosyasında
- API servisleri `ui/src/services/api.js` dosyasında

### Mimari Avantajları

1. **Separation of Concerns**: Her katman kendi sorumluluğuna odaklanır
2. **Testability**: Domain mantığı altyapıdan bağımsız test edilebilir
3. **Flexibility**: Altyapı değişiklikleri domain'i etkilemez
4. **Maintainability**: Kod organizasyonu net ve anlaşılır
5. **Scalability**: Yeni öğretmenler ve özellikler kolayca eklenebilir

### Event-Driven Yaklaşım

Proje, LangGraph ile event-driven bir yaklaşım kullanır:
- **State Transitions**: Konuşma durumu değişiklikleri event olarak ele alınır
- **Message Flow**: Her mesaj bir event tetikler
- **Tool Calls**: RAG aramaları asenkron event'ler olarak işlenir

## 🐛 Sorun Giderme

### MongoDB Bağlantı Hatası
- MongoDB URI'nizin doğru olduğundan emin olun
- Ağ erişim ayarlarını kontrol edin (IP whitelist)

### API Anahtarı Hatası
- Google API anahtarınızın geçerli olduğundan emin olun
- .env dosyasının doğru konumda olduğunu kontrol edin

### Port Çakışması
- 8000 ve 5173 portlarının kullanımda olmadığından emin olun
- Gerekirse farklı portlar kullanın

## 📝 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

1. Projeyi fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📧 İletişim

Proje ile ilgili sorularınız için issue açabilir veya pull request gönderebilirsiniz.
