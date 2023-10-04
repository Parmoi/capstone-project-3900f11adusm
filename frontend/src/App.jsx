import logo from './logo.svg';
import './App.css';
import React from 'react';
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

import SignIn from './components/SignIn';
import Register from './components/Register';

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
import { autocompleteClasses } from '@mui/material';

const theme = createTheme({
  palette: {
    primary: {
      main: "#216869",
      text: "#1F2421",
      light: "#BFCC94"
    },
    secondary: {
      main: "#F0F4EF",
    },
    support: {
      main: "#B4CDED",
    }
  }
});

const linkStyle = {
  textDecoration: 'none',
  color: '#1F2421'
}


const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha("#BFCC94", 0.4),
  '&:hover': {
    backgroundColor: alpha("#BFCC94", 0.2),
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
  color: alpha("#1F2421", 1),
  fontWeight: 'bold',
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
      <AppBar position="fixed" sx={{ height: "10ch", display: 'flex', justifyContent: 'center', backgroundColor: 'secondary.main' }}>
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <Link to="/" style={linkStyle}>
            <Typography variant="h6" component="div" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-evenly' }}>
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
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="fixed" sx={{ height: "10ch", display: 'flex', justifyContent: 'center', backgroundColor: 'secondary.main' }}>
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <Link to="/dashboard" style={linkStyle}>
            <Typography variant="h6" component="div" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-evenly' }}>
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
            <Button color="inherit"><Link to="/profile" style={linkStyle}><AccountBoxIcon /></Link></Button>
          </Box>
        </Toolbar>
      </AppBar>
    </Box>
  );
};

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ display: 'flex', flexDirection: 'column', rowGap: '10ch', alignItems: 'center', justifyContent: 'center' }}>
        <BrowserRouter>
          {/* <SignedInNav /> */}
          <SignedOutNav />
          <Routes>
            {/* home page stub */}
            {/* separate routes based on if they are available signed in/out, check token (?) */}
            <Route path="/" element={<span>Home page</span>} />
            <Route path="/login" element={<SignIn />} />
            <Route path="/register" element={<Register />} />
            <Route path="/profile" element={<span>Profile</span>} />
            <Route path="/dashboard" element={<span>Dashboard</span>} />
          </Routes>
        </BrowserRouter>
      </Box>
    </ThemeProvider>
  );
}

export default App;
