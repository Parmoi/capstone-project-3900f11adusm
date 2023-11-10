import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';

import AssessmentIcon from '@mui/icons-material/Assessment';
import ForumOutlinedIcon from '@mui/icons-material/ForumOutlined';
import UploadOutlinedIcon from '@mui/icons-material/UploadOutlined';

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
  width: '350px',
  height: '350px',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center', 
  backgroundColor: "White",
  borderRadius: '16px'
};

function AdminHomePage() {
  return (
    <ThemeProvider theme={theme}>
      <Container component="main" sx={{ py: 6, }} maxWidth="lg">
      <CssBaseline/>
        <Grid container direction="row" justifyContent="flex-end" alignItems="center" spacing={4} sx={{marginTop: '100px'}}>
          <Grid item xs={4}>
          <Button aria-label="Manage Managers" style={linkStyle} component={Link} to='/manager/feedback'>
            <Stack direction="column" spacing={2} sx={style} >
              <Box component="span">
                <ForumOutlinedIcon variant="outlined" display="flex" sx={{ width: 150, height: 150, marginTop: "16px"}} />
              </Box>
              <Typography variant='h4' sx={{ margin: '20px'}}>Manage Managers</Typography>
            </Stack>
            </Button>
          </Grid>

          <Grid item xs={4}>
          <Button aria-label="Campaign Approval" style={linkStyle} component={Link} to='/manager/post'>
            <Stack direction="column" spacing={2} sx={style} >
              <Box component="span">
                <UploadOutlinedIcon variant="outlined" display="flex" sx={{ width: 150, height: 150, marginTop: "16px"}} />
              </Box>
              <Typography variant='h4' sx={{ margin: '20px'}}>Campaign Approval</Typography>
            </Stack>
            </Button>
          </Grid>

          <Grid item xs={4}>
          <Button aria-label="Manage Collectors" style={linkStyle} component={Link} to='/manager/analytics'>
            <Stack direction="column" spacing={2} sx={style} >
                <Box component="span">
                  <AssessmentIcon variant="outlined" display="flex" sx={{ width: 150, height: 150, marginTop: "16px",}} />
                </Box>
                <Typography variant='h4' sx={{ margin: '20px'}}>Manage Collectors</Typography>
            </Stack>
            </Button>
          </Grid>

        </Grid>
      </Container>
    </ThemeProvider>
  );
}


export default AdminHomePage;