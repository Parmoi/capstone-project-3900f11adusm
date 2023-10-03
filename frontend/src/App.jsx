import logo from './logo.svg';
import './App.css';
import React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
// import IconButton from '@mui/material/IconButton';

import SignIn from './components/SignIn';
import Register from './components/Register';

import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  // useParams,
  // useNavigate,
  // Outlet,
} from 'react-router-dom';

const SignedOutNav = () => {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <Typography variant="h6" component="div">
          🧸 CollectiblesCorner
          </Typography>
          <Box>
            <Button color="inherit"><Link to="/login">Login</Link></Button>
            <Button color="inherit"><Link to="/register">Register</Link></Button>
          </Box>
        </Toolbar>
      </AppBar>
    </Box>
  );
};

function App() {
  return (
    <Box>
    <BrowserRouter>
      <SignedOutNav />
      <Routes>
        <Route path="/login" element={<SignIn />} />
        <Route path="/register" element={<Register />}/>
      </Routes>
    </BrowserRouter>
    </Box>
  );
}

export default App;
