import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import TextField from '@mui/material/TextField';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';

import TwitterIcon from '@mui/icons-material/Twitter';
import InstagramIcon from '@mui/icons-material/Instagram';
import FacebookIcon from '@mui/icons-material/Facebook';

import { createTheme, ThemeProvider } from '@mui/material/styles';
import { Divider } from '@mui/material';

import { useState } from 'react';

import CollectionCompletion from '../components/CollectionCompletion';

const style = {
  alignItems: 'center', 
  marginTop: "20px", 
  backgroundColor: "White",
  borderRadius: '4px'
};

const ProfileBox = () => {
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

const SocialMediaDisplay = () => {
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
        <Button variant="contained" sx={{marginLeft: "16px", marginTop: "16px", marginBottom: "8px"}}>Edit</Button>
    </List>
  );
}

const SocialMediaEdit = () => {
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
        <Button variant="contained" sx={{marginLeft: "16px", marginTop: "16px", marginBottom: "8px"}}>Edit</Button>
    </List>
  );
}

const ProfileDetailsDisplay = ({ editDetails }) => {
  // editDetails(true);

  return (
    <List sx={style}>
      <ListItem secondaryAction={ <ListItemText primary="Bob"/> }>
        <ListItemText primary="Username"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <ListItemText primary="Bob"/> }>
        <ListItemText primary="Full Name"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <ListItemText primary="bob@email.com"/> }>
        <ListItemText primary="Email"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <ListItemText primary="Unknown"/> }>
        <ListItemText primary="Phone Number"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <ListItemText primary="Unknown"/> }>
        <ListItemText primary="Address"/>
      </ListItem>
      <Divider variant="middle"/>
      <Button variant="contained" sx={{margin: "16px"}}>Edit</Button>
    </List>
  );
}

const ProfileDetailsEdit = () => {
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
      <Button variant="contained" sx={{marginLeft: "16px", marginTop: "16px", marginBottom: "8px"}}>Save</Button>
    </List>
  );
}

const theme = createTheme();

function Profile() {
  const [mediaDisplay, mediaEdit] = useState(false);
  const [detailsDisplay, detailsEdit] = useState(false);

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" sx={{ py: 6, }} maxWidth="lg">
      <CssBaseline/>
        <Grid container spacing={2}>
          <Grid item xs={4}>
            <ProfileBox/>
            { !mediaDisplay 
            ? <SocialMediaDisplay/>
            : <SocialMediaEdit/> 
            
            }
          </Grid>
          <Grid item xs={8}>
            { !detailsDisplay 
            ? <ProfileDetailsDisplay/>
            : <ProfileDetailsEdit/>
            
            }
            <CollectionCompletion/>
          </Grid>
        </Grid>
      </Container>
    </ThemeProvider>
  );
}


export default Profile;