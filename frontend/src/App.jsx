import {Container, Typography, Box, Snackbar, Alert} from '@mui/material'
import {useState} from 'react';
import AppHeader from './components/layout/AppHeader.jsx'

import LoginForm from './components/auth/LoginForm.jsx';
import EquipmentDataGrid from './components/equipment/EquipmentDataGrid.jsx';
import ActiveTechniciansDataGrid from './components/technician/ReportingLinesDataGrid.jsx';
import { AuthProvider,useAuth } from './context/AuthContext.jsx';
import DiscrepancyDataGrid from './components/work_orders/DiscrepancyDataGrid.jsx'; 
import ReliabilityDataGrid from './components/work_orders/RatioDataGrid.jsx';
import MaintenanceFlagsDataGrid from './components/hospital/MaintenanceFlagsDataGrid.jsx';
import ServiceReportUpload from './components/service_report/ServiceReportUpload.jsx';

// A main dashboard component that renders the application header and data grid to authenticated users
function Dashboard(){
  //store the current user object and logout function from the global AuthContext
  const {user, logout} = useAuth();
  const [notification, setNotification] = useState(null);
  return (
    <>
      <AppHeader username = {user?.sub} role={user?.role} onLogout={logout} />
      <Container maxWidth = 'lg' sx={{mt:4}}>
        <Typography variant='h5' component='h2' gutterBottom>
          Equipment Overview
        </Typography>
        <Box sx ={{mb : 4}}>
          <EquipmentDataGrid />
        </Box>
        <Typography variant = 'h5' component = 'h2' gutterBottom>
          Co-Location Discrepancies
        </Typography>
         <Box sx = {{mb : 4}}>
          <DiscrepancyDataGrid/>
        </Box>
        <Typography variant='h5' component='h2' gutterBottom>
          Reliability Metrics
        </Typography>
        <Box sx={{mb: 4}}>
          <ReliabilityDataGrid />
        </Box>
        <Typography variant='h5' component='h2' gutterBottom>
          Maintenance Flags
        </Typography>
        <Box sx={{mb: 4}}>
          <MaintenanceFlagsDataGrid />
        </Box>
        <Typography variant='h5' component='h2' gutterBottom>
          Active Technicians by Supervisor
        </Typography>
        <Box sx={{mb: 4}}>
          <ActiveTechniciansDataGrid />
        </Box>
        <Typography variant='h5' component='h2' gutterBottom>
          Upload Service Report
        </Typography>
        <Box sx={{ mb: 4 }}>
          <ServiceReportUpload />
        </Box>
      </Container>

      <Snackbar
        open={Boolean(notification)}
        autoHideDuration={4000}
        onClose={() => setNotification(null)}
      >
        <Alert severity="success" onClose = {()=> setNotification(null)}>
        </Alert>

      </Snackbar>
    </>
  )
}

//Conditional layout switcher component that renders either the Dashbaord or the login form
//based on user authentication status tracked in the global AuthContext
function AppContent() {
  const {isAuthenticated} = useAuth();
  return isAuthenticated ? <Dashboard /> : <LoginForm/>;

}

//Now acts as a root application component that wraps the entire app in the AuthProvider context
function App(){
  return (

    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App;