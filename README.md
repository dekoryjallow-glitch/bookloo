# 📚 Storybook.ai

> AI-powered personalized children's book generator. Upload a photo, pick a theme, and get a 20-page storybook PDF.

## 🏗️ Architecture

```
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── engines/            # Modular AI Engines
│   │   │   ├── story_engine.py   # OpenAI GPT-4 (Hero's Journey)
│   │   │   ├── image_engine.py   # Replicate Flux Model
│   │   │   └── layout_engine.py  # ReportLab PDF Generator
│   │   ├── api/routes/         # REST API Endpoints
│   │   ├── models/             # Pydantic Models
│   │   └── services/           # Firebase Integration
│   └── Dockerfile
│
├── frontend/                   # Next.js Frontend
│   ├── src/
│   │   ├── app/               # App Router Pages
│   │   ├── components/        # React Components
│   │   └── lib/               # API Client & Firebase
│   └── Dockerfile
│
└── docker-compose.yml          # Local Development
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Firebase Project with Firestore & Storage
- API Keys: OpenAI, Replicate

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run development server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp env.example .env.local
# Edit .env.local with your Firebase config

# Run development server
npm run dev
```

### Docker (Recommended)

```bash
# Set environment variables
export OPENAI_API_KEY=sk-...
export REPLICATE_API_TOKEN=r8_...
export FIREBASE_PROJECT_ID=your-project
export FIREBASE_STORAGE_BUCKET=your-project.appspot.com

# Run both services
docker compose up --build
```

## 📖 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/books/create` | Create new book |
| GET | `/api/books/{id}/status` | Get generation status |
| GET | `/api/books/{id}` | Get full book details |
| GET | `/api/books/{id}/download` | Get PDF download URL |

## 🎨 Tech Stack

- **Backend**: FastAPI, Python 3.11
- **Frontend**: Next.js 14, React, Tailwind CSS
- **Database**: Firebase Firestore
- **Storage**: Firebase Cloud Storage
- **AI**: OpenAI GPT-4, Replicate Flux
- **PDF**: ReportLab
- **Deployment**: Google Cloud Run

## 📄 License

MIT
