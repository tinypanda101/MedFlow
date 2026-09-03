/*
    ActiveTechniciansDataGrid shows, per Regional Biomed Supervisor, how many
    of their technicians have active work orders assigned.
*/

import { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Alert, Box, CircularProgress } from '@mui/material';
import apiClient from '../../api/client.js';

const columns = [
  { field: 'supervisor_id', headerName: 'Supervisor ID', width: 140, type: 'number' },
  {
    field: 'active_technician_count',
    headerName: 'Technicians w/ Active Orders',
    width: 240,
    type: 'number',
  },
];

function ActiveTechniciansDataGrid() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function fetchData() {
      try {
        const response = await apiClient.get('/technician/active');
        if (isMounted) setRows(response.data);
      } catch (err) {
        console.error('Active technicians fetch failed:', err);
        if (isMounted) setError('Could not load active technician counts.');
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    fetchData();

    return () => {
      isMounted = false;
    };
  }, []);

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <Box sx={{ height: 400, width: '100%' }}>
      <DataGrid
        rows={rows}
        columns={columns}
        getRowId={(row) => row.supervisor_id}
      />
    </Box>
  );
}

export default ActiveTechniciansDataGrid;