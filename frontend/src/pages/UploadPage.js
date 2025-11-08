import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Typography,
  Box,
  Paper,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert,
  LinearProgress
} from '@mui/material';
import { CloudUpload as UploadIcon } from '@mui/icons-material';
import { uploadMeeting } from '../services/api';

function UploadPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [meetingTitle, setMeetingTitle] = useState('');
  const [meetingDate, setMeetingDate] = useState('');
  const [summaryStyle, setSummaryStyle] = useState('bullet_points');
  const [detailLevel, setDetailLevel] = useState('medium');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      // Auto-populate meeting title from filename if empty
      if (!meetingTitle) {
        const fileName = selectedFile.name.replace(/\.[^/.]+$/, '');
        setMeetingTitle(fileName);
      }
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    if (!meetingTitle) {
      setError('Please enter a meeting title');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setSuccess(false);

      const formData = new FormData();
      formData.append('file', file);
      formData.append('meeting_title', meetingTitle);
      if (meetingDate) {
        formData.append('meeting_date', meetingDate);
      }
      formData.append('summary_style', summaryStyle);
      formData.append('detail_level', detailLevel);

      const response = await uploadMeeting(formData);
      
      setSuccess(true);
      setError(null);

      // Redirect to meeting detail page after 2 seconds
      setTimeout(() => {
        navigate(`/meeting/${response.meeting_id}`);
      }, 2000);

    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload meeting');
      setSuccess(false);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Upload Meeting Transcript
      </Typography>

      <Paper elevation={3} sx={{ p: 4, mt: 3 }}>
        <form onSubmit={handleSubmit}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            {/* File Upload */}
            <Box>
              <Button
                variant="outlined"
                component="label"
                startIcon={<UploadIcon />}
                fullWidth
                sx={{ p: 2, borderStyle: 'dashed' }}
              >
                {file ? file.name : 'Choose Transcript File (VTT, TXT)'}
                <input
                  type="file"
                  hidden
                  accept=".vtt,.txt,.md"
                  onChange={handleFileChange}
                />
              </Button>
              <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                Supported formats: VTT (WebVTT), TXT (plain text transcripts)
              </Typography>
            </Box>

            {/* Meeting Title */}
            <TextField
              label="Meeting Title"
              value={meetingTitle}
              onChange={(e) => setMeetingTitle(e.target.value)}
              required
              fullWidth
              placeholder="e.g., Weekly Team Standup - Nov 8, 2025"
            />

            {/* Meeting Date */}
            <TextField
              label="Meeting Date"
              type="date"
              value={meetingDate}
              onChange={(e) => setMeetingDate(e.target.value)}
              fullWidth
              InputLabelProps={{ shrink: true }}
            />

            {/* Summary Style */}
            <FormControl fullWidth>
              <InputLabel>Summary Style</InputLabel>
              <Select
                value={summaryStyle}
                label="Summary Style"
                onChange={(e) => setSummaryStyle(e.target.value)}
              >
                <MenuItem value="bullet_points">Bullet Points</MenuItem>
                <MenuItem value="narrative">Narrative</MenuItem>
                <MenuItem value="executive">Executive Summary</MenuItem>
              </Select>
            </FormControl>

            {/* Detail Level */}
            <FormControl fullWidth>
              <InputLabel>Detail Level</InputLabel>
              <Select
                value={detailLevel}
                label="Detail Level"
                onChange={(e) => setDetailLevel(e.target.value)}
              >
                <MenuItem value="brief">Brief</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="detailed">Detailed</MenuItem>
              </Select>
            </FormControl>

            {/* Error Alert */}
            {error && (
              <Alert severity="error" onClose={() => setError(null)}>
                {error}
              </Alert>
            )}

            {/* Success Alert */}
            {success && (
              <Alert severity="success">
                Meeting uploaded successfully! Redirecting to summary...
              </Alert>
            )}

            {/* Loading Progress */}
            {loading && <LinearProgress />}

            {/* Submit Button */}
            <Button
              type="submit"
              variant="contained"
              size="large"
              disabled={loading || !file || !meetingTitle}
              fullWidth
            >
              {loading ? <CircularProgress size={24} /> : 'Process Meeting'}
            </Button>
          </Box>
        </form>
      </Paper>

      {/* Instructions */}
      <Paper elevation={2} sx={{ p: 3, mt: 3, bgcolor: 'info.light' }}>
        <Typography variant="h6" gutterBottom>
          Instructions
        </Typography>
        <Typography variant="body2" paragraph>
          1. Upload your meeting transcript in VTT or TXT format
        </Typography>
        <Typography variant="body2" paragraph>
          2. For VTT files, speaker names should be in the format: "Speaker Name: text"
        </Typography>
        <Typography variant="body2" paragraph>
          3. Choose your preferred summary style and detail level
        </Typography>
        <Typography variant="body2">
          4. The system will automatically extract action items, analyze sentiment, and identify participants
        </Typography>
      </Paper>
    </Box>
  );
}

export default UploadPage;
