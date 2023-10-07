import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import TextField from '@mui/material/TextField';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import Grid from '@mui/material/Grid';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import { styled, useTheme, ThemeProvider } from '@mui/material/styles';

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
  flexGrow: 1,
}));

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
      // <Box sx={{ width: 200, height: 200 }}>
      //   <Stack spacing={{ xs: 1, sm: 2 }} direction="row" useFlexGap flexWrap="wrap">
          // <Container component="main" maxWidth="xs">
          //   <CssBaseline />
          //   <Avatar 
          //     sx={{ width: 150, height: 150 }}
          //   />
          //   <Button variant="contained">Change Icon</Button>
          // </Container>

      //     <Item>Item 1</Item>
      //     <Item>Item 2</Item>
      //     <Item>Long content</Item>
      //   </Stack>
      // </Box>
      // <ThemeProvider theme={useTheme()}>
        // <Container component="main" maxWidth="xs">
        //   <CssBaseline />
        //   <Avatar 
        //     sx={{ width: 100, height: 100 }}
        //   />
        // </Container>
      //   <Box sx={{ width: 200 }}>
      //     <Stack spacing={{ xs: 1, sm: 2 }} direction="row" useFlexGap flexWrap="wrap">
            // <Avatar 
            //   sx={{ width: 100, height: 100 }}
            // />
      //       <Item>Item 1</Item>
      //       <Item>Item 2</Item>
      //       <Item>Long content</Item>
      //     </Stack>
      //   </Box>
      // </ThemeProvider>
    );
  }


export default Profile;