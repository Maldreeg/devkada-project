# Meeting transcript processing and analysis

import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import json


class MeetingProcessor:
    """Process and analyze meeting transcripts"""
    
    def __init__(self):
        self.participants = {}
        self.transcript_segments = []
    
    def parse_vtt(self, vtt_content: str) -> List[Dict]:
        """
        Parse VTT (WebVTT) transcript format
        
        Args:
            vtt_content: VTT file content as string
            
        Returns:
            List of transcript segments with timestamps and speaker info
        """
        segments = []
        lines = vtt_content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for timestamp lines (e.g., "00:00:10.000 --> 00:00:15.000")
            if '-->' in line:
                timestamp = line
                i += 1
                
                # Get the text (may span multiple lines)
                text_lines = []
                while i < len(lines) and lines[i].strip() and '-->' not in lines[i]:
                    text_lines.append(lines[i].strip())
                    i += 1
                
                text = ' '.join(text_lines)
                
                # Extract speaker if present (format: "Speaker Name: text")
                speaker = "Unknown"
                if ':' in text:
                    parts = text.split(':', 1)
                    if len(parts[0]) < 50:  # Likely a speaker name
                        speaker = parts[0].strip()
                        text = parts[1].strip()
                
                segments.append({
                    'timestamp': timestamp,
                    'speaker': speaker,
                    'text': text
                })
            
            i += 1
        
        return segments
    
    def parse_txt_transcript(self, txt_content: str) -> List[Dict]:
        """
        Parse plain text transcript with speaker labels
        Expected format: "Speaker Name: text" or just plain text
        
        Args:
            txt_content: Text file content
            
        Returns:
            List of transcript segments
        """
        segments = []
        lines = txt_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to extract speaker
            speaker = "Unknown"
            text = line
            
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts[0]) < 50:  # Likely a speaker name
                    speaker = parts[0].strip()
                    text = parts[1].strip()
            
            segments.append({
                'speaker': speaker,
                'text': text,
                'timestamp': None
            })
        
        return segments
    
    def extract_participants(self, segments: List[Dict]) -> Dict[str, Dict]:
        """
        Extract unique participants from transcript segments
        
        Args:
            segments: List of transcript segments
            
        Returns:
            Dictionary of participants with their statistics
        """
        participants = {}
        
        for segment in segments:
            speaker = segment.get('speaker', 'Unknown')
            
            if speaker not in participants:
                participants[speaker] = {
                    'name': speaker,
                    'speaking_count': 0,
                    'total_words': 0,
                    'role': None,
                    'email': None
                }
            
            participants[speaker]['speaking_count'] += 1
            participants[speaker]['total_words'] += len(segment['text'].split())
        
        return participants
    
    def detect_action_items(self, text: str) -> List[Dict]:
        """
        Detect action items and tasks from text
        
        Args:
            text: Text to analyze
            
        Returns:
            List of detected action items
        """
        action_items = []
        
        # Common action item patterns
        patterns = [
            r'(?:will|should|must|need to|have to|going to)\s+(.{10,100})',
            r'(?:action item|task|todo|to-do):\s*(.{10,100})',
            r'(?:please|can you|could you)\s+(.{10,100})',
            r'(?:assigned to|responsibility of)\s+(\w+(?:\s+\w+)?)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                action_items.append({
                    'text': match.group(0),
                    'extracted_action': match.group(1) if len(match.groups()) > 0 else match.group(0)
                })
        
        return action_items
    
    def detect_dates(self, text: str) -> List[str]:
        """
        Detect dates mentioned in text
        
        Args:
            text: Text to analyze
            
        Returns:
            List of detected dates
        """
        dates = []
        
        # Date patterns
        patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or DD-MM-YYYY
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}\b',
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}\b',
            r'\b(?:next|this)\s+(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b',
            r'\b(?:tomorrow|today|yesterday)\b',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            dates.extend([match.group(0) for match in matches])
        
        return dates
    
    def segment_by_topics(self, segments: List[Dict], keywords: List[str] = None) -> Dict[str, List[Dict]]:
        """
        Segment meeting by topics based on keywords or content shifts
        
        Args:
            segments: List of transcript segments
            keywords: Optional list of keywords to identify topics
            
        Returns:
            Dictionary of topics with their segments
        """
        # Simple topic segmentation based on time gaps or keyword detection
        topics = {'General Discussion': []}
        current_topic = 'General Discussion'
        
        if keywords:
            for segment in segments:
                text = segment['text'].lower()
                found_topic = False
                
                for keyword in keywords:
                    if keyword.lower() in text:
                        current_topic = keyword.title()
                        if current_topic not in topics:
                            topics[current_topic] = []
                        found_topic = True
                        break
                
                if not found_topic:
                    current_topic = 'General Discussion'
                
                topics[current_topic].append(segment)
        else:
            topics['General Discussion'] = segments
        
        return topics
    
    def assign_tasks_to_participants(
        self, 
        action_items: List[Dict], 
        participants: Dict[str, Dict],
        context: str = ""
    ) -> List[Dict]:
        """
        Assign action items to participants based on context
        
        Args:
            action_items: List of detected action items
            participants: Dictionary of participants
            context: Surrounding context text
            
        Returns:
            List of action items with assigned participants
        """
        assigned_tasks = []
        
        for item in action_items:
            task = item.copy()
            task['assigned_to'] = []
            
            # Look for participant names in the action item or context
            search_text = (item['text'] + ' ' + context).lower()
            
            for participant_name in participants.keys():
                if participant_name.lower() in search_text:
                    task['assigned_to'].append(participant_name)
            
            # If no assignment found, mark as unassigned
            if not task['assigned_to']:
                task['assigned_to'] = ['Unassigned']
            
            assigned_tasks.append(task)
        
        return assigned_tasks
