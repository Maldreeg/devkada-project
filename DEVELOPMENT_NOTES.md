# ZoomBrain Development Notes

## Architecture Overview

### Backend (Python/FastAPI)
- **Framework**: FastAPI (async, fast, automatic API documentation)
- **Vector Database**: FAISS (efficient similarity search)
- **Embeddings**: Sentence Transformers (384-dimensional vectors)
- **Document Parsing**: PyPDF2, python-pptx
- **Email**: SMTP (Gmail integration)

### Frontend (React)
- **UI Framework**: Material-UI (MUI v5)
- **Charts**: Recharts (responsive data visualization)
- **HTTP Client**: Axios
- **Routing**: React Router v6

## Key Design Decisions

### 1. In-Memory Storage
- Currently using in-memory dictionaries for meetings and participants
- **Production**: Replace with PostgreSQL or MongoDB
- **Reason**: Simplicity for development and demo purposes

### 2. Sentiment Analysis
- Implemented custom lexicon-based approach
- **Alternative**: Could use transformer models (e.g., distilbert-base-uncased-finetuned-sst-2-english)
- **Reason**: Lightweight, no GPU required, fast processing

### 3. LLM Integration
- Supports OpenAI API for better summaries
- Falls back to extractive summarization if API key not available
- **Alternative**: Hugging Face models, Ollama (local), Together AI
- **Reason**: Flexibility and cost control

### 4. Email Notifications
- Triggered automatically for extreme sentiment (±80)
- Manual trigger for full meeting summaries
- **Production**: Add queue system (Celery) for background processing

## Data Flow

```
Transcript Upload → Parse (VTT/TXT) → Extract Participants → 
Analyze Sentiment → Extract Tasks → Generate Summary → 
Store Results → Send Notifications (if needed)
```

## API Design Patterns

### RESTful Endpoints
- `POST /api/meetings/upload` - Create new meeting
- `GET /api/meetings/{id}` - Read meeting
- `GET /api/meetings` - List meetings
- `POST /api/meetings/{id}/update-participants` - Update meeting

### Response Format
```json
{
  "meeting_id": "uuid",
  "title": "string",
  "summary": "string",
  "participants": {},
  "action_items": [],
  "sentiment_data": {},
  "engagement_heatmap": []
}
```

## Frontend Components

### Pages
1. **HomePage**: Dashboard with recent meetings
2. **UploadPage**: Meeting transcript upload form
3. **MeetingDetailPage**: Full meeting analysis display
4. **ParticipantsPage**: Participant management
5. **DocumentsPage**: Reference document management

### Reusable Patterns
- Material-UI components for consistency
- Axios interceptors for error handling
- React hooks for state management

## Future Enhancements

### Phase 1 (MVP) ✅
- [x] Transcript processing
- [x] Sentiment analysis
- [x] Task extraction
- [x] Basic email notifications
- [x] React frontend

### Phase 2 (Production Ready)
- [ ] Database integration (PostgreSQL)
- [ ] User authentication (JWT)
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Comprehensive testing
- [ ] Rate limiting
- [ ] Caching (Redis)

### Phase 3 (Advanced Features)
- [ ] Real-time processing (WebSocket)
- [ ] Multi-language support
- [ ] Custom ML models
- [ ] Slack/Teams bots
- [ ] Calendar sync
- [ ] Knowledge graph building
- [ ] Conversation threading
- [ ] Speaker diarization

## Performance Considerations

### Current Limitations
- In-memory storage (not scalable)
- Synchronous processing (blocks request)
- Random embeddings (not semantic)

### Optimization Strategies
1. **Async Processing**: Use Celery + Redis for background jobs
2. **Real Embeddings**: Implement sentence-transformers properly
3. **Caching**: Cache summaries and sentiment scores
4. **Batch Processing**: Process multiple files simultaneously
5. **CDN**: Serve static frontend assets via CDN

## Security Considerations

### Current Implementation
- CORS enabled for development (allow all origins)
- No authentication/authorization
- Env variables for sensitive data

### Production Requirements
1. **Authentication**: JWT tokens, OAuth2
2. **Authorization**: Role-based access control
3. **CORS**: Restrict to specific origins
4. **HTTPS**: Enforce SSL/TLS
5. **Input Validation**: Sanitize all inputs
6. **Rate Limiting**: Prevent abuse
7. **File Upload**: Validate file types and sizes
8. **SQL Injection**: Use parameterized queries (when adding DB)

## Testing Strategy

### Unit Tests
- Meeting processor functions
- Sentiment analyzer logic
- Transcript parsers

### Integration Tests
- API endpoints
- Email service
- Document indexing

### E2E Tests
- Full workflow from upload to summary
- Frontend user flows

## Deployment

### Development
```powershell
# Backend
cd zoombrain/app
python main.py

# Frontend
cd frontend
npm start
```

### Production (Docker)
```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

# Frontend Dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY src/ ./src
COPY public/ ./public
RUN npm run build
CMD ["npx", "serve", "-s", "build"]
```

### Cloud Deployment Options
1. **Backend**: Render, Railway, Heroku, AWS Lambda
2. **Frontend**: Vercel, Netlify, AWS S3 + CloudFront
3. **Database**: Supabase, PlanetScale, AWS RDS
4. **Storage**: AWS S3, Cloudinary

## Monitoring & Logging

### Recommended Tools
- **Logging**: Python logging, Winston (Node.js)
- **Monitoring**: Sentry (errors), DataDog (APM)
- **Analytics**: Google Analytics, Mixpanel
- **Uptime**: UptimeRobot, Pingdom

## Cost Optimization

### Free Tier Options
- **LLM**: Hugging Face Inference API
- **Email**: SendGrid (100 emails/day free)
- **Hosting**: Render, Railway (free tier)
- **Database**: Supabase, MongoDB Atlas (free tier)
- **Storage**: Cloudinary (free tier)

### Paid Services (Optional)
- **OpenAI API**: $0.002/1K tokens (GPT-3.5-turbo)
- **Anthropic Claude**: Similar pricing
- **Google Calendar API**: Free
- **Slack API**: Free for basic features
