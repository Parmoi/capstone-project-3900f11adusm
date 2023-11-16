import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import TextField from '@mui/material/TextField';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Alert from '@mui/material/Alert';

import TwitterIcon from '@mui/icons-material/Twitter';
import InstagramIcon from '@mui/icons-material/Instagram';
import FacebookIcon from '@mui/icons-material/Facebook';

import WidgetUpload from './WidgetUpload';

import { Divider } from '@mui/material';

import React from 'react';

import { apiCall } from '../App';

const ProfileBox = ({style, data, handleImageSave, privilege, isAccount}) => {
  const [error, setError] = React.useState(false);
  const [errContent, setErrContent] = React.useState('');

  const handleUpload = (url) => {
    // call api with data
    const options = {
      method: 'POST',
      route: '/profile/update',
      body: JSON.stringify({
        profile_picture: url,
      })
    };

    apiCall(() => {
      handleImageSave();
    }, options)
    .then((res) => {
      if (res) {
        // set error msg if api call returns error
        setErrContent(`Error: ${res.msg}`);
        setError(true);
      }
    });
  }

  return (
    <Stack direction="column" spacing={2} sx={style} >
      <Box component="span">
        <Avatar 
          variant="outlined"
          alt="Profile Image"
          src={data.profile_picture ? data.profile_picture : ''}
          display="flex"
          sx={{ width: 150, height: 150, marginTop: "16px", fontSize: "60px"}}
        />
      </Box>
      <Typography variant="h5">{data.username ? data.username : 'Username Unknown'}</Typography>
      { privilege === 1 && <Typography variant="p1">Collector</Typography>}
      {/* { (privilege === 2 || privilege === 3) && <Route path="/" element={<ManagerHomePage/>} />} */}
      { privilege === 2 && <Typography variant="p1">Manager</Typography>}
      { privilege === 3 && <Typography variant="p1">Admin</Typography>}
      <div>
        {error ? <Alert severity='error'>{errContent}</Alert> : <></> }
      </div>
      <Box component="span">
        { isAccount && <WidgetUpload onSuccess={handleUpload} style={{marginLeft: "8px", marginBottom: "16px"}} buttonName='Change Icon'/> }
      </Box>
    </Stack>
  );
};

const SocialMediaDisplay = ({handleEdit, style, socials, isAccount}) => {
  return (
    <List sx={style}>
      <ListItem >
        <Button 
          variant="link"
          target="_blank"
          color="default"
          startIcon={<TwitterIcon />}
          href={socials.twitter_handle ? socials.twitter_handle : "https://twitter.com/"} 
        >
          Twitter
        </Button>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem >
        <Button 
          variant="link"
          target="_blank"
          color="default"
          startIcon={<FacebookIcon />}
          href={socials.facebook_handle ? socials.facebook_handle : "https://www.facebook.com/"} 
        >
          Facebook
        </Button>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem >
        <Button 
          variant="link"
          target="_blank"
          color="default"
          startIcon={<InstagramIcon />}
          href={socials.instagram_handle ? socials.instagram_handle : "https://www.instagram.com/"} 
        >
          Instagram
        </Button>
      </ListItem>
      <Divider variant="middle"/>
      {
        isAccount && <Button onClick={handleEdit} variant="contained" sx={{marginLeft: "16px", marginTop: "16px", marginBottom: "8px"}}>Edit</Button>
      }
    </List>
  );
}

const SocialMediaEdit = ({handleSave, style}) => {
  const [error, setError] = React.useState(false);
  const [errContent, setErrContent] = React.useState('');

  const edit = (e) => {
    e.preventDefault();
    const data = new FormData(e.currentTarget);

    // call api with data
    const options = {
      method: 'POST',
      route: '/profile/update_socials',
      body: JSON.stringify({
        twitter_handle: data.get('twitter_handle'),
        facebook_handle: data.get('facebook_handle'),
        instagram_handle: data.get('instagram_handle'),
      })
    };

    apiCall(() => {
      handleSave();
    }, options)
    .then((res) => {
      if (res) {
        // set error msg if api call returns error
        setErrContent(`Error: ${res.msg}`);
        setError(true);
      }
    });
  }

  return (
    <List sx={style}>
      <Box component="form" onSubmit={edit} noValidate sx={{ mt: 1 }}>
        <ListItem secondaryAction={ <TextField fullWidth id="twitter_handle" label="twitter_handle" name="twitter_handle" autoComplete="twitter_handle" variant="outlined" size='small' sx={{width: 200}}/> }>
          <Button 
            variant="link"
            target="_blank"
            color="default"
            startIcon={<TwitterIcon />}
          >
            Twitter
          </Button>
        </ListItem>
        <Divider variant="middle"/>
        <ListItem secondaryAction={ <TextField fullWidth id="facebook_handle" label="facebook_handle" name="facebook_handle" autoComplete="facebook_handle" variant="outlined" size='small' sx={{width: 200}}/> }>
          <Button 
            variant="link"
            target="_blank"
            color="default"
            startIcon={<FacebookIcon />}
          >
            Facebook
          </Button>
        </ListItem>
        <Divider variant="middle"/>
        <ListItem secondaryAction={ <TextField fullWidth id="instagram_handle" label="instagram_handle" name="instagram_handle" autoComplete="instagram_handle" variant="outlined" size='small' sx={{width: 200}}/> }>
          <Button 
            variant="link"
            target="_blank"
            color="default"
            startIcon={<InstagramIcon />}
          >
            Instagram
          </Button>
        </ListItem>
        <Divider variant="middle"/>
        <div>
          {error ? <Alert severity='error'>{errContent}</Alert> : <></> }
        </div>
        <Button type="submit" variant="contained" sx={{marginLeft: "16px", marginTop: "16px", marginBottom: "8px"}}>Save</Button>
        </Box>
    </List>
  );
}

const ProfileDetailsDisplay = ({handleEdit, style, data, isAccount }) => {

  return (
    <List sx={style}>
      <ListItem secondaryAction={ <ListItemText primary={data.username ? data.username : 'Unknown'}/> }>
        <ListItemText primary="Username"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <ListItemText primary={data.first_name ? data.first_name : 'Unknown'}/> }>
        <ListItemText primary="First Name"/>
      </ListItem>
      <Divider variant="middle"/>
      <ListItem secondaryAction={ <ListItemText primary={data.last_name ? data.last_name : 'Unknown'}/> }>
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
      {
        isAccount && <Button onClick={handleEdit} variant="contained" sx={{marginLeft: "16px", marginTop: "16px", marginBottom: "8px"}}>Edit</Button>
      }
    </List>
  );
}

const ProfileDetailsEdit = ({handleSave, style}) => {  
  const [error, setError] = React.useState(false);
  const [errContent, setErrContent] = React.useState('');

  const edit = (e) => {
    e.preventDefault();
    const data = new FormData(e.currentTarget);

    // call api with data
    const options = {
      method: 'POST',
      route: '/profile/update',
      body: JSON.stringify({
        email: data.get('email'),
        username: data.get('username'),
        first_name: data.get('first_name'),
        last_name: data.get('last_name'),
        phone: data.get('phone'),
        address: data.get('address'),
      })
    };


    apiCall(() => {
      handleSave();
    }, options)
    .then((res) => {
      if (res) {
        // set error msg if api call returns error
        setErrContent(`Error: ${res.msg}`);
        setError(true);
      }
    });
  }


  return (
    <List sx={style}>
      <Box component="form" onSubmit={edit} noValidate sx={{ mt: 1 }}>
        <ListItem secondaryAction={ <TextField fullWidth id="username" label="Username" name="username" autoComplete="username" size='small' autoFocus sx={{width: 500}}/> }>
          <ListItemText primary="Username"/>
        </ListItem>
        <Divider variant="middle"/>
        <ListItem secondaryAction={ <TextField fullWidth id="first_name" label="First Name" name="first_name" autoComplete="first_name" size='small' sx={{width: 500}}/> }>
          <ListItemText primary="First Name"/>
        </ListItem>
        <Divider variant="middle"/>
        <ListItem secondaryAction={ <TextField fullWidth id="last_name" label="Last Name" name="last_name" autoComplete="last_name" size='small' sx={{width: 500}}/> }>
          <ListItemText primary="Last Name"/>
        </ListItem>
        <Divider variant="middle"/>
        <ListItem secondaryAction={ <TextField fullWidth id="email" label="Email" name="email" autoComplete="email" size='small' sx={{width: 500}}/> }>
          <ListItemText primary="Email"/>
        </ListItem>
        <Divider variant="middle"/>
        <ListItem secondaryAction={ <TextField fullWidth id="phone" label="Phone" name="phone" autoComplete="phone" size='small' sx={{width: 500}}/> }>
          <ListItemText primary="Phone Number"/>
        </ListItem>
        <Divider variant="middle"/>
        <ListItem secondaryAction={ <TextField fullWidth id="address" label="Address" name="address" autoComplete="username" size='small' sx={{width: 500}}/> }>
          <ListItemText primary="Address"/>
        </ListItem>
        <Divider variant="middle"/>
        <div>
          {error ? <Alert severity='error'>{errContent}</Alert> : <></> }
        </div>
        <Button type="submit" variant="contained" sx={{marginLeft: "16px", marginTop: "16px", marginBottom: "8px"}}>Save</Button>
      </Box>
    </List>
  );
}


export { ProfileBox, SocialMediaDisplay, SocialMediaEdit, ProfileDetailsDisplay, ProfileDetailsEdit, }