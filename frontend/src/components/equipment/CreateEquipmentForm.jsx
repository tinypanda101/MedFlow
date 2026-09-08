
import { useState } from 'react';
import {
  Box, Typography, TextField,
  Select, MenuItem, InputLabel, FormControl, Button, Alert,
} from '@mui/material';
import apiClient from '../../api/client.js';

// Must match the EquipmentStatus enum values
const STATUSES = ['Available', 'In-Use', 'Maintenance', 'Offline'];

function CreateEquipmentForm({ onCreated }) {
  const [serialNumber, setSerialNumber] = useState('');
  const [model, setModel] = useState('');
  const [chargeLevel, setChargeLevel] = useState('');
  const [hospitalId, setHospitalId] = useState('');
  const [status, setStatus] = useState('Available');
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState(null);

  async function handleSubmit() {
    if (!serialNumber.trim() || !model.trim() || chargeLevel === '' || hospitalId === '') {
      setFeedback({ severity: 'warning', message: 'Fill in all fields.' });
      return;
    }
    setSubmitting(true);
    setFeedback(null);
    try {
      await apiClient.post('/equipment', {
        serial_number: serialNumber.trim(),
        model: model.trim(),
        charge_level: Number(chargeLevel),
        hospital_id: Number(hospitalId),
        status,
      });
      setFeedback({ severity: 'success', message: `Equipment ${serialNumber.trim()} created.` });
      setSerialNumber('');
      setModel('');
      setChargeLevel('');
      setHospitalId('');
      setStatus('Available');
      if (onCreated) onCreated();
    } catch (err) {
      console.error('Create equipment failed:', err);
      setFeedback({ severity: 'error', message: err.response?.data?.detail || 'Could not create equipment.' });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Box sx={{ p: 3, border: '1px solid', borderColor: 'divider', borderRadius: 1, maxWidth: 560 }}>
      <Typography variant="h6" align="center" gutterBottom>
        Create Equipment
      </Typography>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <TextField label="Serial Number" value={serialNumber} onChange={(e) => setSerialNumber(e.target.value)} size="small" />
        <TextField label="Model" value={model} onChange={(e) => setModel(e.target.value)} size="small" />
        <TextField label="Charge %" type="number" value={chargeLevel} onChange={(e) => setChargeLevel(e.target.value)} size="small" />
        <TextField label="Hospital ID" type="number" value={hospitalId} onChange={(e) => setHospitalId(e.target.value)} size="small" />
        <FormControl size="small">
          <InputLabel id="eq-status-label">Status</InputLabel>
          <Select labelId="eq-status-label" label="Status" value={status} onChange={(e) => setStatus(e.target.value)}>
            {STATUSES.map((s) => (
              <MenuItem key={s} value={s}>{s}</MenuItem>
            ))}
          </Select>
        </FormControl>
        <Button variant="contained" onClick={handleSubmit} disabled={submitting}>
          {submitting ? 'Creating…' : 'Create Equipment'}
        </Button>
        {feedback && <Alert severity={feedback.severity}>{feedback.message}</Alert>}
      </Box>
    </Box>
  );
}

export default CreateEquipmentForm;