import React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import AccountBoxIcon from '@mui/icons-material/AccountBox';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import Tooltip from '@mui/material/Tooltip';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import Logout from '@mui/icons-material/Logout';
import {
    Link,
    useNavigate
  } from 'react-router-dom';

const linkStyle = {
    textDecoration: 'none',
    color: '#F0F4EF'
}


const AdminSignedInNav = ({ logout, username }) => {
    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);
    const navigate = useNavigate();
  
    const handleClick = (event) => {
      setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
      setAnchorEl(null);
    };


    return (
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="fixed" sx={{ height: "10ch", display: 'flex', justifyContent: 'center', backgroundColor: 'primary.main' }}>
          <Toolbar sx={{ justifyContent: 'space-between' }}>
            <Link to="/" style={linkStyle}>
              <Typography variant="h6" component="div" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-evenly', color: 'secondary.main' }}>
                <SmartToyIcon />&nbsp;CollectiblesCorner
              </Typography>
            </Link>
            <Box
              sx={{ display: 'flex', flexDirection: 'flex-end', alignItems: 'center' }}
            >
              <Typography variant='h6'>{username}</Typography>
              <Box>
                <Button color="inherit">
                  <Tooltip title="Menu">
                    <AccountBoxIcon
                      onClick={handleClick}
                      sx={{ color: 'secondary.main' }}
                      aria-controls={open ? 'account-menu' : undefined}
                      aria-haspopup="true"
                      aria-expanded={open ? 'true' : undefined}
                    />
                  </Tooltip>
                </Button>
              </Box>
            </Box>
            <Menu
              anchorEl={anchorEl}
              id="account-menu"
              open={open}
              onClose={handleClose}
              onClick={handleClose}
              PaperProps={{
                elevation: 0,
                sx: {
                  overflow: 'visible',
                  filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
                  mt: 1.5,
                  '& .MuiAvatar-root': {
                    width: 32,
                    height: 32,
                    ml: -0.5,
                    mr: 1,
                  },
                  '&:before': {
                    content: '""',
                    display: 'block',
                    position: 'absolute',
                    top: 0,
                    right: 14,
                    width: 10,
                    height: 10,
                    bgcolor: 'background.paper',
                    transform: 'translateY(-50%) rotate(45deg)',
                    zIndex: 0,
                  },
                },
              }}
              transformOrigin={{ horizontal: 'right', vertical: 'top' }}
              anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
            >
              <MenuItem onClick={() => {
                handleClose();
                logout();
                navigate('/');
                }}>
                <ListItemIcon>
                  <Logout fontSize="small" />
                </ListItemIcon>
                Sign out
              </MenuItem>
            </Menu>
          </Toolbar>
        </AppBar>
      </Box>
    );
  };

  export default AdminSignedInNav;