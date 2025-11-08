# Quick Start Guide

## Starting the Application

### 1. Start Backend (Terminal 1)

```powershell
cd zoombrain
.\venv\Scripts\activate
cd app
python main.py
```

Backend will run on: http://localhost:8000

### 2. Start Frontend (Terminal 2)

```powershell
cd frontend
npm start
```

Frontend will run on: http://localhost:3000

## First Time Setup

### Backend Setup
```powershell
cd zoombrain
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cp .env.template .env
# Edit .env with your email credentials
```

### Frontend Setup
```powershell
cd frontend
npm install
```

## Testing the Application

1. Open http://localhost:3000
2. Click "Upload Meeting"
3. Upload a sample transcript file
4. View the generated summary, sentiment analysis, and action items

## Sample Transcript Format (TXT)

Create a file `sample_meeting.txt`:

```
John Smith: Good morning everyone, let's start our weekly standup.

Sarah Johnson: Thanks John. I completed the user authentication feature yesterday. It's ready for review.

John Smith: Excellent work Sarah! Mike, can you review it by Friday?

Mike Chen: Absolutely, I'll have the review done by end of day Thursday.

Sarah Johnson: I'm also starting work on the dashboard analytics next. Should be exciting!

Mike Chen: I'm a bit concerned about the performance issues we saw in testing. We need to address those soon.

John Smith: Good point Mike. Let's schedule a separate meeting to discuss performance optimizations. Sarah, please send out a calendar invite for next Tuesday.

Sarah Johnson: Will do! I'll send it out today.
```

## Common Issues

### Backend won't start
- Check if port 8000 is available
- Verify virtual environment is activated
- Run `pip install -r requirements.txt` again

### Frontend won't start
- Check if port 3000 is available
- Delete `node_modules` and run `npm install` again
- Make sure backend is running first

### Email not sending
- Use Gmail app-specific password (not your regular password)
- Enable 2-factor authentication first
- Check SMTP settings in .env

## Next Steps

1. Add participants in the Participants page
2. Upload reference documents for context
3. Configure email settings for notifications
4. Explore different summary styles and detail levels
