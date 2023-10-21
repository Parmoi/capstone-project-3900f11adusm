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
import LinearProgress, { linearProgressClasses } from '@mui/material/LinearProgress';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';

import TwitterIcon from '@mui/icons-material/Twitter';
import InstagramIcon from '@mui/icons-material/Instagram';
import FacebookIcon from '@mui/icons-material/Facebook';
import WhatsAppIcon from '@mui/icons-material/WhatsApp';

import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import { Divider } from '@mui/material';

const style = {
  alignItems: 'center', 
  marginTop: "20px", 
  backgroundColor: "White",
  borderRadius: '4px'
};

const BorderLinearProgress = styled(LinearProgress)(({ theme }) => ({
  height: 10,
  borderRadius: 5,
  [`&.${linearProgressClasses.colorPrimary}`]: {
    backgroundColor: theme.palette.grey[theme.palette.mode === 'light' ? 200 : 800],
  },
  [`& .${linearProgressClasses.bar}`]: {
    borderRadius: 5,
    backgroundColor: theme.palette.mode === 'light' ? '#1a90ff' : '#308fe8',
  },
}));

const theme = createTheme();

function Profile() {
  return (
    <ThemeProvider theme={theme}>
      <Container component="main" sx={{ py: 6, }} maxWidth="lg">
        <CssBaseline />
          <Grid container spacing={2}>
            <Grid item xs={4}>
              <Stack direction="column" spacing={2} sx={style} >
                <Box component="span">
                  <Avatar 
                    variant="outlined"
                    sx={{ width: 150, height: 150, marginTop: "16px"}}
                  />
                </Box>
                <Typography variant="h5">Bob</Typography>
                <Typography variant="p1">Collector</Typography>
                <Box component="span">
                  <Button variant="contained" sx={{marginLeft: "8px", marginBottom: "16px"}}>Change Icon</Button>
                </Box>
              </Stack>
              <List sx={style}>
                <ListItem secondaryAction={ <ListItemText primary="@Bob"/> }>
                  <TwitterIcon label="Twitter"/>
                  <ListItemText primary="Twitter" sx={{marginLeft: "8px"}}/>
                </ListItem>
                <Divider variant="middle"/>
                <ListItem secondaryAction={ <ListItemText primary="Bob"/> }>
                  <FacebookIcon/>
                  <ListItemText primary="Facebook" sx={{marginLeft: "8px"}}/>
                </ListItem>
                <Divider variant="middle"/>
                <ListItem secondaryAction={ <ListItemText primary="Bob"/> }>
                  <InstagramIcon/>
                  <ListItemText primary="Instagram" sx={{marginLeft: "8px"}}/>
                </ListItem>
                <Divider variant="middle"/>
                <ListItem secondaryAction={ <ListItemText primary="Bob"/> }>
                  <WhatsAppIcon/>
                  <ListItemText primary="WhatsApp" sx={{marginLeft: "8px"}}/>
                </ListItem>
                <Divider variant="middle"/>
                  <Button variant="contained" sx={{margin: "16px"}}>Edit</Button>
              </List>
            </Grid>
            <Grid item xs={8}>
              {/* <Grid md={12} sx={style}>
                <div>
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
                </div>
              </Grid> */}

              <Grid md={12} sx={style}>
                <div>
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
                      <Button variant="contained" sx={{margin: "16px"}}>Save</Button>
                  </List>
                </div>
              </Grid>


              <Box sx={style} p="8px">
                <Typography variant="h5" sx={{margin: "8px"}}>Collection Completion</Typography>
                <List sx={{alignItems: "center"}} p={8}>
                  <Typography sx={{margin: "8px"}}>Campaign Name</Typography>
                  <BorderLinearProgress variant="determinate" value={50} sx={{margin: "8px"}}/>
                  <Divider sx={{margin: "8px"}}/>
                  <Typography sx={{margin: "8px"}}>Campaign Name</Typography>
                  <BorderLinearProgress variant="determinate" value={50} sx={{margin: "8px"}}/>
                </List> 
              </Box>
            </Grid>
          </Grid>
      </Container>
    </ThemeProvider>
  );
}


export default Profile;