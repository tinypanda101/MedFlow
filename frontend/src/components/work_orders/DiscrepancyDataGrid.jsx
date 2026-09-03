import { DataGrid } from '@mui/x-data-grid';
import { useState, useEffect } from 'react';
import {Alert, Box, CircularProgress, TextField, MenuItem} from '@mui/material';
import apiClient from '../../api/client.js';


const columns = [
    { field: 'work_order_id', headerName: 'ID', width: 90 },
    { field: 'title', headerName: 'Title', width: 150 },
    { field: 'equipment_hospital_id', headerName: 'Equipment Hospital ID', width: 150 },
    { field: 'technician_hospital_id', headerName: 'Technician Hospital ID', width: 150 }
];

function DiscrepancyDataGrid() {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedPriority, setSelectedPriority] = useState('');

    useEffect(() => {
        let isMounted = true;

        //pulls from backend
        async function fetchDiscrepancies(){
            try {
                const response = await apiClient.get('/orders/discrepancies', {
                    params: {priority: selectedPriority || undefined},
                });
                if (isMounted) setOrders(response.data);
            } catch {
                if (isMounted) setError("Could not load discrepancy data");
            } finally {
                if (isMounted) setLoading(false);
            }
        }
        fetchDiscrepancies();

        return () => {
            isMounted = false;
        };
    }, [selectedPriority]);

    if (loading) {
        return <CircularProgress />;
    }

    if (error) {
        return <Alert severity="error">{error}</Alert>;
    }

    //loads data grid component
    return (
        <Box sx={{ height: 400, width: '100%' }}>
            <TextField
                select
                label="Priority"
                value={selectedPriority}
                onChange={(e) => setSelectedPriority(e.target.value)}
                sx={{ mb: 2 }}
            >
                <MenuItem value="">All</MenuItem>
                <MenuItem value="Low">Low</MenuItem>
                <MenuItem value="Medium">Medium</MenuItem>
                <MenuItem value="Critical">Critical</MenuItem>
            </TextField>
            <DataGrid
                rows={orders}
                columns={columns}
                pageSize={5}
                rowsPerPageOptions={[5]}
                getRowId={(row) => row.work_order_id}
            />
        </Box>
    );
}

export default DiscrepancyDataGrid;