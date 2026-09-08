import {Container, Typography, Box, Snackbar, Alert, Tabs, Tab} from '@mui/material'
import {useState} from 'react';
import AppHeader from './components/layout/AppHeader.jsx'

import LoginForm from './components/auth/LoginForm.jsx';
import { AuthProvider,useAuth } from './context/AuthContext.jsx';
import Overview from './layout/Overview.jsx';
import TechPanel from './layout/TechPanel.jsx';
import AdminPanel from './layout/AdminPanel.jsx';
// A main dashboard component that renders the application header and data grid to authenticated users
function Dashboard(){
  //store the current user object and logout function from the global AuthContext
  const {user, logout} = useAuth();
  const isAdmin = user?.role === 'Clinical_Admin';
  const [activeTab, setActiveTab] = useState('overview');
  const [notification, setNotification] = useState(null);
  return (
    <>
      <AppHeader username = {user?.sub} role={user?.role} onLogout={logout} />

      <Box se={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
        <Tabs value={activeTab} onChange={(e, v) => setActiveTab(v)}>
          <Tab label="Overview" value="overview" />
          <Tab label="Tech Panel" value="tech_panel" />
          {isAdmin && <Tab label="Admin Panel" value="admin_panel" />}
        </Tabs>
      </Box>

      {activeTab === 'overview' && <Overview />}
      {activeTab === 'tech_panel' && <TechPanel />}
      {activeTab === 'admin_panel' && <AdminPanel />}

      <Snackbar
        open={Boolean(notification)}
        autoHideDuration={4000}
        onClose={() => setNotification(null)}
      >
        <Alert severity="success" onClose = {()=> setNotification(null)}>
          {notification}
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