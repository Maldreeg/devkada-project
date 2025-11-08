# FastAPI app + endpoints

from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict
import os
import json
import shutil
from datetime import datetime
import uuid

from schemas import (
    MeetingUploadResponse, MeetingSummaryResponse, ParticipantRequest,
    ParticipantResponse, SentimentAnalysisResponse, UploadResponse,
    DocumentListResponse, HealthResponse
)
from meeting_processor import MeetingProcessor
from sentiment_analyzer import SentimentAnalyzer
from llm_summarizer import LLMSummarizer
from integrations import EmailService, GoogleCalendarService
from utils_parsers import extract_text_from_file, chunk_text
from summarizer import DocumentSummarizer

app = FastAPI(
    title="ZoomBrain - AI Meeting Summarization API",
    version="2.0.0",
    description="AI-powered meeting summarization with sentiment analysis and task extraction"
)

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
meeting_processor = MeetingProcessor()
sentiment_analyzer = SentimentAnalyzer()
llm_summarizer = LLMSummarizer()
email_service = EmailService()
calendar_service = GoogleCalendarService()
document_summarizer = DocumentSummarizer()

# In-memory storage for meetings (use database in production)
meetings_db = {}
participants_db = {}

# Create upload directory
UPLOAD_DIR = "app/data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        indexed_documents=document_summarizer.get_document_count(),
        version="2.0.0"
    )


@app.post("/api/meetings/upload", response_model=MeetingUploadResponse)
async def upload_meeting(
    file: UploadFile = File(...),
    meeting_title: str = Form(...),
    meeting_date: Optional[str] = Form(None),
    summary_style: str = Form("bullet_points"),
    detail_level: str = Form("medium")
):
    """
    Upload meeting transcript (VTT, TXT) and process it
    
    - **file**: Transcript file (VTT or TXT format)
    - **meeting_title**: Title of the meeting
    - **meeting_date**: Optional meeting date
    - **summary_style**: Style for summary (bullet_points, narrative, executive)
    - **detail_level**: Detail level (brief, medium, detailed)
    """
    try:
        # Generate unique meeting ID
        meeting_id = str(uuid.uuid4())
        
        # Save uploaded file
        file_extension = os.path.splitext(file.filename)[1].lower()
        file_path = os.path.join(UPLOAD_DIR, f"{meeting_id}{file_extension}")
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Read file content
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Parse transcript based on file type
        if file_extension == ".vtt":
            segments = meeting_processor.parse_vtt(content)
        else:  # .txt or other
            segments = meeting_processor.parse_txt_transcript(content)
        
        # Extract participants
        participants = meeting_processor.extract_participants(segments)
        
        # Analyze sentiment for each participant
        participant_sentiments = sentiment_analyzer.analyze_participant_sentiment(
            segments, participants
        )
        
        # Detect action items
        full_text = " ".join([seg['text'] for seg in segments])
        action_items = meeting_processor.detect_action_items(full_text)
        
        # Assign tasks to participants
        assigned_tasks = meeting_processor.assign_tasks_to_participants(
            action_items, participants, full_text
        )
        
        # Generate summary
        summary = llm_summarizer.summarize_transcript(
            full_text, summary_style, detail_level
        )
        
        # Detect dates for calendar integration
        detected_dates = meeting_processor.detect_dates(full_text)
        
        # Calculate engagement heatmap
        engagement_heatmap = sentiment_analyzer.calculate_engagement_heatmap(segments)
        
        # Store meeting data
        meetings_db[meeting_id] = {
            "meeting_id": meeting_id,
            "title": meeting_title,
            "date": meeting_date or datetime.now().isoformat(),
            "file_path": file_path,
            "segments": segments,
            "participants": participants,
            "participant_sentiments": participant_sentiments,
            "action_items": assigned_tasks,
            "summary": summary,
            "detected_dates": detected_dates,
            "engagement_heatmap": engagement_heatmap,
            "summary_style": summary_style,
            "detail_level": detail_level
        }
        
        # Send sentiment notifications if needed
        for participant_name, sentiment_data in participant_sentiments.items():
            should_send, msg_type = sentiment_analyzer.should_send_sentiment_notification(
                sentiment_data['sentiment_score']
            )
            
            if should_send:
                participant = participants.get(participant_name, {})
                if participant.get('email'):
                    email_service.send_sentiment_notification(
                        recipient_email=participant['email'],
                        recipient_name=participant_name,
                        sentiment_score=sentiment_data['sentiment_score'],
                        meeting_title=meeting_title
                    )
        
        return MeetingUploadResponse(
            meeting_id=meeting_id,
            title=meeting_title,
            date=meeting_date or datetime.now().isoformat(),
            summary=summary,
            participants=participants,
            participant_sentiments=participant_sentiments,
            action_items=assigned_tasks,
            detected_dates=detected_dates,
            engagement_heatmap=engagement_heatmap,
            message="Meeting processed successfully"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing meeting: {str(e)}")


@app.post("/api/documents/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document (PDF, PPTX, TXT) for indexing
    This is separate from meeting transcripts - for reference documents
    """
    try:
        # Save file temporarily
        file_extension = os.path.splitext(file.filename)[1].lower()
        temp_path = os.path.join(UPLOAD_DIR, f"temp_{uuid.uuid4()}{file_extension}")
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text
        text = extract_text_from_file(temp_path)
        
        # Chunk text
        chunks = chunk_text(text, chunk_size=500, overlap=50)
        
        # Create embeddings (placeholder - using random vectors for now)
        import numpy as np
        embeddings = np.random.rand(len(chunks), 384).astype('float32')
        
        # Create metadata for each chunk
        metadata = []
        for i, chunk in enumerate(chunks):
            metadata.append({
                "id": str(uuid.uuid4()),
                "filename": file.filename,
                "file_type": file_extension,
                "upload_date": datetime.now().isoformat(),
                "chunk_id": i,
                "text_preview": chunk[:200]
            })
        
        # Add to index
        document_summarizer.add_documents(embeddings, metadata)
        
        # Clean up temp file
        os.remove(temp_path)
        
        return UploadResponse(
            success=True,
            filename=file.filename,
            document_id=metadata[0]["id"],
            chunks_created=len(chunks),
            message="Document uploaded and indexed successfully"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")


@app.get("/api/meetings/{meeting_id}", response_model=MeetingSummaryResponse)
async def get_meeting(meeting_id: str):
    """Get meeting details by ID"""
    if meeting_id not in meetings_db:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    meeting = meetings_db[meeting_id]
    
    return MeetingSummaryResponse(
        meeting_id=meeting_id,
        title=meeting["title"],
        date=meeting["date"],
        summary=meeting["summary"],
        participants=meeting["participants"],
        action_items=meeting["action_items"],
        sentiment_data=meeting["participant_sentiments"],
        engagement_heatmap=meeting["engagement_heatmap"]
    )


@app.get("/api/meetings")
async def list_meetings():
    """List all processed meetings"""
    meetings_list = [
        {
            "meeting_id": mid,
            "title": data["title"],
            "date": data["date"],
            "participant_count": len(data["participants"])
        }
        for mid, data in meetings_db.items()
    ]
    return {"meetings": meetings_list, "total": len(meetings_list)}


@app.post("/api/participants/add")
async def add_participant(participant: ParticipantRequest):
    """
    Add or update participant information
    This allows users to pre-register participants with their roles and emails
    """
    participants_db[participant.name] = {
        "name": participant.name,
        "role": participant.role,
        "email": participant.email,
        "team": participant.team
    }
    
    return {
        "message": "Participant added successfully",
        "participant": participants_db[participant.name]
    }


@app.get("/api/participants")
async def list_participants():
    """List all registered participants"""
    return {"participants": list(participants_db.values()), "total": len(participants_db)}


@app.post("/api/meetings/{meeting_id}/update-participants")
async def update_meeting_participants(meeting_id: str, participants: List[ParticipantRequest]):
    """Update participant information for a specific meeting"""
    if meeting_id not in meetings_db:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    meeting = meetings_db[meeting_id]
    
    # Update participant info
    for participant in participants:
        if participant.name in meeting["participants"]:
            meeting["participants"][participant.name].update({
                "role": participant.role,
                "email": participant.email,
                "team": participant.team
            })
    
    return {"message": "Participants updated successfully"}


@app.post("/api/meetings/{meeting_id}/send-summary")
async def send_meeting_summary(meeting_id: str):
    """Send meeting summary via email to all participants"""
    if meeting_id not in meetings_db:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    meeting = meetings_db[meeting_id]
    
    # Collect participant emails
    recipient_emails = [
        p.get('email') for p in meeting["participants"].values()
        if p.get('email')
    ]
    
    if not recipient_emails:
        raise HTTPException(status_code=400, detail="No participant emails available")
    
    # Send email
    success = email_service.send_meeting_summary(
        recipient_emails=recipient_emails,
        meeting_title=meeting["title"],
        summary=meeting["summary"],
        action_items=meeting["action_items"],
        meeting_date=datetime.fromisoformat(meeting["date"])
    )
    
    if success:
        return {"message": "Summary sent successfully", "recipients": len(recipient_emails)}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email")


@app.get("/api/documents", response_model=DocumentListResponse)
async def list_documents():
    """List all indexed documents"""
    # This would retrieve from document_summarizer.metadata
    return DocumentListResponse(
        documents=document_summarizer.metadata[:50],  # Limit to 50
        total_count=len(document_summarizer.metadata)
    )


@app.post("/api/documents/search")
async def search_documents(query: str, top_k: int = 5):
    """Search indexed documents"""
    try:
        # Create query embedding (placeholder - using random vector)
        import numpy as np
        query_embedding = np.random.rand(1, 384).astype('float32')
        
        # Search
        results = document_summarizer.search(query_embedding, top_k)
        
        return {
            "query": query,
            "results": results,
            "total_results": len(results)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching documents: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
