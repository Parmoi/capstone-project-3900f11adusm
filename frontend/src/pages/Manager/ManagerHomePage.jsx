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
  width: '20vw',
  height: '20vw',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center', 
  backgroundColor: "White",
  borderRadius: '16px'
};

function ManagerHomePage() {
  return (
    // <ThemeProvider theme={theme}>
    //   <Container component="main" sx={{ py: 6, }} maxWidth="lg">
    //   <CssBaseline/>
    //     <Grid container direction="row" justifyContent="flex-end" alignItems="center" spacing={4} sx={{marginTop: '100px'}}>
    //       <Grid item xs={4}>
    //       <Button aria-label="collecter feedback" style={linkStyle} component={Link} to='/manager/feedback'>
    //         <Stack direction="column" spacing={2} sx={style} >
    //           <Box component="span">
    //             <ForumOutlinedIcon variant="outlined" display="flex" sx={{ width: 150, height: 150, marginTop: "16px"}} />
    //           </Box>
    //           <Typography variant='h4' sx={{ margin: '20px'}}>Feedback</Typography>
    //         </Stack>
    //         </Button>
    //       </Grid>

    //       <Grid item xs={4}>
    //       <Button aria-label="post campaign" style={linkStyle} component={Link} to='/manager/post'>
    //         <Stack direction="column" spacing={2} sx={style} >
    //           <Box component="span">
    //             <UploadOutlinedIcon variant="outlined" display="flex" sx={{ width: 150, height: 150, marginTop: "16px"}} />
    //           </Box>
    //           <Typography variant='h4' sx={{ margin: '20px'}}>Post Campaign</Typography>
    //         </Stack>
    //         </Button>
    //       </Grid>

    //       <Grid item xs={4}>
    //       <Button aria-label="analytics" style={linkStyle} component={Link} to='/manager/analytics'>
    //         <Stack direction="column" spacing={2} sx={style} >
    //             <Box component="span">
    //               <AssessmentIcon variant="outlined" display="flex" sx={{ width: 150, height: 150, marginTop: "16px",}} />
    //             </Box>
    //             <Typography variant='h4' sx={{ margin: '20px'}}>Analytics</Typography>
    //         </Stack>
    //         </Button>
    //       </Grid>

    //     </Grid>
    //   </Container>
    // </ThemeProvider>

    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="lg" direction="column" justifyContent="center" alignItems="center">
      <CssBaseline/>
        <Box height="90vh" mr={4}>
          <Grid container height="100vh" direction="row" justifyContent="center" alignItems="center" spacing={12} sx={{ height: '100%'}}>
            <Grid item xs={4}>
              <Button aria-label="collecter feedback" style={linkStyle} component={Link} to='/'>
                <Stack direction="column" justifyContent='center' spacing={2} sx={style} >
                  <Box component="span">
                    <ForumOutlinedIcon variant="outlined" display="flex" sx={{ width: '14vw', height: '14vw', marginTop: "16px"}} />
                  </Box>
                  <Typography variant='h4' fontSize='1.6vw' sx={{ margin: '20px'}}>Collecter Feedback</Typography>
                </Stack>
              </Button>
            </Grid>

            <Grid item xs={4}>
              <Button aria-label="Post Campaign" style={linkStyle} component={Link} to='/'>
                <Stack direction="column" justifyContent='center' spacing={2} sx={style} >
                  <Box component="span">
                    <UploadOutlinedIcon variant="outlined" display="flex" sx={{ width: '14vw', height: '14vw', marginTop: "16px"}} />
                  </Box>
                    <Typography variant='h4' fontSize='1.6vw' sx={{ margin: '20px'}}>Post Campaign</Typography>
                </Stack>
              </Button>
            </Grid>

            <Grid item xs={4}>
              <Button aria-label="Analytics" style={linkStyle} component={Link} to='/'>
                <Stack direction="column" justifyContent='center' spacing={2} sx={style} backgrounColor='blue'>
                  <Box component="span">
                    <AssessmentIcon variant="outlined" display="flex" sx={{ width: '14vw', height: '14vw', marginTop: "16px",}} />
                  </Box>
                    <Typography variant='h4' fontSize='1.6vw'  sx={{ margin: '20px'}}>Analytics</Typography>
                </Stack>
              </Button>
            </Grid>

          </Grid>
        </Box>
      </Container>
    </ThemeProvider>
  );
}


export default ManagerHomePage;