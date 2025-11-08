# 🧠 ZoomBrain - AI Meeting Summarization Platform

> Transform meeting transcripts into actionable insights with AI-powered summarization, sentiment analysis, and automated task extraction.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18.2-blue.svg)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 What is ZoomBrain?

ZoomBrain is a full-stack application that automatically processes meeting transcripts from Zoom, Microsoft Teams, or any text-based source. It provides:

- 🤖 **AI Summarization** - Generate executive summaries with customizable styles
- 😊 **Sentiment Analysis** - Track participant mood and engagement in real-time
- ✅ **Task Extraction** - Automatically identify and assign action items
- 📧 **Smart Notifications** - Email alerts for sentiment changes and summaries
- 📊 **Visual Analytics** - Interactive charts showing engagement and sentiment trends
- 👥 **Participant Tracking** - Manage team members with roles and contact info

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm

### Installation

**1. Clone & Setup Backend**
```powershell
git clone <your-repo-url>
cd devkada-project/zoombrain
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cp .env.template .env
```

**2. Setup Frontend**
```powershell
cd ..\frontend
npm install
```

**3. Start Application**

Terminal 1 (Backend):
```powershell
cd zoombrain\app
python main.py
```

Terminal 2 (Frontend):
```powershell
cd frontend
npm start
```

**4. Access Application**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

### Try it Now!
Upload the sample file at `sample_data/sample_meeting.vtt` to see it in action!

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [📘 Complete README](zoombrain/README.md) | Full documentation with API details |
| [⚡ Quick Start Guide](QUICKSTART.md) | Get running in 5 minutes |
| [🏗️ Architecture](ARCHITECTURE.md) | System design and data flow |
| [💻 Development Notes](DEVELOPMENT_NOTES.md) | Technical implementation details |
| [📋 Project Summary](PROJECT_SUMMARY.md) | Feature overview and roadmap |
| [✅ Installation Checklist](INSTALLATION_CHECKLIST.md) | Step-by-step verification |

## ✨ Key Features

### Meeting Processing
- ✅ Support for VTT and TXT transcript formats
- ✅ Automatic speaker identification
- ✅ Topic segmentation
- ✅ Timeline-based engagement tracking

### AI Analysis
- ✅ Multi-style summarization (bullets, narrative, executive)
- ✅ Sentiment scoring (-100 to +100)
- ✅ Action item detection with regex patterns
- ✅ Date extraction for calendar integration
- ✅ Participant engagement metrics

### Integrations
- ✅ Email notifications (SMTP/Gmail)
- ✅ Document indexing (PDF, PPTX, TXT)
- ✅ FAISS vector search
- ⚠️ Google Calendar (placeholder)
- ⚠️ Slack/Teams webhooks (placeholder)

### User Interface
- ✅ Modern Material-UI design
- ✅ Responsive charts (Recharts)
- ✅ Real-time form validation
- ✅ Drag-and-drop file upload
- ✅ Mobile-responsive layout

## 📊 Screenshots

### Dashboard
```
┌─────────────────────────────────────────────────────────┐
│  ZoomBrain - AI Meeting Summarizer              [Menu]  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  📤 Upload Meeting    👥 Participants    📄 Documents   │
│                                                          │
│  Recent Meetings                                        │
│  ┌──────────────────────┐  ┌──────────────────────┐   │
│  │ Team Standup         │  │ Q1 Planning          │   │
│  │ Nov 8, 2025          │  │ Nov 7, 2025          │   │
│  │ 3 participants       │  │ 5 participants       │   │
│  └──────────────────────┘  └──────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Meeting Analysis
```
┌─────────────────────────────────────────────────────────┐
│  Team Standup - November 8, 2025    [Send Email]       │
├─────────────────────────────────────────────────────────┤
│  Summary                                                │
│  • Completed authentication feature                     │
│  • Code review scheduled for Friday                     │
│  • Performance issues need attention                    │
│                                                          │
│  Sentiment Analysis                     Engagement      │
│  ┌────────────────┐                    ┌─────────────┐ │
│  │ 😊 John: +45   │                    │    ╱╲       │ │
│  │ 😊 Sarah: +62  │                    │   ╱  ╲      │ │
│  │ 😐 Mike: -12   │                    │  ╱    ╲     │ │
│  └────────────────┘                    └─────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

**Backend**
- FastAPI (Python web framework)
- FAISS (Vector similarity search)
- Sentence Transformers (Embeddings)
- PyPDF2 & python-pptx (Document parsing)
- Pydantic (Data validation)

**Frontend**
- React 18 (UI framework)
- Material-UI (Component library)
- Recharts (Data visualization)
- Axios (HTTP client)
- React Router (Navigation)

## 📁 Project Structure

```
devkada-project/
├── zoombrain/              # Backend (FastAPI)
│   ├── app/
│   │   ├── main.py        # API endpoints
│   │   ├── meeting_processor.py
│   │   ├── sentiment_analyzer.py
│   │   ├── llm_summarizer.py
│   │   └── integrations.py
│   └── requirements.txt
├── frontend/              # Frontend (React)
│   ├── src/
│   │   ├── pages/        # React pages
│   │   └── services/     # API client
│   └── package.json
├── sample_data/          # Example transcripts
└── docs/                 # Documentation
```

## 🔧 Configuration

### Email Setup (Optional)
For Gmail, generate an app-specific password:
1. Enable 2-factor authentication
2. Go to Google Account → Security → App passwords
3. Generate password for "Mail"
4. Add to `.env`:
```env
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
```

### OpenAI Integration (Optional)
For better AI summaries:
```env
OPENAI_API_KEY=sk-your-api-key
```

## 📝 Usage Examples

### Upload Meeting via API
```python
import requests

files = {'file': open('meeting.vtt', 'rb')}
data = {
    'meeting_title': 'Team Standup',
    'summary_style': 'bullet_points',
    'detail_level': 'medium'
}

response = requests.post(
    'http://localhost:8000/api/meetings/upload',
    files=files,
    data=data
)
```

### Add Participant
```python
participant = {
    'name': 'John Doe',
    'role': 'Product Manager',
    'email': 'john@example.com'
}

requests.post(
    'http://localhost:8000/api/participants/add',
    json=participant
)
```

## 🧪 Testing

### Run Backend Tests
```powershell
cd zoombrain
pytest tests/
```

### Test Sample Meeting
1. Navigate to http://localhost:3000/upload
2. Upload `sample_data/sample_meeting.vtt`
3. View generated summary and analytics

## 🚀 Deployment

### Option 1: Cloud Platform (Recommended)
- **Backend**: Deploy to Render, Railway, or Heroku
- **Frontend**: Deploy to Vercel or Netlify
- **Database**: Use Supabase or PlanetScale (when adding DB)

### Option 2: Docker
```powershell
docker-compose up
```

### Option 3: Traditional Server
See [DEVELOPMENT_NOTES.md](DEVELOPMENT_NOTES.md) for detailed deployment guide.

## 🔒 Security Notes

**Development Mode** ⚠️
- No authentication
- CORS allows all origins
- Data stored in memory

**Production Requirements** ✅
- Add JWT authentication
- Implement RBAC
- Use PostgreSQL/MongoDB
- Enable HTTPS
- Add rate limiting
- Restrict CORS

## 🗺️ Roadmap

### ✅ Phase 1: MVP (Complete)
- [x] Transcript processing
- [x] Sentiment analysis
- [x] Task extraction
- [x] Email notifications
- [x] React frontend

### 🚧 Phase 2: Production
- [ ] Database integration
- [ ] User authentication
- [ ] Docker deployment
- [ ] Unit tests
- [ ] CI/CD pipeline

### 🔮 Phase 3: Advanced
- [ ] Real-time processing
- [ ] Multi-language support
- [ ] Calendar sync
- [ ] Slack/Teams bots
- [ ] Custom ML models

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://reactjs.org/) - UI library
- [Material-UI](https://mui.com/) - Component library
- [FAISS](https://github.com/facebookresearch/faiss) - Similarity search
- [Recharts](https://recharts.org/) - Charting library

## 📞 Support

- 📖 [Documentation](zoombrain/README.md)
- 🐛 [Issue Tracker](https://github.com/your-repo/issues)
- 💬 [Discussions](https://github.com/your-repo/discussions)

## ⭐ Star History

If you find ZoomBrain useful, please consider giving it a star! ⭐

---

**Made with ❤️ for better meetings**

