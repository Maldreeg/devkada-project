import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Box,
  CircularProgress,
  Alert
} from '@mui/material';
import {
  UploadFile as UploadIcon,
  People as PeopleIcon,
  Description as DocumentIcon,
  TrendingUp as TrendingIcon
} from '@mui/icons-material';
import { listMeetings } from '../services/api';

function HomePage() {
  const [meetings, setMeetings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadMeetings();
  }, []);

  const loadMeetings = async () => {
    try {
      setLoading(true);
      const data = await listMeetings();
      setMeetings(data.meetings || []);
      setError(null);
    } catch (err) {
      setError('Failed to load meetings');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h3" gutterBottom>
        Welcome to ZoomBrain
      </Typography>
      <Typography variant="h6" color="text.secondary" gutterBottom>
        AI-Powered Meeting Summarization with Sentiment Analysis
      </Typography>

      <Grid container spacing={3} sx={{ mt: 3 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <UploadIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
              <Typography variant="h5" gutterBottom>
                Upload Meeting
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Upload your meeting transcripts (VTT, TXT) and get AI-powered summaries with sentiment analysis
              </Typography>
            </CardContent>
            <CardActions>
              <Button size="small" component={Link} to="/upload">
                Get Started
              </Button>
            </CardActions>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <PeopleIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
              <Typography variant="h5" gutterBottom>
                Manage Participants
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Add team members with their roles and emails for better task assignment
              </Typography>
            </CardContent>
            <CardActions>
              <Button size="small" component={Link} to="/participants">
                View Participants
              </Button>
            </CardActions>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <DocumentIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
              <Typography variant="h5" gutterBottom>
                Reference Documents
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Upload reference documents (PDF, PPTX) for context-aware summaries
              </Typography>
            </CardContent>
            <CardActions>
              <Button size="small" component={Link} to="/documents">
                View Documents
              </Button>
            </CardActions>
          </Card>
        </Grid>
      </Grid>

      <Box sx={{ mt: 5 }}>
        <Typography variant="h4" gutterBottom>
          Recent Meetings
        </Typography>

        {loading && <CircularProgress />}
        {error && <Alert severity="error">{error}</Alert>}

        {!loading && !error && meetings.length === 0 && (
          <Alert severity="info">
            No meetings yet. Upload your first meeting to get started!
          </Alert>
        )}

        <Grid container spacing={3} sx={{ mt: 2 }}>
          {meetings.map((meeting) => (
            <Grid item xs={12} md={6} key={meeting.meeting_id}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {meeting.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Date: {new Date(meeting.date).toLocaleDateString()}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Participants: {meeting.participant_count}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button
                    size="small"
                    component={Link}
                    to={`/meeting/${meeting.meeting_id}`}
                  >
                    View Details
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      <Box sx={{ mt: 5, p: 3, bgcolor: 'grey.100', borderRadius: 2 }}>
        <Typography variant="h5" gutterBottom>
          Features
        </Typography>
        <ul>
          <li>
            <Typography variant="body1">
              <strong>Smart Summarization:</strong> Automatic bullet-point or narrative summaries
            </Typography>
          </li>
          <li>
            <Typography variant="body1">
              <strong>Sentiment Analysis:</strong> Track participant engagement and mood
            </Typography>
          </li>
          <li>
            <Typography variant="body1">
              <strong>Task Extraction:</strong> Automatically identify and assign action items
            </Typography>
          </li>
          <li>
            <Typography variant="body1">
              <strong>Email Notifications:</strong> Send summaries and sentiment alerts automatically
            </Typography>
          </li>
          <li>
            <Typography variant="body1">
              <strong>Visual Analytics:</strong> Engagement heatmaps and sentiment charts
            </Typography>
          </li>
        </ul>
      </Box>
    </Box>
  );
}

export default HomePage;
