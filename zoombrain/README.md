# ZoomBrain - AI Meeting Summarization Platform

An intelligent meeting summarization platform powered by AI that processes Zoom and Microsoft Teams transcripts with context-aware analysis, sentiment tracking, and automated task extraction.

## 🎯 Features

### Core Functionality
- 📄 **Meeting Transcript Processing**: Supports VTT and TXT transcript formats
- 🤖 **AI-Powered Summarization**: Generate bullet-point, narrative, or executive summaries
- � **Participant Management**: Track participants with roles and contact information
- 📊 **Sentiment Analysis**: Real-time sentiment tracking for each participant
- ✅ **Task Extraction**: Automatically identify and assign action items
- 📧 **Email Notifications**: Automated sentiment alerts and meeting summaries
- � **Engagement Analytics**: Visual heatmaps showing engagement over time
- 📅 **Date Detection**: Identify mentioned dates for calendar integration
- 📑 **Document Indexing**: Upload reference documents (PDF, PPTX, TXT) for context

### Advanced Features
- **Topic Segmentation**: Break meetings into logical topics
- **Speaker Intent Detection**: Understand participant contributions
- **Customizable Summaries**: Choose style and detail level
- **Visual Analytics**: Charts and graphs for sentiment and engagement
- **Integration Ready**: Placeholder support for Google Calendar, Slack, Teams

## 🏗️ Project Structure

```
devkada-project/
├── zoombrain/                    # Backend (Python/FastAPI)
│   ├── app/
│   │   ├── main.py              # FastAPI application & endpoints
│   │   ├── schemas.py           # Pydantic models
│   │   ├── meeting_processor.py # Transcript parsing & analysis
│   │   ├── sentiment_analyzer.py# Sentiment analysis engine
│   │   ├── llm_summarizer.py    # LLM-based summarization
│   │   ├── integrations.py      # Email, Calendar, Slack integrations
│   │   ├── summarizer.py        # Document indexing (FAISS)
│   │   ├── utils_parsers.py     # File parsing utilities
│   │   └── data/
│   │       ├── uploads/         # Uploaded transcripts
│   │       └── indexes/         # FAISS vector indexes
│   ├── requirements.txt
│   ├── .env.template
│   └── README.md
├── frontend/                     # Frontend (React)
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js               # Main React component
│   │   ├── index.js
│   │   ├── index.css
│   │   ├── services/
│   │   │   └── api.js           # API service layer
│   │   └── pages/
│   │       ├── HomePage.js
│   │       ├── UploadPage.js
│   │       ├── MeetingDetailPage.js
│   │       ├── ParticipantsPage.js
│   │       └── DocumentsPage.js
│   └── package.json
└── Instructions.txt
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. **Navigate to the backend directory**
   ```powershell
   cd zoombrain
   ```

2. **Create a virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```powershell
   cp .env.template .env
   ```
   
   Edit `.env` and add your credentials:
   - Email settings (for Gmail, use app-specific password)
   - OpenAI API key (optional, for better summaries)
   - Google Calendar credentials (optional)

5. **Start the backend server**
   ```powershell
   cd app
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`
   - Swagger docs: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

1. **Navigate to the frontend directory**
   ```powershell
   cd ..\frontend
   ```

2. **Install Node.js dependencies**
   ```powershell
   npm install
   ```

3. **Start the development server**
   ```powershell
   npm start
   ```
   
   The app will open at `http://localhost:3000`

## 📖 Usage Guide

### 1. Upload Meeting Transcript

1. Go to **Upload Meeting** page
2. Choose your transcript file (VTT or TXT)
3. Enter meeting details:
   - Meeting title
   - Date (optional)
   - Summary style (bullet points, narrative, executive)
   - Detail level (brief, medium, detailed)
4. Click **Process Meeting**

### 2. View Meeting Summary

After processing, you'll see:
- AI-generated summary
- List of participants with engagement metrics
- Extracted action items with assignments
- Sentiment analysis charts
- Engagement heatmap over time
- Detected dates from discussion

### 3. Manage Participants

1. Go to **Participants** page
2. Click **Add Participant**
3. Enter:
   - Name
   - Role/Position
   - Email (for notifications)
   - Team
4. Participants will be automatically recognized in future meetings

### 4. Upload Reference Documents

1. Go to **Documents** page
2. Upload PDFs, PowerPoint, or text files
3. Documents are indexed for context-aware summaries
4. Use search to find relevant content

### 5. Email Notifications

The system automatically sends emails when:
- **Positive sentiment (≥80)**: Congratulatory message
- **Negative sentiment (≤-80)**: Check-in message
- **Manual summary**: Click "Send Summary via Email" on meeting detail page

## 🔧 API Endpoints

### Meeting Endpoints

```
POST   /api/meetings/upload                  # Upload and process transcript
GET    /api/meetings                         # List all meetings
GET    /api/meetings/{meeting_id}            # Get meeting details
POST   /api/meetings/{meeting_id}/update-participants
POST   /api/meetings/{meeting_id}/send-summary
```

### Participant Endpoints

```
POST   /api/participants/add                 # Add participant
GET    /api/participants                     # List all participants
```

### Document Endpoints

```
POST   /api/documents/upload                 # Upload reference document
GET    /api/documents                        # List all documents
POST   /api/documents/search                 # Search documents
```

## 📝 Transcript Format

### VTT Format (WebVTT)
```
WEBVTT

00:00:10.000 --> 00:00:15.000
John Doe: Welcome everyone to today's meeting.

00:00:15.000 --> 00:00:20.000
Jane Smith: Thanks John, excited to discuss the project.
```

### TXT Format
```
John Doe: Welcome everyone to today's meeting.
Jane Smith: Thanks John, excited to discuss the project.
Moderator: Let's start with the first agenda item.
```

## 🎨 Customization Options

### Summary Styles
- **Bullet Points**: Concise list of key points
- **Narrative**: Flowing paragraph-style summary
- **Executive**: High-level overview with decisions

### Detail Levels
- **Brief**: 3-5 key sentences
- **Medium**: Balanced summary with context
- **Detailed**: Comprehensive with all important points

## 🔌 Integration Setup (Optional)

### Email (Gmail)
1. Enable 2-factor authentication on Gmail
2. Generate app-specific password
3. Add to `.env`:
   ```
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=your-app-password
   ```

### OpenAI (Better Summaries)
1. Get API key from https://platform.openai.com
2. Add to `.env`:
   ```
   OPENAI_API_KEY=sk-...
   ```

### Google Calendar
1. Set up Google Cloud project
2. Enable Calendar API
3. Download credentials JSON
4. Add path to `.env`:
   ```
   GOOGLE_CREDENTIALS_PATH=path/to/credentials.json
   ```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **FAISS**: Vector similarity search
- **Sentence Transformers**: Text embeddings
- **PyPDF2**: PDF parsing
- **python-pptx**: PowerPoint parsing
- **Pydantic**: Data validation

### Frontend
- **React**: UI framework
- **Material-UI**: Component library
- **Recharts**: Data visualization
- **Axios**: HTTP client
- **React Router**: Navigation

## 🔒 Security Notes

- Never commit `.env` file with real credentials
- Use app-specific passwords for email
- Store API keys securely
- Configure CORS for production deployments
- Use HTTPS in production

## 🐛 Troubleshooting

### Backend Issues

**Import errors**: Make sure virtual environment is activated
```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

**Email not sending**: Check SMTP settings and app password

**Port already in use**: Change port in `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Frontend Issues

**Cannot connect to API**: Check backend is running on port 8000

**Node modules error**: Delete `node_modules` and reinstall:
```powershell
rm -r node_modules
npm install
```

## 📈 Roadmap

- [x] Basic transcript processing
- [x] Sentiment analysis
- [x] Task extraction
- [x] Email notifications
- [x] React frontend
- [ ] Google Calendar integration (full implementation)
- [ ] Slack/Teams webhooks
- [ ] Real-time processing
- [ ] Multi-language support
- [ ] Custom LLM models
- [ ] Docker deployment
- [ ] User authentication
- [ ] Database persistence

## 📄 License

MIT License - feel free to use and modify for your needs.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📞 Support

For questions or issues, please open a GitHub issue or contact the development team.

---

**Note**: This is a development version. For production use, implement proper authentication, database storage, and security measures.
