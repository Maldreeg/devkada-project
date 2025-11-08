# Integrations with external services (Email, Google Calendar, etc.)

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class EmailService:
    """Handle email notifications"""
    
    def __init__(self, smtp_server: str = None, smtp_port: int = 587):
        """
        Initialize email service
        
        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP port (default: 587 for TLS)
        """
        self.smtp_server = smtp_server or os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = smtp_port
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
    
    def send_sentiment_notification(
        self, 
        recipient_email: str,
        recipient_name: str,
        sentiment_score: float,
        meeting_title: str = "Recent Meeting"
    ) -> bool:
        """
        Send sentiment-based notification email
        
        Args:
            recipient_email: Email address of recipient
            recipient_name: Name of recipient
            sentiment_score: Sentiment score
            meeting_title: Title of the meeting
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.sender_email or not self.sender_password:
            print("Email credentials not configured")
            return False
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"Meeting Feedback - {meeting_title}"
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            # Create email body based on sentiment
            if sentiment_score >= 80:
                body = f"""
                <html>
                <body>
                    <h2>Congratulations, {recipient_name}! 🎉</h2>
                    <p>We noticed your positive and enthusiastic participation in the recent meeting: <strong>{meeting_title}</strong></p>
                    <p>Your sentiment score: <strong>{sentiment_score:.1f}/100</strong></p>
                    <p>Your engagement and positive energy greatly contribute to our team's success. Keep up the great work!</p>
                    <br>
                    <p>Best regards,<br>Meeting Analytics Team</p>
                </body>
                </html>
                """
            else:  # sentiment_score <= -80
                body = f"""
                <html>
                <body>
                    <h2>Hello {recipient_name},</h2>
                    <p>We noticed some concerns during the recent meeting: <strong>{meeting_title}</strong></p>
                    <p>Your sentiment score: <strong>{sentiment_score:.1f}/100</strong></p>
                    <p>We value your well-being and want to ensure you have the support you need. 
                    If you're facing any challenges or would like to discuss anything, please don't hesitate to reach out.</p>
                    <p>How are you feeling? Is there anything we can help with?</p>
                    <br>
                    <p>We're here to support you,<br>Meeting Analytics Team</p>
                </body>
                </html>
                """
            
            html_part = MIMEText(body, "html")
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print(f"Sentiment notification sent to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_meeting_summary(
        self,
        recipient_emails: List[str],
        meeting_title: str,
        summary: str,
        action_items: List[Dict],
        meeting_date: datetime = None
    ) -> bool:
        """
        Send meeting summary email to participants
        
        Args:
            recipient_emails: List of recipient email addresses
            meeting_title: Title of the meeting
            summary: Meeting summary text
            action_items: List of action items
            meeting_date: Date of the meeting
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.sender_email or not self.sender_password:
            print("Email credentials not configured")
            return False
        
        try:
            meeting_date_str = meeting_date.strftime("%B %d, %Y") if meeting_date else "Recent"
            
            # Create action items HTML
            action_items_html = ""
            if action_items:
                action_items_html = "<h3>Action Items:</h3><ul>"
                for item in action_items:
                    assigned = ", ".join(item.get('assigned_to', ['Unassigned']))
                    action_items_html += f"<li><strong>{assigned}:</strong> {item.get('text', '')}</li>"
                action_items_html += "</ul>"
            
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"Meeting Summary - {meeting_title}"
            message["From"] = self.sender_email
            message["To"] = ", ".join(recipient_emails)
            
            body = f"""
            <html>
            <body>
                <h2>Meeting Summary: {meeting_title}</h2>
                <p><strong>Date:</strong> {meeting_date_str}</p>
                <hr>
                <h3>Summary:</h3>
                <p>{summary}</p>
                <hr>
                {action_items_html}
                <br>
                <p><em>This summary was automatically generated by ZoomBrain AI.</em></p>
            </body>
            </html>
            """
            
            html_part = MIMEText(body, "html")
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print(f"Meeting summary sent to {len(recipient_emails)} recipients")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False


class GoogleCalendarService:
    """Handle Google Calendar integration"""
    
    def __init__(self):
        """Initialize Google Calendar service"""
        self.credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
        self.calendar_id = os.getenv('GOOGLE_CALENDAR_ID', 'primary')
    
    def create_event(
        self,
        title: str,
        description: str,
        start_time: datetime,
        end_time: datetime,
        attendees: List[str] = None
    ) -> Optional[str]:
        """
        Create a calendar event (placeholder - requires google-auth-oauthlib)
        
        Args:
            title: Event title
            description: Event description
            start_time: Start datetime
            end_time: End datetime
            attendees: List of attendee email addresses
            
        Returns:
            Event ID if successful, None otherwise
        """
        # This is a placeholder implementation
        # To fully implement, you would need:
        # 1. pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
        # 2. Set up OAuth 2.0 credentials from Google Cloud Console
        # 3. Use the Google Calendar API
        
        print(f"[PLACEHOLDER] Would create calendar event: {title}")
        print(f"  Start: {start_time}")
        print(f"  End: {end_time}")
        print(f"  Attendees: {attendees}")
        
        # Actual implementation would look like:
        # from google.oauth2.credentials import Credentials
        # from googleapiclient.discovery import build
        # 
        # service = build('calendar', 'v3', credentials=creds)
        # event = {
        #     'summary': title,
        #     'description': description,
        #     'start': {'dateTime': start_time.isoformat(), 'timeZone': 'UTC'},
        #     'end': {'dateTime': end_time.isoformat(), 'timeZone': 'UTC'},
        #     'attendees': [{'email': email} for email in attendees]
        # }
        # event = service.events().insert(calendarId=self.calendar_id, body=event).execute()
        # return event.get('id')
        
        return None
    
    def parse_date_from_text(self, date_text: str) -> Optional[datetime]:
        """
        Parse date from natural language text
        
        Args:
            date_text: Date in text format
            
        Returns:
            Datetime object if parsed successfully, None otherwise
        """
        # Simple date parsing - can be enhanced with dateutil or dateparser
        from datetime import datetime, timedelta
        
        date_text = date_text.lower().strip()
        
        # Handle relative dates
        if 'tomorrow' in date_text:
            return datetime.now() + timedelta(days=1)
        elif 'today' in date_text:
            return datetime.now()
        elif 'next week' in date_text:
            return datetime.now() + timedelta(days=7)
        
        # Try to parse standard formats
        formats = [
            '%m/%d/%Y',
            '%m-%d-%Y',
            '%Y-%m-%d',
            '%B %d, %Y',
            '%b %d, %Y'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_text, fmt)
            except ValueError:
                continue
        
        return None


class SlackIntegration:
    """Handle Slack integration (placeholder)"""
    
    def __init__(self):
        """Initialize Slack integration"""
        self.webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        self.bot_token = os.getenv('SLACK_BOT_TOKEN')
    
    def send_summary(self, channel: str, summary: str) -> bool:
        """
        Send meeting summary to Slack channel
        
        Args:
            channel: Slack channel ID or name
            summary: Summary text to send
            
        Returns:
            True if successful, False otherwise
        """
        # Placeholder - would require slack_sdk package
        print(f"[PLACEHOLDER] Would send to Slack channel {channel}: {summary}")
        return False


class TeamsIntegration:
    """Handle Microsoft Teams integration (placeholder)"""
    
    def __init__(self):
        """Initialize Teams integration"""
        self.webhook_url = os.getenv('TEAMS_WEBHOOK_URL')
    
    def send_summary(self, channel_url: str, summary: str) -> bool:
        """
        Send meeting summary to Teams channel
        
        Args:
            channel_url: Teams channel webhook URL
            summary: Summary text to send
            
        Returns:
            True if successful, False otherwise
        """
        # Placeholder - would use requests to post to webhook
        print(f"[PLACEHOLDER] Would send to Teams: {summary}")
        return False
