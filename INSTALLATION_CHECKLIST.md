# Installation & Testing Checklist

## ✅ Pre-Installation Checklist

- [ ] Python 3.8 or higher installed
- [ ] Node.js 16 or higher installed
- [ ] npm or yarn installed
- [ ] Git installed (optional)
- [ ] Text editor or IDE installed

## 📦 Backend Installation Steps

### 1. Create Virtual Environment
```powershell
cd zoombrain
python -m venv venv
```
- [ ] Virtual environment created successfully

### 2. Activate Virtual Environment
```powershell
.\venv\Scripts\activate
```
- [ ] Prompt shows `(venv)` prefix

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```
- [ ] All packages installed without errors
- [ ] No version conflicts

### 4. Configure Environment
```powershell
cp .env.template .env
```
- [ ] `.env` file created
- [ ] Email credentials added (optional)
- [ ] OpenAI API key added (optional)

### 5. Create Data Directories
```powershell
mkdir app\data\uploads
mkdir app\data\indexes
```
- [ ] Directories created

### 6. Test Backend
```powershell
cd app
python main.py
```
- [ ] Server starts without errors
- [ ] Message shows: "Uvicorn running on http://0.0.0.0:8000"
- [ ] Can access http://localhost:8000
- [ ] Can access http://localhost:8000/docs (Swagger UI)

## 🎨 Frontend Installation Steps

### 1. Install Dependencies
```powershell
cd frontend
npm install
```
- [ ] All packages installed without errors
- [ ] No critical vulnerabilities

### 2. Test Frontend
```powershell
npm start
```
- [ ] Server starts without errors
- [ ] Browser opens to http://localhost:3000
- [ ] No console errors
- [ ] UI renders correctly

## 🧪 Functionality Tests

### Test 1: Health Check
- [ ] Backend at http://localhost:8000 returns JSON
- [ ] Frontend at http://localhost:3000 displays homepage

### Test 2: Upload Sample Meeting
1. [ ] Navigate to "Upload Meeting" page
2. [ ] Select `sample_data/sample_meeting.vtt`
3. [ ] Enter title: "Test Meeting"
4. [ ] Click "Process Meeting"
5. [ ] Wait for processing (5-10 seconds)
6. [ ] Redirected to meeting detail page
7. [ ] Summary is displayed
8. [ ] Participants are listed
9. [ ] Sentiment chart shows data
10. [ ] Action items are shown

### Test 3: Participant Management
1. [ ] Navigate to "Participants" page
2. [ ] Click "Add Participant"
3. [ ] Enter name: "Test User"
4. [ ] Enter role: "Tester"
5. [ ] Enter email: "test@example.com"
6. [ ] Click "Add Participant"
7. [ ] Participant appears in list

### Test 4: Document Upload
1. [ ] Navigate to "Documents" page
2. [ ] Click "Upload Document"
3. [ ] Select any PDF/TXT file
4. [ ] Wait for upload
5. [ ] Document appears in list
6. [ ] Search functionality works

### Test 5: Email Notification (Optional)
- [ ] Email credentials configured in `.env`
- [ ] Upload meeting with extreme sentiment
- [ ] Check recipient inbox for notification email
- [ ] OR manually click "Send Summary via Email" on meeting detail page

## 🐛 Troubleshooting

### Backend Issues

**Problem**: ModuleNotFoundError
```powershell
# Solution:
.\venv\Scripts\activate
pip install -r requirements.txt
```
- [ ] Resolved

**Problem**: Port 8000 already in use
```powershell
# Solution: Find and kill process or change port
netstat -ano | findstr :8000
# Kill process or edit main.py to use different port
```
- [ ] Resolved

**Problem**: Import errors for fastapi/uvicorn
```powershell
# Solution: Reinstall
pip install --upgrade fastapi uvicorn
```
- [ ] Resolved

### Frontend Issues

**Problem**: npm install fails
```powershell
# Solution: Clear cache and retry
npm cache clean --force
rm -r node_modules package-lock.json
npm install
```
- [ ] Resolved

**Problem**: Port 3000 already in use
```
# Solution: Kill process or use different port
# When prompted, press 'Y' to use different port
```
- [ ] Resolved

**Problem**: Cannot connect to backend
- [ ] Backend is running on port 8000
- [ ] No firewall blocking connection
- [ ] Browser console shows no CORS errors

## 📊 Verification Tests

### API Endpoint Tests

**Test GET /**
```powershell
curl http://localhost:8000/
```
Expected: JSON with status, version, indexed_documents
- [ ] Passed

**Test POST /api/participants/add**
```powershell
curl -X POST http://localhost:8000/api/participants/add `
  -H "Content-Type: application/json" `
  -d '{"name":"Test User","role":"Developer","email":"test@example.com"}'
```
Expected: Success message with participant data
- [ ] Passed

**Test GET /api/participants**
```powershell
curl http://localhost:8000/api/participants
```
Expected: JSON with participants array
- [ ] Passed

**Test GET /api/meetings**
```powershell
curl http://localhost:8000/api/meetings
```
Expected: JSON with meetings array
- [ ] Passed

### Frontend Component Tests

- [ ] HomePage loads and displays features
- [ ] Navigation menu works (all links)
- [ ] Upload form validation works
- [ ] Meeting detail page displays charts
- [ ] Participants table renders correctly
- [ ] Documents search is functional
- [ ] Responsive design works on mobile

## 🎯 Feature Verification

### Core Features
- [ ] VTT transcript parsing works
- [ ] TXT transcript parsing works
- [ ] Participant extraction works
- [ ] Sentiment analysis generates scores
- [ ] Action items are detected
- [ ] Dates are extracted
- [ ] Summary is generated
- [ ] Engagement heatmap is created

### Advanced Features
- [ ] Multiple summary styles work
- [ ] Different detail levels work
- [ ] Email notifications send (if configured)
- [ ] Document upload and indexing works
- [ ] Document search returns results
- [ ] Charts render correctly (Recharts)

## 📝 Documentation Checklist

- [ ] README.md is comprehensive
- [ ] QUICKSTART.md is easy to follow
- [ ] ARCHITECTURE.md explains system design
- [ ] DEVELOPMENT_NOTES.md covers technical details
- [ ] PROJECT_SUMMARY.md provides overview
- [ ] Sample data files are available
- [ ] .env.template has all variables
- [ ] .gitignore covers sensitive files

## 🚀 Ready for Demo

### Pre-Demo Setup
- [ ] Backend running
- [ ] Frontend running
- [ ] Sample data prepared
- [ ] At least one meeting uploaded
- [ ] At least one participant added
- [ ] Email notifications tested (optional)

### Demo Flow
1. [ ] Show homepage with features
2. [ ] Upload sample meeting
3. [ ] Show detailed analysis
4. [ ] Demonstrate sentiment charts
5. [ ] Show action items extraction
6. [ ] Add participant
7. [ ] Upload reference document
8. [ ] Search documents
9. [ ] Send email summary (optional)

## 🎉 Completion

### All Systems Go ✅
- [ ] Backend: ✅ Running
- [ ] Frontend: ✅ Running
- [ ] Features: ✅ Working
- [ ] Tests: ✅ Passing
- [ ] Documentation: ✅ Complete

**Installation Status**: [ ] READY FOR USE

**Notes**:
_Add any issues or observations here_

---

**Installation completed by**: _______________
**Date**: _______________
**Time spent**: _______________
