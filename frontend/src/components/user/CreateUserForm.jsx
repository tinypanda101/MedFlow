
import { useState } from 'react';
import {
  Box, Typography, TextField,
  Select, MenuItem, InputLabel, FormControl, Button, Alert,
} from '@mui/material';
import apiClient from '../../api/client.js';
 
// These values must match the UserRole enum values on the backend
const ROLES = ['Clinical_Admin', 'Field_Technician', 'Auditor'];
 
function CreateUserForm({ onCreated }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState(null); // { severity, message }
 
  async function handleSubmit() {
    // Basic client side checks mirroring the schema (username >=3, password >=8)
    if (username.trim().length < 3) {
      setFeedback({ severity: 'warning', message: 'Username must be at least 3 characters.' });
      return;
    }
    if (password.length < 3) {
      setFeedback({ severity: 'warning', message: 'Password must be at least 3 characters.' });
      return;
    }
    if (!role) {
      setFeedback({ severity: 'warning', message: 'Select a role for the new user.' });
      return;
    }
 
    setSubmitting(true);
    setFeedback(null);
    try {
      await apiClient.post('/auth/register', {
        username: username.trim(),
        password,
        role,
      });
      setFeedback({ severity: 'success', message: `User ${username.trim()} created as ${role}.` });
      // reset the form so the admin can add another
      setUsername('');
      setPassword('');
      setRole('');
      if (onCreated) onCreated();
    } catch (err) {
      // 400 -> username already taken (from the register endpoint)
      if (err.response?.status === 400) {
        setFeedback({ severity: 'error', message: err.response.data.detail || 'Username already taken.' });
      } else if (err.response?.status === 403) {
        setFeedback({ severity: 'error', message: 'You do not have permission to create users.' });
      } else {
        console.error('Create user failed:', err);
        setFeedback({ severity: 'error', message: 'Could not create user.' });
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
        Create New User
      </Typography>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <TextField
          label="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          size="small"
        />
        <TextField
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          size="small"
        />
        <FormControl size="small">
          <InputLabel id="role-label">Role</InputLabel>
          <Select
            labelId="role-label"
            label="Role"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            {ROLES.map((r) => (
              <MenuItem key={r} value={r}>{r}</MenuItem>
            ))}
          </Select>
        </FormControl>
        <Button
          variant="contained"
          onClick={handleSubmit}
          disabled={submitting}
        >
          {submitting ? 'Creating…' : 'Create User'}
        </Button>
        {feedback && <Alert severity={feedback.severity}>{feedback.message}</Alert>}
      </Box>
    </Box>
  );
}
 
export default CreateUserForm;
