import { Container, Typography, Box } from "@mui/material";
import LowChargeDataGrid from '../components/equipment/LowChargeDataGrid.jsx';
import ActiveTechniciansDataGrid from '../components/technician/ReportingLinesDataGrid.jsx';
import DiscrepancyDataGrid from '../components/work_orders/DiscrepancyDataGrid.jsx'; 
import ReliabilityDataGrid from '../components/work_orders/RatioDataGrid.jsx';
import MaintenanceFlagsDataGrid from '../components/hospital/MaintenanceFlagsDataGrid.jsx';


function Overview() {
    return (
         <Container maxWidth = 'lg' sx={{mt:4}}>
        <Typography variant='h5' component='h2' gutterBottom color = 'secondary'>
          Low Charge Equipment
        </Typography>
        <Box sx ={{mb : 4}}>
          <LowChargeDataGrid/>
        </Box>
        <Typography variant = 'h5' component = 'h2' gutterBottom color = 'secondary'>
          Co-Location Discrepancies
        </Typography>
         <Box sx = {{mb : 4}}>
          <DiscrepancyDataGrid/>
        </Box>
        <Typography variant='h5' component='h2' gutterBottom color = 'secondary'>
          Reliability Metrics
        </Typography>
        <Box sx={{mb: 4}}>
          <ReliabilityDataGrid />
        </Box>
        <Typography variant='h5' component='h2' gutterBottom color = 'secondary'>
          Maintenance Flags
        </Typography>
        <Box sx={{mb: 4}}>
          <MaintenanceFlagsDataGrid />
        </Box>
        <Typography variant='h5' component='h2' gutterBottom color = 'secondary'>
          Active Technicians by Supervisor
        </Typography>
        <Box sx={{mb: 4}}>
          <ActiveTechniciansDataGrid />
        </Box>
        
      </Container>

    )
}

export default Overview;