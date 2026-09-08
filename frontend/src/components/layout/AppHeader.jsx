import {AppBar, Toolbar, Typography, Box, Button} from '@mui/material';
import PrecisionManufacturingIcon from '@mui/icons-material/PrecisionManufacturing';

// Every React component must return a single (html) element. In this one, we return an AppBar that acts as a top-level nav bar that contains app title and other nav elements.
// The AppBar is wrapped in a ToolBar to provide proper padding and alignment for its child elements.
// Inside ToolBar we have PrecisionManufacturingIcon and Typography components to display the app icon and title respectively.

//Change out PrecisionManufacturingIcon with a different icon later bc medflow not robopulse

function AppHeader({username,role,onLogout}) {
    return (
        <AppBar position="static">
            <Toolbar>
                <PrecisionManufacturingIcon sx={{ mr: 2 }} />
                <Typography variant="h6" component="h1">
                    MedFlow Clinical Equipment Command Center 
                </Typography>
                {/* Display username and role, and provide a logout button */}
                {username && (
                    <Box sx={{display:'flex', alignItems:'center', gap:2}}>
                        <Typography variant="body2">
                            {username} ({role})
                        </Typography>
                        <Button color="inherit" onClick={onLogout}>
                            Log Out
                        </Button>
                    </Box>
                )}
            </Toolbar>
        </AppBar>
    );
}


// Must have this or it wont load
export default AppHeader;