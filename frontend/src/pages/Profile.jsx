import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';

import { createTheme, ThemeProvider } from '@mui/material/styles';

import { useState } from 'react';

import { ProfileBox, ProfileDetailsDisplay, ProfileDetailsEdit, SocialMediaDisplay, SocialMediaEdit } from '../components/ProfileDetails'
import CollectionCompletion from '../components/CollectionCompletion';

const theme = createTheme();

function Profile() {
  const [editDetails, displayDetails] = useState(false);
  const [editSocials, displaySocials] = useState(false);

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
            <ProfileBox style={style}/>
            { !editSocials 
            ? <SocialMediaDisplay displaySocials={displaySocials} style={style} />
            : <SocialMediaEdit displaySocials={displaySocials} style={style} /> 
            }
          </Grid>
          <Grid item xs={8}>
            { !editDetails 
            ? <ProfileDetailsDisplay displayDetails={displayDetails} style={style} /> 
            : <ProfileDetailsEdit displayDetails={displayDetails} style={style} />             
            }
            <CollectionCompletion style={style} />
          </Grid>
        </Grid>
      </Container>
    </ThemeProvider>
  );
}


export default Profile;