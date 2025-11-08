# Pydantic models

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============= Document-related schemas =============

class DocumentUpload(BaseModel):
    """Schema for document upload request"""
    filename: str = Field(..., description="Name of the file")
    content_type: str = Field(..., description="MIME type of the file")


class DocumentMetadata(BaseModel):
    """Schema for document metadata"""
    id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Original filename")
    file_type: str = Field(..., description="File extension")
    upload_date: str = Field(..., description="Upload datetime")
    chunk_id: Optional[int] = Field(None, description="Chunk number if document is split")
    text_preview: Optional[str] = Field(None, description="Preview of document text")


class QueryRequest(BaseModel):
    """Schema for summarization query request"""
    query: str = Field(..., description="Search query", min_length=1)
    top_k: int = Field(5, description="Number of results to return", ge=1, le=20)


class SearchResult(BaseModel):
    """Schema for search result"""
    metadata: DocumentMetadata
    distance: float = Field(..., description="Similarity distance")
    relevance_score: Optional[float] = Field(None, description="Normalized relevance score")


class UploadResponse(BaseModel):
    """Schema for upload response"""
    success: bool = Field(..., description="Upload success status")
    filename: str = Field(..., description="Uploaded filename")
    document_id: str = Field(..., description="Generated document ID")
    chunks_created: int = Field(..., description="Number of chunks created")
    message: str = Field(..., description="Status message")


class DocumentListResponse(BaseModel):
    """Schema for document list response"""
    documents: List[Dict[str, Any]] = Field(default_factory=list)
    total_count: int = Field(..., description="Total number of documents")


# ============= Meeting-related schemas =============

class ParticipantRequest(BaseModel):
    """Schema for participant information"""
    name: str = Field(..., description="Participant name")
    role: Optional[str] = Field(None, description="Role/position in team")
    email: Optional[EmailStr] = Field(None, description="Email address")
    team: Optional[str] = Field(None, description="Team name")


class ParticipantResponse(BaseModel):
    """Schema for participant response"""
    name: str
    role: Optional[str]
    email: Optional[EmailStr]
    team: Optional[str]
    speaking_count: int = Field(0, description="Number of times spoke")
    total_words: int = Field(0, description="Total words spoken")


class ActionItemSchema(BaseModel):
    """Schema for action items"""
    text: str = Field(..., description="Action item text")
    extracted_action: str = Field(..., description="Extracted action description")
    assigned_to: List[str] = Field(default_factory=list, description="Assigned participants")


class SentimentData(BaseModel):
    """Schema for sentiment analysis data"""
    sentiment_score: float = Field(..., description="Sentiment score (-100 to 100)")
    classification: str = Field(..., description="Sentiment classification")
    total_statements: int = Field(0, description="Total number of statements")
    avg_words_per_statement: float = Field(0, description="Average words per statement")


class EngagementHeatmapPoint(BaseModel):
    """Schema for engagement heatmap data point"""
    window: str = Field(..., description="Time window")
    speaker_count: int = Field(..., description="Number of speakers in window")
    word_count: int = Field(..., description="Total words in window")
    avg_sentiment: float = Field(..., description="Average sentiment in window")
    engagement_score: float = Field(..., description="Overall engagement score")
    speakers: List[str] = Field(default_factory=list, description="List of speakers")


class MeetingUploadResponse(BaseModel):
    """Schema for meeting upload response"""
    meeting_id: str = Field(..., description="Unique meeting identifier")
    title: str = Field(..., description="Meeting title")
    date: str = Field(..., description="Meeting date")
    summary: str = Field(..., description="Generated summary")
    participants: Dict[str, Any] = Field(default_factory=dict, description="Participant data")
    participant_sentiments: Dict[str, Any] = Field(default_factory=dict, description="Sentiment analysis")
    action_items: List[Dict[str, Any]] = Field(default_factory=list, description="Action items")
    detected_dates: List[str] = Field(default_factory=list, description="Detected dates")
    engagement_heatmap: List[Dict[str, Any]] = Field(default_factory=list, description="Engagement heatmap")
    message: str = Field(..., description="Status message")


class MeetingSummaryResponse(BaseModel):
    """Schema for meeting summary response"""
    meeting_id: str
    title: str
    date: str
    summary: str
    participants: Dict[str, Any]
    action_items: List[Dict[str, Any]]
    sentiment_data: Dict[str, Any]
    engagement_heatmap: List[Dict[str, Any]]


class SentimentAnalysisResponse(BaseModel):
    """Schema for sentiment analysis response"""
    participant_sentiments: Dict[str, SentimentData]
    overall_sentiment: float = Field(..., description="Overall meeting sentiment")
    engagement_heatmap: List[EngagementHeatmapPoint]


# ============= System schemas =============

class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str = Field("healthy", description="Service status")
    indexed_documents: int = Field(..., description="Number of indexed documents")
    version: str = Field("2.0.0", description="API version")
