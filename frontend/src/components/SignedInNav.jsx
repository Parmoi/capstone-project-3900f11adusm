import React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import AccountBoxIcon from '@mui/icons-material/AccountBox';
import { styled, alpha } from '@mui/material/styles';
import SearchIcon from '@mui/icons-material/Search';
import InputBase from '@mui/material/InputBase';
import SmartToyIcon from '@mui/icons-material/SmartToy';
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
import CurrencyExchangeIcon from '@mui/icons-material/CurrencyExchange';
import {
    Link,
    useNavigate,
  } from 'react-router-dom';

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

const SignedInNav = ({ logout, username, userId }) => {
    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);
    const navigate = useNavigate();
  
    const handleClick = (event) => {
      setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
      setAnchorEl(null);
    };

    const [searchInput, setSearchInput] = React.useState(''); // New state for managing the search input

    const handleSearchChange = (event) => {
      setSearchInput(event.target.value); // Update the searchInput state whenever the input changes
    };

    const handleSearchKeyPress = (event) => {
      if(event.key === 'Enter') {
        navigate(`/search/${searchInput}`); // Navigate to /search/:query when Enter is pressed
      }
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
            <Search>
              <SearchIconWrapper>
                <SearchIcon />
              </SearchIconWrapper>
              <StyledInputBase
                placeholder="Search…"
                inputProps={{ 'aria-label': 'search' }}
                value={searchInput} // Bind the input value to state
                onChange={handleSearchChange} // Listen for changes
                onKeyPress={handleSearchKeyPress} // Listen for the Enter key press
              />
            </Search>
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
              <MenuItem onClick={handleClose}>
                <Avatar />
                <Link to={`/profile/${userId}`} style={{ textDecoration: 'none', color: 'inherit' }}>Profile</Link>
              </MenuItem>
              <MenuItem onClick={handleClose}>
                <ListItemIcon>
                  <LibraryAddCheckIcon />
                </ListItemIcon>
                <Link to="/collection" style={{ textDecoration: 'none', color: 'inherit' }}>Collection</Link>
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
                  <CurrencyExchangeIcon />
                </ListItemIcon>
                <Link to="/trade" style={{ textDecoration: 'none', color: 'inherit' }}>Trade item</Link>
              </MenuItem>
              <MenuItem onClick={handleClose}>
                <ListItemIcon>
                  <SellIcon />
                </ListItemIcon>
                <Link to="/tradelist" style={{ textDecoration: 'none', color: 'inherit' }}>Tradelist</Link>
              </MenuItem>
              <MenuItem onClick={handleClose}>
                <ListItemIcon>
                  <PriceCheckIcon />
                </ListItemIcon>
                <Link to="/offers" style={{ textDecoration: 'none', color: 'inherit' }}>Offers Sent</Link>
              </MenuItem>
              <MenuItem onClick={handleClose}>
                <ListItemIcon>
                  <CreditScoreIcon />
                </ListItemIcon>
                <Link to="/exchange-history" style={{ textDecoration: 'none', color: 'inherit' }}>Exchange History</Link>
              </MenuItem>
              <Divider />
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

  export default SignedInNav;