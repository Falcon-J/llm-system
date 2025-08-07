# 🚀 Deployment Guide

## Railway Deployment (Recommended)

### 1. Prepare Repository

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: HackRx LLM system"

# Push to GitHub
git remote add origin https://github.com/yourusername/hackrx-llm-system.git
git branch -M main
git push -u origin main
```

### 2. Deploy to Railway

1. **Visit [Railway.app](https://railway.app)**
2. **Connect GitHub** account
3. **Create New Project** → "Deploy from GitHub repo"
4. **Select** your repository
5. **Add Environment Variable:**
   - Name: `OPENAI_API_KEY`
   - Value: `sk-or-v1-your-openrouter-key`
6. **Deploy** automatically

### 3. Get Your API URL

Railway will provide a URL like:

```
https://hackrx-llm-system-production.up.railway.app
```

### 4. Test Deployment

```bash
# Set your Railway URL
export TEST_BASE_URL=https://your-app.railway.app

# Run production tests
python test_production.py
```

## Alternative: Docker Deployment

### 1. Build Container

```bash
# Build image
docker build -t hackrx-llm-system .

# Run container
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-or-v1-your-key hackrx-llm-system
```

### 2. Docker Compose

```bash
# Copy environment file
cp .env.example .env
# Edit .env with your API key

# Start with Docker Compose
docker-compose up -d
```

## Alternative: Manual Server Deployment

### 1. Server Setup

```bash
# Install Python 3.11+
sudo apt update
sudo apt install python3.11 python3.11-pip

# Clone repository
git clone https://github.com/yourusername/hackrx-llm-system.git
cd hackrx-llm-system

# Install dependencies
pip3 install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit with your API key
nano .env
```

### 3. Run with Gunicorn

```bash
# Install Gunicorn
pip3 install gunicorn

# Run production server
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 4. Process Manager (PM2)

```bash
# Install PM2
npm install -g pm2

# Create ecosystem file
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'hackrx-api',
    script: 'gunicorn',
    args: 'main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000',
    env: {
      OPENAI_API_KEY: 'sk-or-v1-your-key'
    }
  }]
}
EOF

# Start with PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## Environment Variables

### Required

| Variable         | Description        | Example              |
| ---------------- | ------------------ | -------------------- |
| `OPENAI_API_KEY` | OpenRouter API key | `sk-or-v1-abc123...` |

### Optional

| Variable      | Description      | Default              |
| ------------- | ---------------- | -------------------- |
| `PORT`        | Server port      | `8000`               |
| `ENVIRONMENT` | Environment mode | `production`         |
| `LLM_MODEL`   | Model to use     | `openai/gpt-4o-mini` |

## Health Checks

After deployment, verify these endpoints:

```bash
# Health check
curl https://your-app.railway.app/health

# Root endpoint
curl https://your-app.railway.app/

# Competition endpoint test
curl -X POST "https://your-app.railway.app/hackrx/run" \
  -H "Authorization: Bearer hackrx-api-token-2024" \
  -H "Content-Type: application/json" \
  -d '{"documents":"test","questions":["test"]}'
```

## Monitoring

### Railway Dashboard

- Monitor logs in Railway dashboard
- Check resource usage
- View deployment history

### Custom Monitoring

```bash
# Check logs
curl https://your-app.railway.app/health

# Monitor response times
python test_production.py
```

## Troubleshooting

### Common Issues

1. **503 Service Unavailable**

   - Check OPENAI_API_KEY is set
   - Verify Railway app is running

2. **Timeout Errors**

   - Document processing takes 30-60 seconds
   - Increase timeout in client requests

3. **401 Authentication Error**
   - Verify exact token: `hackrx-api-token-2024`
   - Check Authorization header format

### Debug Commands

```bash
# Check environment
curl https://your-app.railway.app/health

# Test with minimal request
curl -X POST "https://your-app.railway.app/hackrx/run" \
  -H "Authorization: Bearer hackrx-api-token-2024" \
  -H "Content-Type: application/json" \
  -d '{"documents":"test","questions":["What is this?"]}'
```

## Support

For deployment issues:

1. Check Railway logs in dashboard
2. Verify environment variables
3. Test with `test_production.py`
4. Ensure OpenRouter API key has credits

## 🎯 Ready for Competition!

Once deployed, your API will be available at:

```
https://your-app.railway.app/hackrx/run
```

This endpoint is ready for HackRx competition evaluation!
