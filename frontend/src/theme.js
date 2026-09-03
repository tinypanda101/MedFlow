// Theme configuration for the MedFlow frontend application

// createTheme function is used to create custom themes for materialUI components
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
    palette: {
        mode: 'light',
        primary: {
            main: '#007a99'
        },
        secondary: {
            main: '#000000'
        },
    },
    shape: {
        borderRadius: 8,
    }
});

export default theme;