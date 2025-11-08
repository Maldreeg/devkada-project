import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Meeting APIs
export const uploadMeeting = async (formData) => {
  const response = await api.post('/meetings/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getMeeting = async (meetingId) => {
  const response = await api.get(`/meetings/${meetingId}`);
  return response.data;
};

export const listMeetings = async () => {
  const response = await api.get('/meetings');
  return response.data;
};

export const updateMeetingParticipants = async (meetingId, participants) => {
  const response = await api.post(`/meetings/${meetingId}/update-participants`, participants);
  return response.data;
};

export const sendMeetingSummary = async (meetingId) => {
  const response = await api.post(`/meetings/${meetingId}/send-summary`);
  return response.data;
};

// Participant APIs
export const addParticipant = async (participant) => {
  const response = await api.post('/participants/add', participant);
  return response.data;
};

export const listParticipants = async () => {
  const response = await api.get('/participants');
  return response.data;
};

// Document APIs
export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const listDocuments = async () => {
  const response = await api.get('/documents');
  return response.data;
};

export const searchDocuments = async (query, topK = 5) => {
  const response = await api.post('/documents/search', null, {
    params: { query, top_k: topK },
  });
  return response.data;
};

// Health check
export const healthCheck = async () => {
  const response = await api.get('/');
  return response.data;
};
