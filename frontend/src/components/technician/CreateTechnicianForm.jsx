
import { useState } from 'react';
import { Box, Typography, TextField, Button, Alert } from '@mui/material';
import apiClient from '../../api/client.js';

function CreateTechnicianForm({ onCreated }) {
  const [name, setName] = useState('');
  const [hospitalId, setHospitalId] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState(null); 
  async function handleSubmit() {
    if (!name.trim() || hospitalId === '') {
      setFeedback({ severity: 'warning', message: 'Fill in all fields.' });
      return;
    }
    setSubmitting(true);
    setFeedback(null);
    try {
      await apiClient.post('/technician', {
        name: name.trim(),
        hospital_id: Number(hospitalId),
      });
      setFeedback({ severity: 'success', message: `Technician ${name.trim()} created.` });
      setName('');
      setHospitalId('');
      if (onCreated) onCreated();
    } catch (err) {
      console.error('Create technician failed:', err);
      setFeedback({ severity: 'error', message: err.response?.data?.detail || 'Could not create technician.' });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Box sx={{ p: 3, border: '1px solid', borderColor: 'divider', borderRadius: 1, maxWidth: 560 }}>
      <Typography variant="h6" align="center" gutterBottom>
        Create Technician
      </Typography>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <TextField label="Name" value={name} onChange={(e) => setName(e.target.value)} size="small" />
        <TextField label="Hospital ID" type="number" value={hospitalId} onChange={(e) => setHospitalId(e.target.value)} size="small" />
        <Button variant="contained" onClick={handleSubmit} disabled={submitting}>
          {submitting ? 'Creating…' : 'Create Technician'}
        </Button>
        {feedback && <Alert severity={feedback.severity}>{feedback.message}</Alert>}
      </Box>
    </Box>
  );
}

export default CreateTechnicianForm;