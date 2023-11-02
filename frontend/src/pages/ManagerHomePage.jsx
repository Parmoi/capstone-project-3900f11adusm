import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';

import { createTheme, ThemeProvider } from '@mui/material/styles';

import { useState, useEffect } from 'react';


const theme = createTheme();

function ManagerHomePage() {

  const style = {
    alignItems: 'center', 
    marginTop: "20px", 
    backgroundColor: "White",
    borderRadius: '4px'
  };

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" sx={{ py: 6, }} maxWidth="lg">
      <CssBaseline/>
        <Grid container spacing={2}>
          <Grid item xs={4}>

          </Grid>

          <Grid item xs={4}>

          </Grid>

          <Grid item xs={4}>

          </Grid>

        </Grid>
      </Container>
    </ThemeProvider>
  );
}


export default ManagerHomePage;