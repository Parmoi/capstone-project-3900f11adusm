import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Paper from '@mui/material/Paper';
import Link from '@mui/material/Link';
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));

const theme = createTheme();

function Profile() {
  return (
    <ThemeProvider theme={theme}>
      <Container component="main" sx={{ py: 12, backgroundColor: 'blue' }} maxWidth="xl">
        <CssBaseline />
        <Box sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            backgroundColor: 'Black'
          }}
        >
          <Grid container spacing={2}>
            <Grid item xs={4}>
              <Box>
                <Item>Avatar and Icon</Item>
              </Box>
            </Grid>
            <Grid item xs={8}>
              <Box>
                <Item>Addresses</Item>
              </Box>
            </Grid>
            <Grid item xs={4}>
              <Box>
                <Item>Social Media</Item>
              </Box>
            </Grid>
            <Grid item xs={8}>
              <Box>
                <Item>Progress Bar</Item>
              </Box>
            </Grid>
          </Grid>
        </Box>
        {/* <Grid container sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            backgroundColor: 'red'
          }} 
        > */}
        {/* <Grid item xs={8}>
          <Item>xs=8</Item>
        </Grid>
        <Grid item xs={4}>
          <Item>xs=4</Item>
        </Grid> */}
          {/* <Box sx={{ my: 3, mx: 2, backgroundColor: 'purple' }}>
            <Grid container alignItems="center" justifyContent="center" sx={{backgroundColor: 'white'}}>
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
          </Box> */}

          {/* <Grid item xs={12} sm={6} md={4} sx={{ py: 8, backgroundColor: 'purple' }}>
            <Box
              sx={{ height: '100%', width: '100%', display: 'flex', flexDirection: 'column', backgroundColor: 'white' }}
            >
              <CardMedia
                component="div"
                sx={{
                  // 16:9
                  pt: '56.25%',
                }}
                image="https://source.unsplash.com/random?wallpapers"
              />
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography gutterBottom variant="h5" component="h2">
                  Heading
                </Typography>
                <Typography>
                  This is a media card. You can use this section to describe the content.
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small">View</Button>
                <Button size="small">Edit</Button>
              </CardActions>
            </Box>
          </Grid> */}
          
          
        {/* </Grid> */}
      </Container>
    </ThemeProvider>
  );
}


export default Profile;