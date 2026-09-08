
import { useState } from 'react';
import { Container, Typography, Box } from '@mui/material';

import CreateUserForm from '../components/user/CreateUserForm.jsx';
import UserDataGrid from '../components/user/UserDataGrid.jsx';
import CreateEquipmentForm from '../components/equipment/CreateEquipmentForm.jsx';
import CreateHospitalForm from '../components/hospital/CreateHospitalForm.jsx';
import CreateWorkOrderForm from '../components/work_orders/CreateWorkOrderForm.jsx';
import CreateTechnicianForm from '../components/technician/CreateTechnicianForm.jsx';

function AdminPanel() {
  
  const [userRefreshKey, setUserRefreshKey] = useState(0);

  return (
    <Container maxWidth='lg' sx={{ mt: 4 }}>
      <Typography variant='h5' component='h2' gutterBottom color='secondary'>
        User Management
      </Typography>
      <Box sx={{ mb: 4 }}>
        <CreateUserForm onCreated={() => setUserRefreshKey((k) => k + 1)} />
      </Box>
      <Box sx={{ mb: 4 }}>
        <UserDataGrid refreshKey={userRefreshKey} />
      </Box>

      <Typography variant='h5' component='h2' gutterBottom color='secondary'>
        Technician Management
      </Typography>
      <Box sx={{ mb: 4 }}>
        <CreateTechnicianForm />
      </Box>

      <Typography variant='h5' component='h2' gutterBottom color='secondary'>
        Equipment Management
      </Typography>
      <Box sx={{ mb: 4 }}>
        <CreateEquipmentForm />
      </Box>

      <Typography variant='h5' component='h2' gutterBottom color='secondary'>
        Hospital Management
      </Typography>
      <Box sx={{ mb: 4 }}>
        <CreateHospitalForm />
      </Box>

      <Typography variant='h5' component='h2' gutterBottom color='secondary'>
        Work Order Management
      </Typography>
      <Box sx={{ mb: 4 }}>
        <CreateWorkOrderForm />
      </Box>
    </Container>
  );
}

export default AdminPanel;