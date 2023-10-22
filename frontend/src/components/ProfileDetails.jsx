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
    const options = {
      method: 'GET',
      route: '/profile',
    };

    apiCall(() => { }, options)
      .then(data => { setData(data) })
  }

  useEffect(() => {
    fetchInfo();
  }, []);

  // console.log(data)

  return (
    <List sx={style}>
      <ListItem secondaryAction={ <ListItemText primary={JSON.stringify(data, null, 2) }/> }>
        <ListItemText primary="Username"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <ListItemText primary={data['first_name']}/> }>
        <ListItemText primary="Full Name"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <ListItemText primary={data['email']}/> }>
        <ListItemText primary="Email"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <ListItemText primary={data['phone']}/> }>
        <ListItemText primary="Phone Number"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <ListItemText primary={data['address']}/> }>
        <ListItemText primary="Address"/>
      </ListItem>
      <Divider variant="middle"/>
      <Button onClick={() => { displayDetails(true) }} variant="contained" sx={{marginLeft: "16px", marginTop: "16px", marginBottom: "8px"}}>Edit</Button>
    </List>
  );
}

const ProfileDetailsEdit = ({displayDetails, style}) => {
  return (
    <List sx={style}>
      <ListItem secondaryAction={ <TextField fullWidth id="Username" label="Username" variant="outlined" size='small' sx={{width: 500}}/> }>
        <ListItemText primary="Username"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <TextField fullWidth id="Full Name" label="Full Name" variant="outlined" size='small' sx={{width: 500}}/> }>
        <ListItemText primary="Full Name"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <TextField fullWidth id="Email" label="Email" variant="outlined" size='small' sx={{width: 500}}/> }>
        <ListItemText primary="Email"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <TextField fullWidth id="Phone Number" label="Phone Number" variant="outlined" size='small' sx={{width: 500}}/> }>
        <ListItemText primary="Phone Number"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <TextField fullWidth id="Address" label="Address" variant="outlined" size='small' sx={{width: 500}}/> }>
        <ListItemText primary="Address"/>
      </ListItem>
      <Divider variant="middle"/>
      <Button onClick={() => { displayDetails(false) }} variant="contained" sx={{marginLeft: "16px", marginTop: "16px", marginBottom: "8px"}}>Save</Button>
    </List>
  );
}


export { ProfileBox, SocialMediaDisplay, SocialMediaEdit, ProfileDetailsDisplay, ProfileDetailsEdit, }