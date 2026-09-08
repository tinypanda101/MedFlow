/*
    UserDataGrid - lists user accounts and lets an admin delete them.
 
    NOTE: the backend currently exposes DELETE /auth/{user_id} but there is no
    "list users" GET endpoint yet. This grid tries GET /auth/users; if that route
    doesn't exist (404) it falls back to a delete-by-ID box so the panel is still
    usable. Add a list endpoint on the backend to populate the table automatically.
*/
 
import { useEffect, useState, useCallback } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import {
  Alert, Box, Button, CircularProgress, TextField, Typography,
} from '@mui/material';
import apiClient from '../../api/client.js';
 
// refreshKey lets the parent force a reload after a new user is created
function UserDataGrid({ refreshKey }) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [listSupported, setListSupported] = useState(true);
  const [deleteId, setDeleteId] = useState('');
  const [feedback, setFeedback] = useState(null); // { severity, message }
 
  const columns = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'username', headerName: 'Username', width: 200 },
    { field: 'role', headerName: 'Role', width: 180 },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 130,
      sortable: false,
      renderCell: (params) => (
        <Button
          color="error"
          size="small"
          onClick={() => handleDelete(params.row.id)}
        >
          Delete
        </Button>
      ),
    },
  ];
 
  const fetchUsers = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get('/auth/users');
      setUsers(response.data);
      setListSupported(true);
    } catch (err) {
      // If there's no list endpoint yet fall back to the delete-by-ID tool
      if (err.response?.status === 404) {
        setListSupported(false);
      } else {
        console.error('User fetch failed:', err);
        setError('Could not load users.');
      }
    } finally {
      setLoading(false);
    }
  }, []);
 
  useEffect(() => {
    fetchUsers();
  }, [fetchUsers, refreshKey]);
 
  async function handleDelete(id) {
    setFeedback(null);
    try {
      await apiClient.delete(`/auth/${id}`);
      setFeedback({ severity: 'success', message: `User ${id} deleted.` });
      setDeleteId('');
      // reload the table if we have a list endpoint
      if (listSupported) fetchUsers();
    } catch (err) {
      if (err.response?.status === 403) {
        setFeedback({ severity: 'error', message: err.response.data.detail || 'Cannot delete this user.' });
      } else if (err.response?.status === 404) {
        setFeedback({ severity: 'error', message: 'User not found.' });
      } else {
        console.error('Delete user failed:', err);
        setFeedback({ severity: 'error', message: 'Could not delete user.' });
      }
    }
  }
 
  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;
 
  // Fallback UI when there's no list endpoint on the backend
  if (!listSupported) {
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
        <Typography variant="h6" gutterBottom>
          Delete User
        </Typography>
        <Alert severity="info" sx={{ mb: 2 }}>
          No user-list endpoint found. Delete by ID below, or add GET /auth/users
          to the backend to see the full table.
        </Alert>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <TextField
            label="User ID"
            type="number"
            value={deleteId}
            onChange={(e) => setDeleteId(e.target.value)}
            size="small"
          />
          <Button
            variant="contained"
            color="error"
            onClick={() => deleteId.trim() && handleDelete(deleteId.trim())}
          >
            Delete
          </Button>
        </Box>
        {feedback && <Alert severity={feedback.severity} sx={{ mt: 2 }}>{feedback.message}</Alert>}
      </Box>
    );
  }
 
  return (
    <Box sx={{ width: '100%' }}>
      {feedback && <Alert severity={feedback.severity} sx={{ mb: 2 }}>{feedback.message}</Alert>}
      <Box sx={{ height: 400, width: '100%' }}>
        <DataGrid rows={users} columns={columns} getRowId={(row) => row.id} />
      </Box>
    </Box>
  );
}
 
export default UserDataGrid;
