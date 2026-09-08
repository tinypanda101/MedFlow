/*
    CreateWorkOrderForm - Admin form to create a new work order.
    Fields match OrderCreate: title, priority, equipment_id, technician_id.
    (status is intentionally omitted - the model defaults to Pending.)
    POST /orders is already locked to CLINICAL_ADMIN on the backend.
*/

import { useState } from 'react';
import {
  Box, Typography, TextField,
  Select, MenuItem, InputLabel, FormControl, Button, Alert,
} from '@mui/material';
import apiClient from '../../api/client.js';

// Must match the OrderPriority enum values
const PRIORITIES = ['Low', 'Medium', 'Critical'];

function CreateWorkOrderForm({ onCreated }) {
  const [title, setTitle] = useState('');
  const [priority, setPriority] = useState('');
  const [equipmentId, setEquipmentId] = useState('');
  const [technicianId, setTechnicianId] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState(null);

  async function handleSubmit() {
    if (!title.trim() || !priority || equipmentId === '' || technicianId === '') {
      setFeedback({ severity: 'warning', message: 'Fill in all fields.' });
      return;
    }
    setSubmitting(true);
    setFeedback(null);
    try {
      await apiClient.post('/orders', {
        title: title.trim(),
        priority,
        equipment_id: Number(equipmentId),
        technician_id: Number(technicianId),
      });
      setFeedback({ severity: 'success', message: `Work order "${title.trim()}" created.` });
      setTitle('');
      setPriority('');
      setEquipmentId('');
      setTechnicianId('');
      if (onCreated) onCreated();
    } catch (err) {
      console.error('Create work order failed:', err);
      setFeedback({ severity: 'error', message: err.response?.data?.detail || 'Could not create work order.' });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Box sx={{ p: 3, border: '1px solid', borderColor: 'divider', borderRadius: 1, maxWidth: 560 }}>
      <Typography variant="h6" align="center" gutterBottom>
        Create Work Order
      </Typography>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <TextField label="Title" value={title} onChange={(e) => setTitle(e.target.value)} size="small" />
        <FormControl size="small">
          <InputLabel id="wo-priority-label">Priority</InputLabel>
          <Select labelId="wo-priority-label" label="Priority" value={priority} onChange={(e) => setPriority(e.target.value)}>
            {PRIORITIES.map((p) => (
              <MenuItem key={p} value={p}>{p}</MenuItem>
            ))}
          </Select>
        </FormControl>
        <TextField label="Equipment ID" type="number" value={equipmentId} onChange={(e) => setEquipmentId(e.target.value)} size="small" />
        <TextField label="Technician ID" type="number" value={technicianId} onChange={(e) => setTechnicianId(e.target.value)} size="small" />
        <Button variant="contained" onClick={handleSubmit} disabled={submitting}>
          {submitting ? 'Creating…' : 'Create Work Order'}
        </Button>
        {feedback && <Alert severity={feedback.severity}>{feedback.message}</Alert>}
      </Box>
    </Box>
  );
}

export default CreateWorkOrderForm;