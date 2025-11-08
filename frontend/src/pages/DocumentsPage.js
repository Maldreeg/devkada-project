import React, { useState, useEffect } from 'react';
import {
  Typography,
  Box,
  Paper,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress,
  Alert,
  TextField,
  Grid
} from '@mui/material';
import { CloudUpload as UploadIcon, Search as SearchIcon } from '@mui/icons-material';
import { uploadDocument, listDocuments, searchDocuments } from '../services/api';

function DocumentsPage() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      setLoading(true);
      const data = await listDocuments();
      setDocuments(data.documents || []);
      setError(null);
    } catch (err) {
      setError('Failed to load documents');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      setUploading(true);
      setError(null);
      await uploadDocument(file);
      setSuccess(`Document "${file.name}" uploaded successfully!`);
      setTimeout(() => setSuccess(null), 5000);
      loadDocuments();
    } catch (err) {
      setError('Failed to upload document');
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    try {
      setLoading(true);
      const results = await searchDocuments(searchQuery, 5);
      setSearchResults(results);
      setError(null);
    } catch (err) {
      setError('Failed to search documents');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">
          Reference Documents
        </Typography>
        <Button
          variant="contained"
          component="label"
          startIcon={uploading ? <CircularProgress size={20} /> : <UploadIcon />}
          disabled={uploading}
        >
          Upload Document
          <input
            type="file"
            hidden
            accept=".pdf,.pptx,.txt,.md"
            onChange={handleFileUpload}
          />
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      {/* Search Section */}
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Search Documents
        </Typography>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={9}>
            <TextField
              fullWidth
              label="Search query"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="e.g., What are the quarterly goals?"
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <Button
              variant="contained"
              fullWidth
              startIcon={<SearchIcon />}
              onClick={handleSearch}
              disabled={!searchQuery.trim()}
            >
              Search
            </Button>
          </Grid>
        </Grid>

        {searchResults && (
          <Box mt={3}>
            <Typography variant="subtitle1" gutterBottom>
              Search Results:
            </Typography>
            {searchResults.results && searchResults.results.length > 0 ? (
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Document</TableCell>
                      <TableCell>Preview</TableCell>
                      <TableCell>Distance</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {searchResults.results.map((result, index) => (
                      <TableRow key={index}>
                        <TableCell>{result.filename || 'Unknown'}</TableCell>
                        <TableCell>{result.text_preview?.substring(0, 100) || '-'}</TableCell>
                        <TableCell>{result.distance?.toFixed(2) || '-'}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            ) : (
              <Alert severity="info">No results found</Alert>
            )}
          </Box>
        )}
      </Paper>

      {/* Documents List */}
      <Paper elevation={3}>
        <Box p={2}>
          <Typography variant="h6" gutterBottom>
            All Documents ({documents.length})
          </Typography>
        </Box>

        {loading ? (
          <Box display="flex" justifyContent="center" p={4}>
            <CircularProgress />
          </Box>
        ) : documents.length === 0 ? (
          <Box p={4}>
            <Alert severity="info">
              No documents yet. Upload reference documents (PDF, PPTX, TXT) to enhance context-aware summaries.
            </Alert>
          </Box>
        ) : (
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell><strong>Filename</strong></TableCell>
                  <TableCell><strong>Type</strong></TableCell>
                  <TableCell><strong>Upload Date</strong></TableCell>
                  <TableCell><strong>Preview</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {documents.map((doc, index) => (
                  <TableRow key={index}>
                    <TableCell>{doc.filename}</TableCell>
                    <TableCell>{doc.file_type}</TableCell>
                    <TableCell>
                      {new Date(doc.upload_date).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2" noWrap sx={{ maxWidth: 300 }}>
                        {doc.text_preview || '-'}
                      </Typography>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>

      {/* Info Box */}
      <Paper elevation={2} sx={{ p: 3, mt: 3, bgcolor: 'info.light' }}>
        <Typography variant="h6" gutterBottom>
          About Reference Documents
        </Typography>
        <Typography variant="body2" paragraph>
          Upload reference documents to provide context for meeting summaries:
        </Typography>
        <ul>
          <li>
            <Typography variant="body2">
              <strong>PDFs:</strong> Company policies, project documentation, reports
            </Typography>
          </li>
          <li>
            <Typography variant="body2">
              <strong>PowerPoint:</strong> Presentation slides shared during meetings
            </Typography>
          </li>
          <li>
            <Typography variant="body2">
              <strong>Text files:</strong> Meeting agendas, notes, specifications
            </Typography>
          </li>
        </ul>
        <Typography variant="body2">
          These documents are indexed using AI embeddings for semantic search and context-aware summarization.
        </Typography>
      </Paper>
    </Box>
  );
}

export default DocumentsPage;
