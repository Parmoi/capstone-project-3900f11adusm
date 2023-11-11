import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';


import ManageAccountsIcon from '@mui/icons-material/ManageAccounts';
import AddTaskIcon from '@mui/icons-material/AddTask';
import GroupIcon from '@mui/icons-material/Group';

import { createTheme, ThemeProvider } from '@mui/material/styles';
import {Link } from "react-router-dom";


const theme = createTheme();

const linkStyle = {
  textDecoration: 'none',
  color: 'Black',
  display: 'span',
  justifyContent: 'center',
}

const style = {
  width: '20vw',
  height: '20vw',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center', 
  backgroundColor: "White",
  borderRadius: '16px'
};

function AdminHomePage() {
  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="lg" direction="column" justifyContent="center" alignItems="center">
      <CssBaseline/>
      <Box height="85vh">
        <Grid container spacing={4} height="100vh" direction="row" justifyContent="center" alignItems="center" sx={{ height: '100%',}}>
          <Grid item xs={4} sx={{margin: 'auto'}}>
            <Button aria-label="Manage Managers" style={linkStyle} component={Link} to='/manage/managers'>
              <Stack direction="column" justifyContent='center' spacing={2} sx={style} >
                <Box component="span">
                  <ManageAccountsIcon variant="outlined" display="flex" sx={{ width: '14vw', height: '14vw', marginTop: "16px"}} />
                </Box>
                <Typography variant='h4' fontSize='1.6vw'>Manage Managers</Typography>
              </Stack>
            </Button>
          </Grid>

          <Grid item xs={4} sx={{margin: 'auto'}}>
            <Button aria-label="Campaign Approval" style={linkStyle} component={Link} to='/campaign/approval'>
              <Stack direction="column" justifyContent='center' spacing={2} sx={style} >
                <Box component="span">
                  <AddTaskIcon variant="outlined" display="flex" sx={{ width: '14vw', height: '14vw', marginTop: "16px"}} />
                </Box>
                  <Typography variant='h4' fontSize='1.6vw'>Campaign Approval</Typography>
              </Stack>
            </Button>
          </Grid>

          <Grid item xs={4} sx={{margin: 'auto'}}>
            <Button aria-label="Manage Collectors" style={linkStyle} component={Link} to='/manage/collectors'>
              <Stack direction="column" justifyContent='center' spacing={2} sx={style} backgrounColor='blue'>
                <Box component="span">
                  <GroupIcon variant="outlined" display="flex" sx={{ width: '14vw', height: '14vw', marginTop: "16px",}} />
                </Box>
                  <Typography variant='h4' fontSize='1.6vw' >Manage Collectors</Typography>
              </Stack>
            </Button>
          </Grid>

        </Grid>
      </Box>
      </Container>
    </ThemeProvider>
  );
}


export default AdminHomePage;