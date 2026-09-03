import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import {ThemeProvider, CssBaseline} from '@mui/material';
import theme from './theme'; 



createRoot(document.getElementById('root')).render(
  <StrictMode>
    {// ThemeProvider is a component that allows you to apply the custom themes
    }
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </StrictMode>,
)
