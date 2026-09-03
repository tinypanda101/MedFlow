import {Grid} from '@mui/material';
import EquipmentCard from './EquipmentCard.jsx';

function EquipmentList({equipment}) {
    return (
        <Grid container spacing = {2}>
            {/* Map function is used to iterate over 'equipment' array and render a card component for each equipment item*/}
            {equipment.map((item)=> 
            <Grid item key = {item.id}>
                <EquipmentCard equipment={item} />
            </Grid>
        )}
        </Grid>
    );
}

export default EquipmentList;