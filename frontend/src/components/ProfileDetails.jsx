import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import TextField from '@mui/material/TextField';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

import TwitterIcon from '@mui/icons-material/Twitter';
import InstagramIcon from '@mui/icons-material/Instagram';
import FacebookIcon from '@mui/icons-material/Facebook';

import { Divider } from '@mui/material';

import React, { useState, useEffect } from 'react';

import { apiCall } from '../App';

const ProfileBox = ({style}) => {
  return (
    <Stack direction="column" spacing={2} sx={style} >
      <Box component="span">
        <Avatar 
          variant="outlined"
          alt="Bob Ret"
          src="/src/images/home_page_icon.png"
          display="flex"
          sx={{ width: 150, height: 150, marginTop: "16px", fontSize: "60px"}}
        />
      </Box>
      <Typography variant="h5">Bob</Typography>
      <Typography variant="p1">Collector</Typography>
      <Box component="span">
        <Button variant="contained" sx={{marginLeft: "8px", marginBottom: "16px"}}>Change Icon</Button>
      </Box>
    </Stack>
  );
};

const SocialMediaDisplay = ({displaySocials, style}) => {
  return (
    <List sx={style}>
      <ListItem secondaryAction={ <ListItemText primary="@Bob"/> }>
        <Button 
          variant="link"
          target="_blank"
          color="default"
          startIcon={<TwitterIcon />}
          href="https://twitter.com/"
        >
          Twitter
        </Button>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <ListItemText primary="Bob"/> }>
        <Button 
          variant="link"
          target="_blank"
          color="default"
          startIcon={<FacebookIcon />}
          href="https://www.facebook.com/"
        >
          Facebook
        </Button>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <ListItemText primary="Bob"/> }>
        <Button 
          variant="link"
          target="_blank"
          color="default"
          startIcon={<InstagramIcon />}
          href="https://www.instagram.com/"
        >
          Instagram
        </Button>
      </ListItem>
      <Divider variant="middle"/>
      <Button onClick={() => { displaySocials(true); }} variant="contained" sx={{marginLeft: "16px", marginTop: "16px", marginBottom: "8px"}}>Edit</Button>
    </List>
  );
}

const SocialMediaEdit = ({displaySocials, style}) => {
  return (
    <List sx={style}>
      <ListItem secondaryAction={ <TextField fullWidth id="Address" label="Address" variant="outlined" size='small' sx={{width: 200}}/> }>
        <Button 
          variant="link"
          target="_blank"
          color="default"
          startIcon={<TwitterIcon />}
          href="https://twitter.com/"
        >
          Twitter
        </Button>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <TextField fullWidth id="Address" label="Address" variant="outlined" size='small' sx={{width: 200}}/> }>
        <Button 
          variant="link"
          target="_blank"
          color="default"
          startIcon={<FacebookIcon />}
          href="https://www.facebook.com/"
        >
          Facebook
        </Button>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <TextField fullWidth id="Address" label="Address" variant="outlined" size='small' sx={{width: 200}}/> }>
        <Button 
          variant="link"
          target="_blank"
          color="default"
          startIcon={<InstagramIcon />}
          href="https://www.instagram.com/"
        >
          Instagram
        </Button>
      </ListItem>
      <Divider variant="middle"/>
        <Button onClick={() => { displaySocials(false); }} variant="contained" sx={{marginLeft: "16px", marginTop: "16px", marginBottom: "8px"}}>Save</Button>
    </List>
  );
}

const ProfileDetailsDisplay = ({displayDetails, style}) => {

  const [data, setData] = useState([]);

  const fetchInfo = () => { 
    return fetch('http://localhost:5000/profile', {
      method: 'GET',
      headers: {
        'Content-type': 'application/json',
      },
      credentials: 'include'
    }) 
      .then((res) => res.json()) 
      .then((d) => setData(d)) 
    }

  useEffect(() => {
    fetchInfo();
  }, []);

  // console.log(data)

  return (
    <List sx={style}>
      <ListItem secondaryAction={ <ListItemText primary={data.username ? data.username : 'Unknown'}/> }>
        <ListItemText primary="Username"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <ListItemText primary={data.real_name ? data.real_name : 'Unknown'}/> }>
        <ListItemText primary="First Name"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <ListItemText primary={data.real_name ? data.real_name : 'Unknown'}/> }>
        <ListItemText primary="Last Name"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <ListItemText primary={data.email ? data.email : 'Unknown'}/> }>
        <ListItemText primary="Email"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <ListItemText primary={data.phone ? data.phone : 'Unknown'}/> }>
        <ListItemText primary="Phone Number"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <ListItemText primary={data.address ? data.address : 'Unknown'}/> }>
        <ListItemText primary="Address"/>
      </ListItem>
      <Divider variant="middle"/>
      <Button onClick={() => { displayDetails(true) }} variant="contained" sx={{marginLeft: "16px", marginTop: "16px", marginBottom: "8px"}}>Edit</Button>
    </List>
  );
}

const ProfileDetailsEdit = ({displayDetails, style}) => {  
  const edit = (e) => {
    e.preventDefault();
    const data = new FormData(e.currentTarget);

    // call api with data
    const options = {
      method: 'POST',
      route: '/profile/update',
      body: JSON.stringify({
        // email: data.get('email'),
        username: data.get('username'),
        // first_name: data.get('first_name'),
        // last_name: data.get('last_name'),
        // phone: data.get('phone'),
        // address: data.get('address'),
      })
    };

    apiCall(() => {
      displayDetails(false);
    }, options)
      .then((res) => {
        if (res) {

        }
      });
  }


  return (
    <List sx={style}>
      <ListItem secondaryAction={ <TextField fullWidth id="username" label="Username" name="username" autoComplete="username" size='small' autoFocus sx={{width: 500}}/> }>
        <ListItemText primary="Username"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <TextField fullWidth id="first_name" label="First Name" variant="outlined" size='small' sx={{width: 500}}/> }>
        <ListItemText primary="First Name"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <TextField fullWidth id="last_name" label="Last Name" variant="outlined" size='small' sx={{width: 500}}/> }>
        <ListItemText primary="Last Name"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <TextField fullWidth id="email" label="email" variant="outlined" size='small' sx={{width: 500}}/> }>
        <ListItemText primary="Email"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <TextField fullWidth id="phone" label="phone" variant="outlined" size='small' sx={{width: 500}}/> }>
        <ListItemText primary="Phone Number"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <TextField fullWidth id="address" label="address" variant="outlined" size='small' sx={{width: 500}}/> }>
        <ListItemText primary="Address"/>
      </ListItem>
      <Divider variant="middle"/>
      <Box component="form" onSubmit={edit} noValidate sx={{ mt: 1 }}>
      <Button type="submit" variant="contained" sx={{marginLeft: "16px", marginTop: "16px", marginBottom: "8px"}}>Save</Button>
      </Box>
    </List>
  );
}


export { ProfileBox, SocialMediaDisplay, SocialMediaEdit, ProfileDetailsDisplay, ProfileDetailsEdit, }