// Answers question 3

import { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Alert, Box, CircularProgress } from '@mui/material';
import apiClient from '../../api/client.js';

const HIGH_FAILURE_THRESHOLD = 0.25; // flag models failing >25% of resolved orders

const pct = (v) => (v == null ? '—' : `${(v * 100).toFixed(1)}%`);

const columns = [
  { field: 'model', headerName: 'Model', width: 180 },
  { field: 'total', headerName: 'Total Orders', width: 120, type: 'number' },
  { field: 'completed', headerName: 'Completed', width: 120, type: 'number' },
  { field: 'failed', headerName: 'Failed', width: 100, type: 'number' },
  { field: 'pending', headerName: 'Pending', width: 100, type: 'number' },
  { field: 'in_progress', headerName: 'In Progress', width: 120, type: 'number' },
  {
    field: 'completion_ratio',
    headerName: 'Completion %',
    width: 140,
    type: 'number',
    valueFormatter: (value) => pct(value),
  },
  {
    field: 'failure_ratio',
    headerName: 'Failure %',
    width: 120,
    type: 'number',
    valueFormatter: (value) => pct(value),
  },
];

function ReliabilityDataGrid() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function fetchRatios() {
      try {
        const response = await apiClient.get('/orders/ratios');
        if (isMounted) setRows(response.data);
      } catch (err) {
        console.error('Reliability metrics fetch failed:', err);
        if (isMounted) setError('Could not load reliability metrics.');
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    fetchRatios();

    return () => {
      isMounted = false;
    };
  }, []);

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <Box
      sx={{
        height: 400,
        width: '100%',
        '& .high-failure-row': {
          bgcolor: 'error.light',
          '&:hover': { bgcolor: 'error.main' },
        },
      }}
    >
      <DataGrid
        rows={rows}
        columns={columns}
        getRowId={(row) => row.model}
        getRowClassName={(params) =>
          params.row.failure_ratio != null &&
          Number(params.row.failure_ratio) > HIGH_FAILURE_THRESHOLD
            ? 'high-failure-row'
            : ''
        }
      />
    </Box>
  );
}

export default ReliabilityDataGrid;