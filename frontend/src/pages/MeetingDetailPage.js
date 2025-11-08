import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Typography,
  Box,
  Paper,
  Grid,
  Chip,
  CircularProgress,
  Alert,
  Button,
  Card,
  CardContent,
  Divider,
  List,
  ListItem,
  ListItemText
} from '@mui/material';
import {
  Send as SendIcon,
  Person as PersonIcon,
  Assignment as AssignmentIcon,
  SentimentSatisfied as HappyIcon,
  SentimentNeutral as NeutralIcon,
  SentimentDissatisfied as SadIcon
} from '@mui/icons-material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import { getMeeting, sendMeetingSummary } from '../services/api';

function MeetingDetailPage() {
  const { meetingId } = useParams();
  const [meeting, setMeeting] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sendingEmail, setSendingEmail] = useState(false);
  const [emailSuccess, setEmailSuccess] = useState(false);

  useEffect(() => {
    loadMeeting();
  }, [meetingId]);

  const loadMeeting = async () => {
    try {
      setLoading(true);
      const data = await getMeeting(meetingId);
      setMeeting(data);
      setError(null);
    } catch (err) {
      setError('Failed to load meeting details');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSendEmail = async () => {
    try {
      setSendingEmail(true);
      await sendMeetingSummary(meetingId);
      setEmailSuccess(true);
      setTimeout(() => setEmailSuccess(false), 5000);
    } catch (err) {
      console.error(err);
      alert('Failed to send email. Make sure email settings are configured.');
    } finally {
      setSendingEmail(false);
    }
  };

  const getSentimentIcon = (classification) => {
    switch (classification) {
      case 'positive':
        return <HappyIcon color="success" />;
      case 'negative':
        return <SadIcon color="error" />;
      default:
        return <NeutralIcon color="action" />;
    }
  };

  const getSentimentColor = (score) => {
    if (score >= 20) return 'success';
    if (score <= -20) return 'error';
    return 'default';
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error || !meeting) {
    return <Alert severity="error">{error || 'Meeting not found'}</Alert>;
  }

  // Prepare data for charts
  const sentimentChartData = Object.entries(meeting.sentiment_data || {}).map(([name, data]) => ({
    name,
    score: data.sentiment_score
  }));

  const engagementChartData = meeting.engagement_heatmap || [];

  return (
    <Box>
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" gutterBottom>
            {meeting.title}
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            {new Date(meeting.date).toLocaleDateString('en-US', {
              weekday: 'long',
              year: 'numeric',
              month: 'long',
              day: 'numeric'
            })}
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={sendingEmail ? <CircularProgress size={20} /> : <SendIcon />}
          onClick={handleSendEmail}
          disabled={sendingEmail}
        >
          Send Summary via Email
        </Button>
      </Box>

      {emailSuccess && (
        <Alert severity="success" sx={{ mb: 2 }}>
          Meeting summary sent successfully!
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Summary Section */}
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Meeting Summary
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Typography variant="body1" style={{ whiteSpace: 'pre-wrap' }}>
              {meeting.summary}
            </Typography>
          </Paper>
        </Grid>

        {/* Action Items */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <AssignmentIcon sx={{ mr: 1 }} color="primary" />
                <Typography variant="h6">Action Items</Typography>
              </Box>
              <List>
                {meeting.action_items && meeting.action_items.length > 0 ? (
                  meeting.action_items.map((item, index) => (
                    <ListItem key={index} divider>
                      <ListItemText
                        primary={item.extracted_action || item.text}
                        secondary={`Assigned to: ${item.assigned_to?.join(', ') || 'Unassigned'}`}
                      />
                    </ListItem>
                  ))
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    No specific action items identified
                  </Typography>
                )}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Participants */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <PersonIcon sx={{ mr: 1 }} color="primary" />
                <Typography variant="h6">Participants</Typography>
              </Box>
              <List>
                {Object.entries(meeting.participants || {}).map(([name, data]) => (
                  <ListItem key={name} divider>
                    <ListItemText
                      primary={name}
                      secondary={`${data.speaking_count} contributions | ${data.total_words} words`}
                    />
                    {meeting.sentiment_data && meeting.sentiment_data[name] && (
                      <Box display="flex" alignItems="center">
                        {getSentimentIcon(meeting.sentiment_data[name].classification)}
                        <Chip
                          label={`${meeting.sentiment_data[name].sentiment_score.toFixed(1)}`}
                          size="small"
                          color={getSentimentColor(meeting.sentiment_data[name].sentiment_score)}
                          sx={{ ml: 1 }}
                        />
                      </Box>
                    )}
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Sentiment Analysis Chart */}
        {sentimentChartData.length > 0 && (
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Participant Sentiment Analysis
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={sentimentChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis domain={[-100, 100]} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="score" fill="#8884d8" name="Sentiment Score" />
                </BarChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>
        )}

        {/* Engagement Heatmap */}
        {engagementChartData.length > 0 && (
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Engagement Over Time
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={engagementChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="window" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="engagement_score" stroke="#8884d8" name="Engagement" />
                  <Line type="monotone" dataKey="speaker_count" stroke="#82ca9d" name="Active Speakers" />
                </LineChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>
        )}

        {/* Detected Dates */}
        {meeting.detected_dates && meeting.detected_dates.length > 0 && (
          <Grid item xs={12}>
            <Paper elevation={2} sx={{ p: 2, bgcolor: 'info.light' }}>
              <Typography variant="h6" gutterBottom>
                Detected Dates
              </Typography>
              <Box>
                {meeting.detected_dates.map((date, index) => (
                  <Chip key={index} label={date} sx={{ mr: 1, mb: 1 }} />
                ))}
              </Box>
            </Paper>
          </Grid>
        )}
      </Grid>
    </Box>
  );
}

export default MeetingDetailPage;
