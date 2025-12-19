# Deployment to Google Cloud Run for bookloo.xyz

Dieses Projekt besteht aus zwei Services: dem **Backend (FastAPI)** und dem **Frontend (Next.js)**. Da Cloud Run keine Docker-Compose Dateien nativ unterstützt, deployen wir beide separat.

## 1. Vorbereitung (Google Cloud Console)
1. Erstelle ein neues Projekt in GCP (z.B. `bookloo-prod`).
2. Aktiviere die APIs: `Cloud Run`, `Artifact Registry`, `Secret Manager`.
3. Installiere die [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) auf deinem Rechner.

## 2. Secrets im Secret Manager anlegen (Empfohlen)
Anstatt API-Keys in Dateien zu speichern, lege sie sicher in GCP an:
- `STRIPE_SECRET_KEY`
- `OPENAI_API_KEY`
- `REPLICATE_API_TOKEN`
- `GEMINI_API_KEY`
- `FIREBASE_SERVICE_ACCOUNT` (Inhalt der .json Datei)

## 3. Backend Deployment
Gehe in den `/backend` Ordner und führe aus:

```bash
# Projekt ID setzen
export PROJECT_ID=dein-projekt-id

# Image bauen und hochladen (Google Cloud Build)
gcloud builds submit --tag gcr.io/$PROJECT_ID/bookloo-backend

# Deploy auf Cloud Run
gcloud run deploy bookloo-backend \
  --image gcr.io/$PROJECT_ID/bookloo-backend \
  --platform managed \
  --region europe-west3 \
  --allow-unauthenticated \
  --set-env-vars="APP_ENV=production,STRIPE_PRICE_ID=price_1SfuBHIaw7jNzdMRXKloVszf,FRONTEND_URL=https://bookloo.xyz" \
  --update-secrets="STRIPE_SECRET_KEY=STRIPE_SECRET_KEY:latest,OPENAI_API_KEY=OPENAI_API_KEY:latest,REPLICATE_API_TOKEN=REPLICATE_API_TOKEN:latest,GEMINI_API_KEY=GEMINI_API_KEY:latest"
```

## 4. Frontend Deployment
Gehe in den `/frontend` Ordner. 
**Wichtig:** Das Frontend muss wissen, wo das Backend liegt.

```bash
# Image bauen
gcloud builds submit --tag gcr.io/$PROJECT_ID/bookloo-frontend

# Deploy auf Cloud Run
gcloud run deploy bookloo-frontend \
  --image gcr.io/$PROJECT_ID/bookloo-frontend \
  --platform managed \
  --region europe-west3 \
  --allow-unauthenticated \
  --set-env-vars="NEXT_PUBLIC_API_URL=https://bookloo.xyz"
```

## 5. Domain Mapping (bookloo.xyz)
Da du zwei Services hast, aber nur eine Domain, gibt es zwei Wege:

### Weg A: Firebase Hosting Proxy (Einfachster Weg für Next.js + FastAPI)
1. Initialisiere Firebase Hosting im Root: `firebase init hosting`.
2. Konfiguriere `firebase.json` so, dass `/api/*` zum Backend Service und alles andere zum Frontend Service geroutet wird:

```json
{
  "hosting": {
    "public": "public",
    "rewrites": [
      { "source": "/api/**", "run": { "serviceId": "bookloo-backend", "region": "europe-west3" } },
      { "source": "**", "run": { "serviceId": "bookloo-frontend", "region": "europe-west3" } }
    ]
  }
}
```
3. Verbinde deine Domain `bookloo.xyz` in der Firebase Console.

### Weg B: Cloud Load Balancer (Professionell & Teurer)
Erstelle einen HTTPS Load Balancer in GCP und erstelle Pfad-Regeln für `/api/*` (Backend) und default (Frontend).

## 6. Stripe Live Test
Vergiss nicht, den Webhook in Stripe auf die neue URL zu aktualisieren: `https://bookloo.xyz/api/webhook/stripe`.
