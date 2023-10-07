import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';


const Profile = () => {
    return (
      <Box sx={{ width: '100%', maxWidth: '100%', bgcolor: 'background.paper' }}>
        <Box sx={{ my: 3, mx: 2 }}>
          <Grid container alignItems="center" justifyContent="center">
            <Grid item xs={2}>
              <Stack direction="column" spacing={3} >
                <Avatar 
                  sx={{ width: "300px", height: "300px", margin: "auto" }}
                />
                <Button variant="contained">Change Icon</Button>
              </Stack>
            </Grid>
            <Grid item xs={2}></Grid>
            <Grid item xs={3}>
              <Stack direction="column" spacing={3}>
                <Typography gutterBottom variant="h6" component="div">
                  Username
                </Typography>
                <TextField label="Username" />
                <Typography gutterBottom variant="h6" component="div">
                  Given Name
                </Typography>
                <TextField label="John Smith" />
              </Stack>
            </Grid>
          </Grid>
        </Box>
        <Divider variant="middle" />
        <Box sx={{ m: 2 }}>
          <Stack direction="column" spacing={3}>
            <Typography gutterBottom variant="h6" component="div">
              Address
            </Typography>
            <TextField label="Type your home address here" />
            <Typography gutterBottom variant="h6" component="div">
              Email Address
            </Typography>
            <TextField label="address@gmail.com" />
            <Typography gutterBottom variant="h6" component="div">
              Phone Number
            </Typography>
            <TextField label="0489 329 892" />
          </Stack>
        </Box>
      </Box>
    );
  }


export default Profile;