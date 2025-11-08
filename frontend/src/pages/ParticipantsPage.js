import React, { useState, useEffect } from 'react';
import {
  Typography,
  Box,
  Paper,
  Grid,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  Alert
} from '@mui/material';
import { PersonAdd as PersonAddIcon } from '@mui/icons-material';
import { addParticipant, listParticipants } from '../services/api';

function ParticipantsPage() {
  const [participants, setParticipants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    role: '',
    email: '',
    team: ''
  });

  useEffect(() => {
    loadParticipants();
  }, []);

  const loadParticipants = async () => {
    try {
      setLoading(true);
      const data = await listParticipants();
      setParticipants(data.participants || []);
      setError(null);
    } catch (err) {
      setError('Failed to load participants');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDialog = () => {
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setFormData({ name: '', role: '', email: '', team: '' });
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    try {
      await addParticipant(formData);
      handleCloseDialog();
      loadParticipants();
    } catch (err) {
      setError('Failed to add participant');
      console.error(err);
    }
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">
          Manage Participants
        </Typography>
        <Button
          variant="contained"
          startIcon={<PersonAddIcon />}
          onClick={handleOpenDialog}
        >
          Add Participant
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Paper elevation={3}>
        {loading ? (
          <Box display="flex" justifyContent="center" p={4}>
            <CircularProgress />
          </Box>
        ) : participants.length === 0 ? (
          <Box p={4}>
            <Alert severity="info">
              No participants yet. Add participants to track their roles and enable email notifications.
            </Alert>
          </Box>
        ) : (
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell><strong>Name</strong></TableCell>
                  <TableCell><strong>Role</strong></TableCell>
                  <TableCell><strong>Email</strong></TableCell>
                  <TableCell><strong>Team</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {participants.map((participant, index) => (
                  <TableRow key={index}>
                    <TableCell>{participant.name}</TableCell>
                    <TableCell>{participant.role || '-'}</TableCell>
                    <TableCell>{participant.email || '-'}</TableCell>
                    <TableCell>{participant.team || '-'}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>

      {/* Add Participant Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <form onSubmit={handleSubmit}>
          <DialogTitle>Add New Participant</DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  label="Name"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                  fullWidth
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Role/Position"
                  name="role"
                  value={formData.role}
                  onChange={handleInputChange}
                  fullWidth
                  placeholder="e.g., Product Manager, Developer"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  fullWidth
                  placeholder="user@example.com"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Team"
                  name="team"
                  value={formData.team}
                  onChange={handleInputChange}
                  fullWidth
                  placeholder="e.g., Engineering, Marketing"
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>Cancel</Button>
            <Button type="submit" variant="contained" disabled={!formData.name}>
              Add Participant
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      {/* Info Box */}
      <Paper elevation={2} sx={{ p: 3, mt: 3, bgcolor: 'info.light' }}>
        <Typography variant="h6" gutterBottom>
          About Participants
        </Typography>
        <Typography variant="body2" paragraph>
          Add team members here to enable:
        </Typography>
        <ul>
          <li>
            <Typography variant="body2">
              <strong>Automatic task assignment:</strong> The system will recognize participants in transcripts
            </Typography>
          </li>
          <li>
            <Typography variant="body2">
              <strong>Email notifications:</strong> Receive meeting summaries and sentiment alerts
            </Typography>
          </li>
          <li>
            <Typography variant="body2">
              <strong>Role-based analysis:</strong> Better context for task assignment based on roles
            </Typography>
          </li>
        </ul>
      </Paper>
    </Box>
  );
}

export default ParticipantsPage;
