# VetNet AI Deployment Guide

## 🚀 Quick Start Commands

### Local Development
```bash
# Backend
python simple_api.py

# Frontend
cd vetnet-ui
npm run dev
```

### Docker Deployment
```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down
```

## 📦 GitHub Setup

### First Time Setup
```bash
# Initialize repository
git init
git add .
git commit -m "Initial VetNet AI Platform"

# Connect to GitHub
git remote add origin https://github.com/YOUR_USERNAME/vetnet-ai.git
git branch -M main
git push -u origin main
```

### Update Existing Repository
```bash
git add .
git commit -m "Update: Enhanced AI with 24 species support"
git push
```

## 🔧 Environment Variables

Create a `.env` file in the root directory:

```env
# API Configuration
API_PORT=8002
API_HOST=0.0.0.0

# Database (Optional - for production)
DATABASE_URL=postgresql://user:password@localhost:5432/vetnet

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=http://localhost:5173,https://yourdomain.com

# IoT Configuration
IOT_DEVICE_TIMEOUT=300
MAX_DEVICES=1000
```

## 🏗️ Production Deployment

### Using Docker

1. **Build the image:**
```bash
docker build -t vetnet-ai:latest .
```

2. **Run the container:**
```bash
docker run -d \
  -p 8002:8002 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/data:/app/data \
  --name vetnet-brain \
  vetnet-ai:latest
```

### Using Cloud Platforms

#### AWS EC2
```bash
# Install Docker
sudo yum update -y
sudo yum install docker -y
sudo service docker start

# Clone and deploy
git clone https://github.com/YOUR_USERNAME/vetnet-ai.git
cd vetnet-ai
docker-compose up -d
```

#### Google Cloud Run
```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/vetnet-ai
gcloud run deploy vetnet-ai --image gcr.io/PROJECT_ID/vetnet-ai --platform managed
```

#### Azure Container Instances
```bash
az container create \
  --resource-group vetnet-rg \
  --name vetnet-ai \
  --image YOUR_REGISTRY/vetnet-ai:latest \
  --ports 8002
```

## 🔒 Security Hardening

### Enable HTTPS
```bash
# Using Let's Encrypt with Nginx
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### Firewall Configuration
```bash
# Allow only necessary ports
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 📊 Monitoring

### Health Check Endpoint
```bash
curl http://localhost:8002/health
```

### Docker Logs
```bash
docker-compose logs -f vetnet-brain
```

### System Metrics
The platform automatically logs to `logs/system_metrics.jsonl`

## 🔄 Updates and Maintenance

### Update Models
```bash
python scripts/generate_enhanced_data.py
python src/train_nn.py
python scripts/retrain_models.py
docker-compose restart vetnet-brain
```

### Database Backup (if using PostgreSQL)
```bash
pg_dump vetnet > backup_$(date +%Y%m%d).sql
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8002
netstat -ano | findstr :8002

# Kill the process (Windows)
taskkill /PID <PID> /F

# Kill the process (Linux/Mac)
kill -9 <PID>
```

### Model Not Loading
```bash
# Verify model files exist
ls -la models/

# Retrain if necessary
python src/train_nn.py
```

### IoT Device Connection Issues
1. Check device is on same network
2. Verify API_URL in device firmware
3. Check firewall rules
4. Verify device registration: `GET /iot/dashboard/summary`

## 📈 Scaling

### Horizontal Scaling
```yaml
# docker-compose.yml
services:
  vetnet-brain:
    deploy:
      replicas: 3
    ports:
      - "8002-8004:8002"
```

### Load Balancing
Use Nginx or HAProxy to distribute traffic across multiple instances.

## 🎯 Performance Optimization

### Model Optimization
- Use GPU for inference: Set `DEVICE = 'cuda'` in `inference_nn.py`
- Enable model quantization for faster inference
- Cache predictions for frequently diagnosed animals

### Database Optimization
- Index device_id and timestamp columns
- Use Redis for session storage
- Implement connection pooling

## 📝 Changelog

### v1.0.0 (Current)
- Initial release
- 24 species support
- VetNet Neural Network (95% accuracy)
- IoT device integration
- Real-time telemetry processing
- Device registration system

---

For more information, see [README.md](README.md)
