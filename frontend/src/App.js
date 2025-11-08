import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Button,
  CssBaseline,
  ThemeProvider,
  createTheme
} from '@mui/material';
import { Psychology as BrainIcon } from '@mui/icons-material';
import HomePage from './pages/HomePage';
import UploadPage from './pages/UploadPage';
import MeetingDetailPage from './pages/MeetingDetailPage';
import ParticipantsPage from './pages/ParticipantsPage';
import DocumentsPage from './pages/DocumentsPage';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar>
              <BrainIcon sx={{ mr: 2 }} />
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                ZoomBrain - AI Meeting Summarizer
              </Typography>
              <Button color="inherit" component={Link} to="/">
                Home
              </Button>
              <Button color="inherit" component={Link} to="/upload">
                Upload Meeting
              </Button>
              <Button color="inherit" component={Link} to="/participants">
                Participants
              </Button>
              <Button color="inherit" component={Link} to="/documents">
                Documents
              </Button>
            </Toolbar>
          </AppBar>

          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/upload" element={<UploadPage />} />
              <Route path="/meeting/:meetingId" element={<MeetingDetailPage />} />
              <Route path="/participants" element={<ParticipantsPage />} />
              <Route path="/documents" element={<DocumentsPage />} />
            </Routes>
          </Container>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
