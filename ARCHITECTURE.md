# ZoomBrain - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                          │
│                     (React Frontend - Port 3000)                 │
├─────────────────────────────────────────────────────────────────┤
│  HomePage  │  UploadPage  │  MeetingDetail  │  Participants     │
│            │              │                 │  Documents        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND (Port 8000)                  │
├─────────────────────────────────────────────────────────────────┤
│                        API Endpoints                             │
│  /api/meetings/upload  │  /api/participants  │  /api/documents  │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│  PROCESSING MODULES      │  │  INTEGRATION SERVICES     │
├──────────────────────────┤  ├──────────────────────────┤
│ • Meeting Processor      │  │ • Email Service (SMTP)   │
│ • Sentiment Analyzer     │  │ • Google Calendar API    │
│ • LLM Summarizer         │  │ • Slack Integration      │
│ • Document Parser        │  │ • Teams Integration      │
│ • FAISS Indexer          │  │                          │
└──────────────────────────┘  └──────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DATA STORAGE                             │
├─────────────────────────────────────────────────────────────────┤
│ • In-Memory Store (meetings_db, participants_db)                │
│ • File Storage (uploads/, indexes/)                             │
│ • FAISS Vector Index                                            │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
1. UPLOAD TRANSCRIPT
   ┌──────────┐
   │  User    │
   └────┬─────┘
        │ Upload VTT/TXT
        ▼
   ┌──────────────────┐
   │  Frontend Form   │
   └────┬─────────────┘
        │ POST /api/meetings/upload
        ▼
   ┌──────────────────┐
   │  FastAPI Router  │
   └────┬─────────────┘
        │
        ▼
   ┌──────────────────────────────┐
   │  Meeting Processor           │
   │  • Parse VTT/TXT             │
   │  • Extract Participants      │
   │  • Detect Action Items       │
   │  • Find Dates                │
   └────┬─────────────────────────┘
        │
        ▼
   ┌──────────────────────────────┐
   │  Sentiment Analyzer          │
   │  • Analyze per participant   │
   │  • Generate heatmap          │
   │  • Calculate engagement      │
   └────┬─────────────────────────┘
        │
        ▼
   ┌──────────────────────────────┐
   │  LLM Summarizer              │
   │  • OpenAI API (if available) │
   │  • Extractive fallback       │
   │  • Apply style/detail        │
   └────┬─────────────────────────┘
        │
        ▼
   ┌──────────────────────────────┐
   │  Store Results               │
   │  • Save to meetings_db       │
   │  • Return meeting_id         │
   └────┬─────────────────────────┘
        │
        ▼
   ┌──────────────────────────────┐
   │  Email Service               │
   │  • Check sentiment ≥80/-80   │
   │  • Send notifications        │
   └────┬─────────────────────────┘
        │
        ▼
   ┌──────────────────┐
   │  Return Response │
   │  (JSON)          │
   └────┬─────────────┘
        │
        ▼
   ┌──────────────────┐
   │  Display Summary │
   │  (React UI)      │
   └──────────────────┘
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────────┐
│                     MEETING PROCESSOR                            │
│                                                                  │
│  parse_vtt(content)        ─→  List[Dict] segments             │
│  parse_txt_transcript()    ─→  List[Dict] segments             │
│  extract_participants()    ─→  Dict[name, stats]               │
│  detect_action_items()     ─→  List[Dict] tasks                │
│  detect_dates()            ─→  List[str] dates                 │
│  segment_by_topics()       ─→  Dict[topic, segments]           │
│  assign_tasks_to_participants() ─→ List[Dict] assigned_tasks   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   SENTIMENT ANALYZER                             │
│                                                                  │
│  analyze_text(text)                ─→  Dict{score, class}      │
│  analyze_participant_sentiment()   ─→  Dict[name, sentiment]   │
│  calculate_engagement_heatmap()    ─→  List[Dict] heatmap      │
│  identify_sentiment_triggers()     ─→  Dict{pos, neg}          │
│  should_send_notification()        ─→  Tuple[bool, type]       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     LLM SUMMARIZER                               │
│                                                                  │
│  summarize_transcript()            ─→  str summary             │
│  generate_action_items_summary()   ─→  str formatted           │
│  generate_participant_summary()    ─→  str formatted           │
│  generate_sentiment_summary()      ─→  str formatted           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    INTEGRATIONS                                  │
│                                                                  │
│  EmailService                                                   │
│    • send_sentiment_notification()                              │
│    • send_meeting_summary()                                     │
│                                                                  │
│  GoogleCalendarService                                          │
│    • create_event()                                             │
│    • parse_date_from_text()                                     │
│                                                                  │
│  SlackIntegration (placeholder)                                 │
│  TeamsIntegration (placeholder)                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Database Schema (In-Memory)

```python
# meetings_db structure
{
  "meeting_id": {
    "meeting_id": str,
    "title": str,
    "date": str (ISO 8601),
    "file_path": str,
    "segments": List[Dict],
    "participants": Dict[str, Dict],
    "participant_sentiments": Dict[str, Dict],
    "action_items": List[Dict],
    "summary": str,
    "detected_dates": List[str],
    "engagement_heatmap": List[Dict],
    "summary_style": str,
    "detail_level": str
  }
}

# participants_db structure
{
  "participant_name": {
    "name": str,
    "role": str,
    "email": str,
    "team": str
  }
}

# document_summarizer.metadata
[
  {
    "id": str (uuid),
    "filename": str,
    "file_type": str,
    "upload_date": str (ISO 8601),
    "chunk_id": int,
    "text_preview": str
  }
]
```

## Frontend State Management

```
App.js (Router)
│
├── HomePage
│   ├── State: meetings[], loading, error
│   └── API: listMeetings()
│
├── UploadPage
│   ├── State: file, formData, loading, error
│   └── API: uploadMeeting(formData)
│
├── MeetingDetailPage
│   ├── State: meeting, loading, error, emailStatus
│   └── API: getMeeting(id), sendMeetingSummary(id)
│
├── ParticipantsPage
│   ├── State: participants[], formData, dialogOpen
│   └── API: listParticipants(), addParticipant()
│
└── DocumentsPage
    ├── State: documents[], searchResults, loading
    └── API: listDocuments(), uploadDocument(), searchDocuments()
```

## API Request/Response Examples

### Upload Meeting
```http
POST /api/meetings/upload
Content-Type: multipart/form-data

file: [binary data]
meeting_title: "Team Standup"
meeting_date: "2025-11-08"
summary_style: "bullet_points"
detail_level: "medium"

Response (200):
{
  "meeting_id": "uuid",
  "title": "Team Standup",
  "summary": "• Completed authentication feature\n• Code review by Friday...",
  "participants": {
    "John Smith": {
      "speaking_count": 5,
      "total_words": 120,
      ...
    }
  },
  "participant_sentiments": {...},
  "action_items": [...],
  "engagement_heatmap": [...]
}
```

### Get Meeting
```http
GET /api/meetings/{meeting_id}

Response (200):
{
  "meeting_id": "uuid",
  "title": "Team Standup",
  "date": "2025-11-08T10:00:00",
  "summary": "...",
  "participants": {...},
  "action_items": [...],
  "sentiment_data": {...},
  "engagement_heatmap": [...]
}
```

## Technology Dependencies

### Backend Dependencies
```
fastapi==0.104.1           → Web framework
uvicorn==0.24.0            → ASGI server
pydantic==2.5.0            → Data validation
faiss-cpu==1.7.4           → Vector search
numpy==1.24.3              → Numerical computing
sentence-transformers      → Text embeddings
PyPDF2==3.0.1             → PDF parsing
python-pptx==0.6.23       → PowerPoint parsing
email-validator            → Email validation
python-dotenv              → Environment variables
requests==2.31.0           → HTTP client
```

### Frontend Dependencies
```
react@18.2.0               → UI framework
react-dom@18.2.0           → React DOM
react-router-dom@6.20.0    → Routing
@mui/material@5.14.20      → Material-UI components
@mui/icons-material        → Material-UI icons
axios@1.6.0                → HTTP client
recharts@2.10.0            → Charts
@emotion/react             → CSS-in-JS
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                           PRODUCTION                             │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │   Load Balancer  │
                    │   (Nginx)        │
                    └────────┬─────────┘
                             │
                ┌────────────┴──────────────┐
                │                           │
                ▼                           ▼
    ┌─────────────────────┐    ┌─────────────────────┐
    │  Frontend Server    │    │  Backend Servers    │
    │  (Vercel/Netlify)   │    │  (Render/Railway)   │
    │  Static React Build │    │  FastAPI + Gunicorn │
    └─────────────────────┘    └──────────┬──────────┘
                                          │
                              ┌───────────┴──────────┐
                              │                      │
                              ▼                      ▼
                    ┌──────────────┐      ┌──────────────┐
                    │  PostgreSQL  │      │  Redis Cache │
                    │  (Supabase)  │      │  (Upstash)   │
                    └──────────────┘      └──────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  S3/CloudStorage │
                    │  (File Uploads)  │
                    └──────────────────┘
```

## Security Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                      SECURITY MEASURES                           │
├─────────────────────────────────────────────────────────────────┤
│  Layer 1: Network                                               │
│    • HTTPS/TLS encryption                                       │
│    • CORS policy (specific origins)                             │
│    • Rate limiting (per IP/user)                                │
├─────────────────────────────────────────────────────────────────┤
│  Layer 2: Authentication                                        │
│    • JWT tokens                                                 │
│    • OAuth2 (Google/Microsoft)                                  │
│    • API key rotation                                           │
├─────────────────────────────────────────────────────────────────┤
│  Layer 3: Authorization                                         │
│    • Role-based access control (RBAC)                           │
│    • Resource-level permissions                                 │
│    • Team/organization isolation                                │
├─────────────────────────────────────────────────────────────────┤
│  Layer 4: Data                                                  │
│    • Encrypted at rest (database)                               │
│    • Encrypted in transit (TLS)                                 │
│    • PII data masking                                           │
├─────────────────────────────────────────────────────────────────┤
│  Layer 5: Application                                           │
│    • Input validation (Pydantic)                                │
│    • SQL injection prevention (ORM)                             │
│    • XSS protection (React escaping)                            │
│    • CSRF tokens                                                │
│    • File upload validation                                     │
└─────────────────────────────────────────────────────────────────┘
```

This architecture provides a complete overview of how ZoomBrain is structured and how all components interact with each other.
