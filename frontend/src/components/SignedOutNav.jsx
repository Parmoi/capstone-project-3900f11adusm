import React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import SmartToyIcon from '@mui/icons-material/SmartToy';

import {
  Link,
} from 'react-router-dom';

const linkStyle = {
    textDecoration: 'none',
    color: '#F0F4EF'
}

const SignedOutNav = () => {
    return (
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="fixed" sx={{ height: "10ch", display: 'flex', justifyContent: 'center', backgroundColor: 'primary.main' }}>
          <Toolbar sx={{ justifyContent: 'space-between' }}>
            <Link to="/" style={linkStyle}>
              <Typography variant="h6" component="div" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-evenly', color: 'secondary.main' }}>
                <SmartToyIcon />&nbsp;CollectiblesCorner
              </Typography>
            </Link>
            <Box>
              <Button color="inherit"><Link to="/login" style={linkStyle}>Login</Link></Button>
              <Button color="inherit"><Link to="/register" style={linkStyle}>Register</Link></Button>
            </Box>
          </Toolbar>
        </AppBar>
      </Box >
    );
};

export default SignedOutNav;