---
description: Deploy the Storybook.ai application to production on bookloo.xyz
---

# 🚀 Deployment Workflow for bookloo.xyz

Follow these steps to deploy the application to your VPS.

## 1. Server Preparation
Ensure your VPS (Ubuntu 22.04+ recommended) has Docker and Docker Compose installed.

```bash
# Update and install Docker
sudo apt update && sudo apt install -y docker.io docker-compose
```

## 2. Setup Files
Upload the project files to your server (or clone via git).
Ensure you have the following files in the root:
- `docker-compose.prod.yml`
- `Caddyfile`
- `.env` (Production version)
- `backend/service-account.json` (Firebase credentials)

## 3. Environment Configuration
Edit your `.env` file with production values:
```env
OPENAI_API_KEY=your_key
REPLICATE_API_TOKEN=your_token
GEMINI_API_KEY=your_key
FIREBASE_PROJECT_ID=storybookai-3d5fa
FIREBASE_STORAGE_BUCKET=storybookai-3d5fa.firebasestorage.app
STRIPE_SECRET_KEY=your_key
STRIPE_PRICE_ID=price_1SfrAfIzRdpbFdRdve2fq2vK
NEXT_PUBLIC_API_URL=https://bookloo.xyz
```

## 4. Launch Application
Run the following command to build and start all services:

// turbo
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## 5. Domain Setup
Point your DNS A-Record for `bookloo.xyz` to your VPS IP address.
Caddy will automatically handle the SSL certificates (Let's Encrypt).

## 6. Verification
Once started, visit:
- `https://bookloo.xyz` (Frontend)
- `https://bookloo.xyz/api/health` (Backend status)
