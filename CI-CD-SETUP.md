# VetNet AI - CI/CD Setup Guide

## 🔐 Required GitHub Secrets

To enable automated Docker builds and deployments, add these secrets to your GitHub repository:

### Navigate to: Settings → Secrets and variables → Actions → New repository secret

1. **DOCKER_USERNAME**
   - Your Docker Hub username
   - Example: `manoj1234`

2. **DOCKER_PASSWORD**
   - Your Docker Hub access token (NOT your password)
   - Generate at: https://hub.docker.com/settings/security
   - Click "New Access Token"
   - Name it "GitHub Actions"
   - Copy the token and paste as secret

## 🚀 How the CI/CD Pipeline Works

### On Every Push to `main`:
1. ✅ **Test Backend** - Validates Python code and AI models
2. ✅ **Test Frontend** - Builds React UI and checks for errors
3. ✅ **Build Docker Image** - Creates production container
4. ✅ **Push to Docker Hub** - Uploads to your Docker registry
5. ✅ **Auto-Deploy** - (Optional) Deploys to your server

### Workflow Files Created:
- `.github/workflows/ci-cd.yml` - Main CI/CD pipeline
- `.github/workflows/docker-build.yml` - Docker-specific builds

## 📦 Docker Hub Setup

### 1. Create Docker Hub Account
Visit: https://hub.docker.com/signup

### 2. Create Repository
```bash
# Login to Docker Hub
docker login

# Tag your image
docker tag vetnet-ai:latest YOUR_USERNAME/vetnet-ai:latest

# Push manually (first time)
docker push YOUR_USERNAME/vetnet-ai:latest
```

### 3. Verify Auto-Build
After setting up secrets, push to GitHub:
```bash
git push origin main
```

Check the "Actions" tab on GitHub to see the pipeline running.

## 🔄 Automated Deployment Options

### Option 1: Deploy to Cloud VM (AWS/GCP/Azure)

Add this to your CI/CD workflow:
```yaml
- name: Deploy to Production Server
  uses: appleboy/ssh-action@master
  with:
    host: ${{ secrets.SERVER_HOST }}
    username: ${{ secrets.SERVER_USER }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    script: |
      cd /opt/vetnet-ai
      docker-compose pull
      docker-compose up -d
```

Required secrets:
- `SERVER_HOST` - Your server IP
- `SERVER_USER` - SSH username
- `SSH_PRIVATE_KEY` - Your private SSH key

### Option 2: Deploy to Kubernetes

```yaml
- name: Deploy to Kubernetes
  run: |
    kubectl set image deployment/vetnet-ai \
      vetnet-ai=${{ secrets.DOCKER_USERNAME }}/vetnet-ai:${{ github.sha }}
```

### Option 3: Deploy to Heroku

```yaml
- name: Deploy to Heroku
  uses: akhileshns/heroku-deploy@v3.12.12
  with:
    heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
    heroku_app_name: "vetnet-ai-prod"
    heroku_email: "your-email@example.com"
```

## 🧪 Testing the Pipeline

### Manual Trigger
You can manually run workflows from the GitHub Actions tab.

### Test Deployment
```bash
# Make a small change
echo "# Test" >> README.md

# Commit and push
git add .
git commit -m "Test CI/CD pipeline"
git push origin main

# Watch the pipeline
# Go to: https://github.com/YOUR_USERNAME/animal-health-predictor/actions
```

## 📊 Pipeline Status Badge

Add this to your README.md:
```markdown
![CI/CD](https://github.com/manoj1234-ms/animal-health-predictor/workflows/VetNet%20AI%20CI/CD%20Pipeline/badge.svg)
```

## 🐛 Troubleshooting

### Pipeline Fails on Model Training
- Increase GitHub Actions timeout
- Pre-train models and commit them to repo
- Skip training in CI, only validate

### Docker Build Fails
- Check Dockerfile syntax
- Verify all dependencies are listed
- Check Docker Hub credentials

### Deployment Fails
- Verify server SSH access
- Check firewall rules
- Ensure Docker is installed on target server

## 🔒 Security Best Practices

1. **Never commit secrets** - Use GitHub Secrets
2. **Use access tokens** - Not passwords
3. **Rotate credentials** - Every 90 days
4. **Limit permissions** - Minimal required access
5. **Enable 2FA** - On GitHub and Docker Hub

## 📈 Advanced Features

### Multi-Environment Deployment
```yaml
deploy-staging:
  if: github.ref == 'refs/heads/develop'
  # Deploy to staging

deploy-production:
  if: github.ref == 'refs/heads/main'
  # Deploy to production
```

### Slack Notifications
```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Automated Testing
```yaml
- name: Run Integration Tests
  run: |
    docker-compose up -d
    pytest tests/integration/
    docker-compose down
```

---

For more information, see [DEPLOYMENT.md](DEPLOYMENT.md)
