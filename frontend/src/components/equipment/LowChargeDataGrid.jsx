
import { useEffect, useState } from 'react';
const LOW_CHARGE_THRESHOLD = 20; // Example threshold value for low charge
import { DataGrid } from '@mui/x-data-grid';
import { Alert, Box, CircularProgress } from '@mui/material';
import apiClient from '../../api/client.js';

//defines our DataGrid columns and maps them to our backend API response data
const columns = [
  { field: 'id', headerName: 'ID', width: 70 },
  { field: 'serial_number', headerName: 'Serial Number', width: 150 },
  { field: 'model', headerName: 'Model', width: 160 },
  { field: 'charge_level', headerName: 'Charge %', width: 120, type: 'number' },
  { field: 'status', headerName: 'Status', width: 130 },
  { field: 'hospital_id', headerName: 'Hospital ID', width: 110, type: 'number' },
];

//local state variables for tracking table rows, loading status, and network errors
//to track the lifecycle of the async API request so the UI can render appropriately
function LowChargeDataGrid() {
  const [equipment, setEquipment] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  //React effect hook that runs our async fetch 
  useEffect(() => {
    //tracks component mount status to prevent memory leaks via network request delays
    let isMounted = true;

    //pulls our robot fleet data from our backend
    async function fetchEquipment() {
      try {
        const response = await apiClient.get('/equipment');
        if (isMounted) {
            const lowCharge = response.data.filter(
                (item) => Number(item.charge_level) < LOW_CHARGE_THRESHOLD
            );
            setEquipment(lowCharge);
        }
      } catch (err) {
        console.error('Equipment fetch failed:', err);
        if (isMounted) setError('Could not load equipment data.');
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    fetchEquipment();

    return () => {
      isMounted = false;
    };
  }, []);

  //shows a spinning progress indicator if loading data
  if (loading) return <CircularProgress />;
  //shows error alert if API call fails
  if (error) return <Alert severity="error">{error}</Alert>;

  //loads data grid component if all goes well
  return (
    <Box sx={{ height: 400, width: '100%' }}>
      <DataGrid rows={equipment} columns={columns} getRowId={(row) => row.id} />
    </Box>
  );
}

export default LowChargeDataGrid;