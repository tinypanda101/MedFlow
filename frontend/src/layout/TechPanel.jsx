import { Container, Typography, Box } from "@mui/material";
import EquipmentDataGrid from '../components/equipment/EquipmentDataGrid.jsx';
import ServiceReportUpload from '../components/service_report/ServiceReportUpload.jsx';
import OrderStatusChange from '../components/work_orders/OrderStatusChange.jsx';


function TechPanel() {
  return (
    <Container maxWidth = 'lg' sx={{mt:4}}>
        <Typography variant='h5' component='h2' gutterBottom color = 'secondary'>
          Equipment Overview
        </Typography>
        <Box sx ={{mb : 4}}>
          <EquipmentDataGrid />
        </Box>
        <Typography variant='h5' component='h2' gutterBottom color = 'secondary'>
          Upload Service Report
        </Typography>
        <Box sx={{ mb: 4 }}>
          <ServiceReportUpload />
        </Box>
        <Typography variant='h5' component='h2' gutterBottom color = 'secondary'>
          Status Change for Work Orders
        </Typography>
        <Box sx={{ mb: 4 }}>
          <OrderStatusChange />
        </Box>
    </Container>
    )
}

export default TechPanel;
