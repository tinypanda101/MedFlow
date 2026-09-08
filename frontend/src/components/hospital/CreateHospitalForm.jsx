

import { useState } from 'react';
import { Box, Typography, TextField, Button, Alert } from '@mui/material';
import apiClient from '../../api/client.js';

function CreateHospitalForm({ onCreated }) {
  const [name, setName] = useState('');
  const [region, setRegion] = useState('');
  const [capacity, setCapacity] = useState('');
  const [supervisorId, setSupervisorId] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState(null);

  async function handleSubmit() {
    if (!name.trim() || !region.trim() || capacity === '' || supervisorId === '') {
      setFeedback({ severity: 'warning', message: 'Fill in all fields.' });
      return;
    }
    setSubmitting(true);
    setFeedback(null);
    try {
      await apiClient.post('/hospitals', {
        name: name.trim(),
        location_region: region.trim(),
        capacity: Number(capacity),
        supervisor_id: Number(supervisorId),
      });
      setFeedback({ severity: 'success', message: `Hospital ${name.trim()} created.` });
      setName('');
      setRegion('');
      setCapacity('');
      setSupervisorId('');
      if (onCreated) onCreated();
    } catch (err) {
      console.error('Create hospital failed:', err);
      setFeedback({ severity: 'error', message: err.response?.data?.detail || 'Could not create hospital.' });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Box sx={{ p: 3, border: '1px solid', borderColor: 'divider', borderRadius: 1, maxWidth: 560 }}>
      <Typography variant="h6" align="center" gutterBottom>
        Create Hospital
      </Typography>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <TextField label="Name" value={name} onChange={(e) => setName(e.target.value)} size="small" />
        <TextField label="Location Region" value={region} onChange={(e) => setRegion(e.target.value)} size="small" />
        <TextField label="Capacity" type="number" value={capacity} onChange={(e) => setCapacity(e.target.value)} size="small" />
        <TextField label="Supervisor ID" type="number" value={supervisorId} onChange={(e) => setSupervisorId(e.target.value)} size="small" />
        <Button variant="contained" onClick={handleSubmit} disabled={submitting}>
          {submitting ? 'Creating…' : 'Create Hospital'}
        </Button>
        {feedback && <Alert severity={feedback.severity}>{feedback.message}</Alert>}
      </Box>
    </Box>
  );
}

export default CreateHospitalForm;