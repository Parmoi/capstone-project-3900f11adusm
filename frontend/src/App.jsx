import logo from './logo.svg';
import './App.css';
import React, { Fragment } from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
// import IconButton from '@mui/material/IconButton';
import AccountBoxIcon from '@mui/icons-material/AccountBox';
import { styled, alpha } from '@mui/material/styles';
import SearchIcon from '@mui/icons-material/Search';
import InputBase from '@mui/material/InputBase';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import { ThemeProvider, createTheme } from "@mui/material/styles";
import Tooltip from '@mui/material/Tooltip';
import Menu from '@mui/material/Menu';
import Avatar from '@mui/material/Avatar';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import Divider from '@mui/material/Divider';
import Logout from '@mui/icons-material/Logout';
import LibraryAddCheckIcon from '@mui/icons-material/LibraryAddCheck';
import VisibilityIcon from '@mui/icons-material/Visibility';
import SellIcon from '@mui/icons-material/Sell';
import PriceCheckIcon from '@mui/icons-material/PriceCheck';
import CreditScoreIcon from '@mui/icons-material/CreditScore';

import SignIn from './components/SignIn';
import Register from './components/Register';

// API call for testing
import { useState, useEffect } from 'react';


import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  Navigate,
  // useParams,
  // useNavigate,
  // Outlet,
} from 'react-router-dom';
import { Helmet } from 'react-helmet';

const PORT = 5000;

export async function apiCall(onSuccess, options, ...optional) {
  const url = `http://localhost:${PORT}${options.route}`;
  const params = {
    method: options.method,
    headers: {
      'Content-type': 'application/json',
    },
    body: options.body
  }
  console.log(url);
  console.log(params);

  const response = await fetch(url, params);
  const data = await response.json();
  if (data.error) {
    return data.error;
  } else {
    return onSuccess(data, ...optional);
  }
}


const theme = createTheme({
  palette: {
    primary: {
      main: "#216869",
      light: "#BFCC94",
      text: "#1F2421",
    },
    secondary: {
      main: "#F0F4EF",
    },
    support: {
      main: "#B4CDED",
    },
  }
});

const linkStyle = {
  textDecoration: 'none',
  color: '#F0F4EF'
}

const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  borderWidth: '100px',
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  marginLeft: 0,
  width: '100%',
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(1),
    width: 'auto',
  },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    // vertical padding + font size from searchIcon
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    width: '100%',
    [theme.breakpoints.up('sm')]: {
      width: '50ch',
    },
  },
}));

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

const SignedInNav = () => {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
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
          <Link to="/dashboard" style={linkStyle}>
            <Typography variant="h6" component="div" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-evenly', color: 'secondary.main' }}>
              <SmartToyIcon />&nbsp;CollectiblesCorner
            </Typography>
          </Link>
          <Search>
            <SearchIconWrapper>
              <SearchIcon />
            </SearchIconWrapper>
            <StyledInputBase
              placeholder="Search…"
              inputProps={{ 'aria-label': 'search' }}
            />
          </Search>
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
            <MenuItem onClick={handleClose}>
              <Avatar />
              <Link to="/profile" style={{ textDecoration: 'none', color: 'inherit' }}>Profile</Link>
            </MenuItem>
            <MenuItem onClick={handleClose}>
              <ListItemIcon>
                <LibraryAddCheckIcon />
              </ListItemIcon>
              Collections
            </MenuItem>
            <MenuItem onClick={handleClose}>
              <ListItemIcon>
                <VisibilityIcon />
              </ListItemIcon>
              <Link to="/wantlist" style={{ textDecoration: 'none', color: 'inherit' }}>Wantlist</Link>
            </MenuItem>
            <Divider />
            <MenuItem onClick={handleClose}>
              <ListItemIcon>
                <SellIcon />
              </ListItemIcon>
              Tradelist
            </MenuItem>
            <MenuItem onClick={handleClose}>
              <ListItemIcon>
                <PriceCheckIcon />
              </ListItemIcon>
              Offers
            </MenuItem>
            <MenuItem onClick={handleClose}>
              <ListItemIcon>
                <CreditScoreIcon />
              </ListItemIcon>
              Order History
            </MenuItem>
            <Divider />
            <MenuItem onClick={handleClose}>
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

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  return (
    <Fragment>
      <ThemeProvider theme={theme}>
        <Helmet bodyAttributes={{ style: 'background-color : white' }} />
        <Box sx={{ display: 'flex', flexDirection: 'column', rowGap: '10ch', alignItems: 'center', justifyContent: 'center' }}>
          { !loggedIn
           ?  <BrowserRouter>
              <SignedOutNav />
              <Routes>
                <Route path="/" element={<span>Home page</span>} />
                <Route path="/login" element={<SignIn setLogin={setLoggedIn}/>} />
                <Route path="/register" element={<Register setLogin={setLoggedIn}/>} />
              </Routes>
              </BrowserRouter>
          : <BrowserRouter>
            <SignedInNav />
            <Routes>
              <Route path="/profile" element={<span>Profile</span>} />
              <Route path="/wantlist" element={<WantList />} />
              <Route path="/dashboard" element={<span>Dashboard</span>} />
            </Routes>
          </BrowserRouter>
          } 
        </Box>
      </ThemeProvider>
    </Fragment>
  );
}

export default App;
