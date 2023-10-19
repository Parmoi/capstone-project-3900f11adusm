import React, { Fragment, useState } from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { useHistory } from 'react-router-dom';
// import IconButton from '@mui/material/IconButton';
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



const SignedInNav = ({ logout }) => {
    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);
    const navigate = useNavigate();
    // add the search function
    const [searchQuery, setSearchQuery] = useState('');
    const [filteredItems, setFilteredItems] = useState([]);
    const history = useHistory();

    const items = [
      {
        image: 'https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg',
        name: 'Homer',
        collectionName: 'Winter 2022',
        yearReleased: 1999,
        dateAdded: 1800,
      },
      {
        image: 'https://tse4.mm.bing.net/th?id=OIP.e4tAXeZ6G0YL4OE5M8KTwAHaMq&pid=Api',
        name: 'Marge',
        collectionName: 'Winter 2022',
        yearReleased: 1899,
        dateAdded: 1800,
      },
      {
        image: 'https://tse2.mm.bing.net/th?id=OIP.j7EknM6CUuEct_kx7o-dNQHaMN&pid=Api',
        name: 'Bart',
        collectionName: 'Winter 2022',
        yearReleased: 1499,
        dateAdded: 1800,
      },
      {
        image: 'https://tse3.mm.bing.net/th?id=OIP.6761X25CX3UUjklkDCnjSwHaHa&pid=Api',
        name: 'Dog',
        collectionName: 'Winter 2022',
        yearReleased: 1989,
        dateAdded: 1800,
      },
      {
        image: 'https://tse3.mm.bing.net/th?id=OIP.JqWjPHsW5aJIZDnPYMGovQHaJQ&pid=Api',
        name: 'Lisa',
        collectionName: 'Winter 2022',
        yearReleased: 1709,
        dateAdded: 1800,
      },
      {
        image: 'https://tse1.mm.bing.net/th?id=OIP.qVV8kcLdcLysZ5OOCzhKLAHaF7&pid=Api',
        name: 'Rando',
        collectionName: 'Winter 2022',
        yearReleased: 1909,
        dateAdded: 1801,
      },
    ]

    const handleInputChange = (event) => {
      setSearchQuery(event.target.value);
      filterItems(event.target.value);
    };

    const filterItems = (query) => {
      const filtered = items.filter((item) =>
        item.name.toLowerCase().includes(query.toLowerCase())
      );
      setFilteredItems(filtered);
    };

    const handleKeyPress = (event) => {
      if (event.key === 'Enter') {
        // Handle the search logic here. You can display the filtered items.
        // console.log('Search for:', searchQuery);
        // console.log('Filtered Items:', filteredItems);
        history.push(`/results?query=${encodeURIComponent(searchQuery)}`);
      }
    };
      
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
                value={searchQuery}
                onChange={handleInputChange}
                onKeyPress={handleKeyPress}
              />
            </Search>
            <div>
              {filteredItems.map((item, index) => (
                <div key={index}>{item.name}</div>
              ))}
            </div>
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