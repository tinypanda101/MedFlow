import { useState } from 'react';
import {
  Box, Card, CardContent, Typography, TextField,
  Select, MenuItem, InputLabel, FormControl, Button, Alert,
} from '@mui/material';
import apiClient from '../../api/client.js';

const STATUSES = ['Pending', 'In-Progress', 'Completed', 'Failed'];

function WorkOrderStatusChange() {
  const [workOrderId, setWorkOrderId] = useState('');
  const [status, setStatus] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState(null); // { severity, message }

  async function handleSubmit() {
    if (!workOrderId.trim() || !status) {
      setFeedback({ severity: 'warning', message: 'Enter a Work Order ID and select a status.' });
      return;
    }
    setSubmitting(true);
    setFeedback(null);
    try {
      await apiClient.patch(
        `/orders/${workOrderId.trim()}/status`,
        { status }
    );
      setFeedback({ severity: 'success', message: `Work order ${workOrderId.trim()} set to ${status}.` });
    } catch (err) {
      if (err.response?.status === 404) {
        setFeedback({ severity: 'error', message: 'Work order not found.' });
      } else {
        console.error('Status update failed:', err);
        setFeedback({ severity: 'error', message: 'Could not update work order status.' });
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
   <Box
      sx={{
        p: 3,
        border: '1px solid',
        borderColor: 'divider',
        borderRadius: 1,
        maxWidth: 560,
      }}
    >
        <Typography variant="h6" align="center" gutterBottom>
          Change Work Order Status
        </Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Work Order ID"
            value={workOrderId}
            onChange={(e) => setWorkOrderId(e.target.value)}
            size="small"
          />
          <FormControl size="small">
            <InputLabel id="status-label">New Status</InputLabel>
            <Select
              labelId="status-label"
              label="New Status"
              value={status}
              onChange={(e) => setStatus(e.target.value)}
            >
              {STATUSES.map((s) => (
                <MenuItem key={s} value={s}>{s}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <Button
            variant="contained"
            onClick={handleSubmit}
            disabled={submitting}
          >
            {submitting ? 'Updating…' : 'Update Status'}
          </Button>
          {feedback && <Alert severity={feedback.severity}>{feedback.message}</Alert>}
        </Box>
      </Box>
  );
}

export default WorkOrderStatusChange;