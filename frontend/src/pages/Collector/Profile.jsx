import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';

import { createTheme, ThemeProvider } from '@mui/material/styles';

import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import { ProfileBox, ProfileDetailsDisplay, ProfileDetailsEdit, SocialMediaDisplay, SocialMediaEdit } from '../../components/ProfileDetails'
import CollectionCompletion from '../../components/CollectionCompletion';

import { apiCall } from '../../App';

const theme = createTheme();

// Page which displays user's profile details
// Displays username, first and last name, email, phone number, address, social media, profile avatar and collection completion
// Allows user to edit profile details
function Profile() {
  const [editDetails, displayDetails] = useState(false);
  const [editSocials, displaySocials] = useState(false);
  const [data, setData] = useState([]);
  const [userProfile, setUserProfile] = useState(false);

  const params = useParams();
  const u_id = params.id;

  const fetchInfo = () => {
    // fetches info of profile
    let url = '';
    if (u_id == '') {
      // user profile
      url='/profile';
      setUserProfile(true);
    } else {
      url = `/profile?id=${u_id}`;
    }
  
    const options = {
      method: 'GET',
      route: url,
    };

    apiCall((d) => {
      setData(d);
    }, options);
  }

  useEffect(() => {
    fetchInfo();
  }, []);

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
            <ProfileBox style={style} data={data}/>
            { !editSocials 
            ? <SocialMediaDisplay displaySocials={displaySocials} style={style} />
            : <SocialMediaEdit displaySocials={displaySocials} style={style} /> 
            }
          </Grid>
          <Grid item xs={8}>
            { !editDetails 
            ? <ProfileDetailsDisplay displayDetails={displayDetails} style={style} data={data} /> 
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