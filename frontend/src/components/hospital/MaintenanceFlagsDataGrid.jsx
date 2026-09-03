/*
    MaintenanceFlagsDataGrid lists hospitals with >30% of equipment flagged for maintenance.
*/

import { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Alert, Box, CircularProgress } from '@mui/material';
import apiClient from '../../api/client.js';

const HIGH_FLAG_THRESHOLD = 0.30; // highlight hospitals over 30% flagged
const pct = (v) => (v == null ? '—' : `${(v * 100).toFixed(1)}%`);

const columns = [
  { field: 'hospital_name', headerName: 'Hospital Name', width: 200, type: 'string' },
  { field: 'hospital_id', headerName: 'Hospital ID', width: 120, type: 'number' },
  { field: 'total_equipment', headerName: 'Total Equipment', width: 150, type: 'number' },
  { field: 'flagged', headerName: 'Flagged', width: 110, type: 'number' },
  {
    field: 'flagged_ratio',
    headerName: 'Flagged %',
    width: 130,
    type: 'number',
    valueFormatter: (value) => pct(value),
  },
];

function MaintenanceFlagsDataGrid() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function fetchFlags() {
      try {
        const response = await apiClient.get('/hospitals/maintenance');
        if (isMounted) setRows(response.data);
      } catch (err) {
        console.error('Maintenance flags fetch failed:', err);
        if (isMounted) setError('Could not load maintenance flags.');
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    fetchFlags();

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
        '& .high-flag-row': {
          bgcolor: 'warning.light',
          '&:hover': { bgcolor: 'warning.main' },
        },
      }}
    >
      <DataGrid
        rows={rows}
        columns={columns}
        getRowId={(row) => row.hospital_id}
        getRowClassName={(params) =>
          Number(params.row.flagged_ratio) > HIGH_FLAG_THRESHOLD
            ? 'high-flag-row'
            : ''
        }
      />
    </Box>
  );
}

export default MaintenanceFlagsDataGrid;