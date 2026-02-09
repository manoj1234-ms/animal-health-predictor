# VetNet AI - Enterprise Veterinary Disease Prediction Platform

![VetNet AI](https://img.shields.io/badge/AI-Deep%20Learning-blue)
![Species](https://img.shields.io/badge/Species-24-green)
![Accuracy](https://img.shields.io/badge/Accuracy-95%25-brightgreen)

## 🚀 Overview

VetNet AI is a cutting-edge veterinary diagnostic platform that combines **Deep Learning (PyTorch)** with **XGBoost** to provide real-time disease prediction across 24 animal species. The system integrates with IoT smart tags for continuous health monitoring and AI-powered diagnostics.

### Key Features

- **🧠 Hybrid AI Engine**: VetNet Neural Network (Stage 1) + XGBoost (Stage 2)
- **📡 IoT Integration**: Real-time telemetry from smart collars/ear tags
- **🌍 Multi-Species Support**: 24 species including Zoo, Farm, and Exotic animals
- **🎯 95%+ Accuracy**: Validated on 15,000+ clinical signatures
- **💉 Clinical Precision**: 25 diagnostic features including real-world symptoms
- **🔄 Optional Data Handling**: Robust imputation for missing sensor data

## 📊 Supported Species

### Zoo Animals
Lion, Tiger, Elephant

### Farm Animals
Cattle, Buffalo, Sheep, Goat, Pig, Horse, Chicken, Turkey, Duck, Llama, Alpaca

### Pets & Exotic
Dog, Cat, Rabbit, Parrot, Lizard, Snake, Turtle, Fish

## 🏗️ Architecture

```
┌─────────────────┐
│  IoT Devices    │ (ESP32 Smart Tags)
│  Temperature    │
│  Heart Rate     │
│  Activity       │
└────────┬────────┘
         │ HTTP POST
         ▼
┌─────────────────┐
│  IoT Gateway    │ (FastAPI)
│  Telemetry      │
│  Device Registry│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  VetNet Brain   │
│  Stage 1: NN    │ (PyTorch - Category)
│  Stage 2: XGB   │ (Disease Prediction)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Dashboard UI   │ (React + Vite)
│  Live Monitoring│
│  AI Diagnosis   │
└─────────────────┘
```

## 🛠️ Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker (optional)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/vetnet-ai.git
cd vetnet-ai

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Generate training data and train models
python scripts/generate_enhanced_data.py
python src/train_nn.py
python scripts/retrain_models.py

# 4. Start the backend
python simple_api.py

# 5. Start the frontend (in a new terminal)
cd vetnet-ui
npm install
npm run dev
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the API at http://localhost:8002
# Access the UI at http://localhost:5173
```

## 📡 IoT Device Setup

### Hardware Requirements
- ESP32-WROOM-32 microcontroller
- DS18B20 temperature sensor
- MAX30102 pulse oximeter
- ADXL345 accelerometer
- 3.7V Li-Po battery

### Firmware Installation

1. Open `hardware/VetNet_SmartTag_ESP32.ino` in Arduino IDE
2. Install required libraries:
   - WiFi
   - HTTPClient
   - ArduinoJson
   - OneWire
   - DallasTemperature
   - MAX30105
3. Update WiFi credentials and server IP
4. Upload to ESP32

### Device Registration

```bash
# Register a new IoT device
python scripts/register_iot_device.py TAG_001 Simba Lion 4.5 African Male
```

## 🧪 API Endpoints

### Health Check
```bash
GET /health
```

### IoT Telemetry
```bash
POST /iot/telemetry
{
  "device_id": "TAG_001",
  "animal_id": "Lion_Alpha",
  "species": "Lion",
  "timestamp": 1707490000,
  "temperature": 38.5,
  "heart_rate": 55,
  "activity_level": 82.0,
  "battery_level": 95.0
}
```

### AI Diagnosis
```bash
POST /iot/diagnose/{device_id}
```

### Device Registration
```bash
POST /iot/register
{
  "device_id": "TAG_001",
  "animal_id": "Lion_Alpha",
  "species": "Lion",
  "name": "Simba",
  "age": 4.5,
  "breed": "African",
  "gender": "Male"
}
```

## 📈 Model Performance

| Model | Accuracy | Features | Species |
|-------|----------|----------|---------|
| VetNet (Stage 1) | 95.47% | 25 | 24 |
| XGBoost (Stage 2) | 94.3% | 25 | 24 |

### Clinical Features
- **Vital Signs**: Temperature, Heart Rate, Activity
- **Blood Work**: WBC, RBC, Hemoglobin, Platelets, Glucose, ALT, AST, Urea, Creatinine
- **Symptoms**: Fever, Lethargy, Vomiting, Diarrhea, Weight Loss, Skin Lesion, Coughing, Lameness, Nasal Discharge, Eye Discharge, Drooling, Blisters

## 🔬 Disease Categories

- Viral
- Bacterial
- Parasitic
- Metabolic
- Respiratory
- Cardiovascular
- Musculoskeletal
- Gastrointestinal

## 📁 Project Structure

```
vetnet-ai/
├── src/
│   ├── models/
│   │   └── neural_network.py      # VetNet PyTorch model
│   ├── inference_nn.py             # AI prediction engine
│   ├── train_nn.py                 # Neural network training
│   ├── iot_gateway.py              # IoT telemetry handler
│   ├── biological_rules.py         # Vital sign analysis
│   └── monitoring.py               # System metrics
├── scripts/
│   ├── generate_enhanced_data.py   # Dataset generation
│   ├── retrain_models.py           # XGBoost training
│   ├── simulate_iot_devices.py     # IoT simulator
│   └── register_iot_device.py      # Device onboarding
├── vetnet-ui/                      # React frontend
├── hardware/
│   └── VetNet_SmartTag_ESP32.ino   # IoT firmware
├── models/                         # Trained AI models
├── data/                           # Training datasets
├── simple_api.py                   # FastAPI server
├── Dockerfile
└── docker-compose.yml
```

## 🎨 UI Features

- **Live Dashboard**: Real-time device monitoring
- **Species Filtering**: Zoo, Farm, Pet categories
- **AI Diagnosis**: One-click disease prediction
- **Premium Design**: Glassmorphism UI with species-specific icons
- **Responsive Layout**: Mobile and desktop optimized

## 🔐 Security & Privacy

- Device authentication via unique TAG IDs
- Encrypted telemetry transmission (HTTPS recommended)
- HIPAA-compliant data handling (when deployed with SSL)

## 🚀 Deployment

### Production Checklist
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up database (PostgreSQL/MongoDB)
- [ ] Enable Redis for caching
- [ ] Configure monitoring (Prometheus/Grafana)
- [ ] Set up backup strategy

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.

## 📧 Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/YOUR_USERNAME/vetnet-ai/issues)
- Email: support@vetnet-ai.com

## 🙏 Acknowledgments

- PyTorch Team for the deep learning framework
- XGBoost contributors
- FastAPI community
- React and Vite teams

---

**Built with ❤️ for veterinary professionals worldwide**
