import {Card, CardContent, Typography, Chip, Stack} from '@mui/material';

const LOW_CHARGE_THRESHOLD = 20; // Example threshold value for low charge

/* 
    EquipmentCard is a React component that takes in Equipment object as a prop (parameter).
    The component uses MUI components to create a acard that displays the equipment's name, status, and charge level.
    It will also visually change colors depending on charge level.
*/

//For now doing what Robopulse looks like if bored later might change it

function EquipmentCard({ equipment }) {
    const isLowCharge = equipment.chargelevel < LOW_CHARGE_THRESHOLD;

    return (
    <Card variant="outlined" sx={{ minWidth: 240 }}>
      <CardContent>
        {/* The Typography component lets us display text with different styles.*/}
        <Typography variant="h6" component="div">
          {equipment.serialNumber}
        </Typography>
        <Typography color="text.secondary" gutterBottom>
          {equipment.model}
        </Typography>
        {/* The Stack component is a layout component that arranges its children in a row or column.*/}
        <Stack direction="row" spacing={1} alignItems="center">
        {/* The Chip component is a small, interactive element that can display information or trigger actions.*/}
          <Chip
            label={`${equipment.chargelevel}% battery`}
            color={isLowCharge ? 'error' : 'success'}
            size="small"
          />
          <Chip label={equipment.status} variant="outlined" size="small" />
        </Stack>
      </CardContent>
    </Card>
  );
}

export default EquipmentCard;