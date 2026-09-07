
import { useState } from 'react';
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import apiClient from '../../api/client.js';
import { useAuth } from '../../context/AuthContext.jsx';

const UPLOAD_ROLES = ['Clinical_Admin', 'Field_Technician'];

function ServiceReportUpload({ onUploaded }) {
  const { user } = useAuth();

  const [workOrderId, setWorkOrderId] = useState('');
  const [notes, setNotes] = useState('');
  const [file, setFile] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);


  if (!user || !UPLOAD_ROLES.includes(user.role)) {
    return null;
  }

  const canSubmit = workOrderId !== '' && file !== null && !submitting;

  const handleSubmit = async () => {
    setError(null);
    setSuccess(null);

    // Build multipart body. Field names must match the FastAPI Form(...) params:
    // work_order_id, file, notes.
    const formData = new FormData();
    formData.append('work_order_id', workOrderId);
    formData.append('file', file);
    if (notes) formData.append('notes', notes);

    setSubmitting(true);
    try {
      const response = await apiClient.post('/reports', formData);
      setSuccess(`Report uploaded. Stored at ${response.data.file_url}`);
      setWorkOrderId('');
      setNotes('');
      setFile(null);
      
      if (onUploaded) onUploaded(response.data);
    } catch (err) {
      
      const detail = err.response?.data?.detail;
      setError(detail || 'Upload failed. Check the work order ID and file type.');
    } finally {
      setSubmitting(false);
    }
  };

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
      <Typography variant="h6" component="h3" gutterBottom>
        Attach Service Report
      </Typography>

      <Stack spacing={2}>
        <TextField
          label="Work Order ID"
          type="number"
          value={workOrderId}
          onChange={(e) => setWorkOrderId(e.target.value)}
          size="small"
          fullWidth
        />

        <TextField
          label="Notes"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          size="small"
          multiline
          minRows={2}
          fullWidth
        />

        <Button variant="outlined" component="label">
          {file ? file.name : 'Choose file (.txt, .pdf, image)'}
          <input
            type="file"
            hidden
            accept=".txt,.pdf,image/png,image/jpeg"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          />
        </Button>

        <Button
          variant="contained"
          onClick={handleSubmit}
          disabled={!canSubmit}
        >
          {submitting ? <CircularProgress size={22} /> : 'Upload report'}
        </Button>

        {error && <Alert severity="error">{error}</Alert>}
        {success && <Alert severity="success">{success}</Alert>}
      </Stack>
    </Box>
  );
}

export default ServiceReportUpload;
