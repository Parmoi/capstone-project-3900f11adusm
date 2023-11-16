import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';

import { createTheme, ThemeProvider } from '@mui/material/styles';

import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import { ProfileBox, ProfileDetailsDisplay, ProfileDetailsEdit, SocialMediaDisplay, SocialMediaEdit } from '../components/ProfileDetails'
import CollectionCompletion from '../components/CollectionCompletion';

import { apiCall } from '../App';

const theme = createTheme();

function Profile({privilege, user_id}) {
  const [editDetails, displayDetails] = useState(false);
  const [editSocials, displaySocials] = useState(false);
  const [data, setData] = useState({});

  const params = useParams();
  const u_id = params.id;
  const isAccount = u_id == user_id || u_id == ''
  console.log(u_id)

  const fetchInfo = () => {
    let url = '';
    if (u_id == '') {
      url='/profile';
    } else {
      url = `/profile?id=${u_id}`;
    }
  
    const options = {
      method: 'GET',
      route: url,
    };

    apiCall((d) => {
      setData(d);
    }, options)
    .then((res) => {
      if (res) {
        // set error msg if api call returns error
        
      }
    });
  }

  useEffect(() => {
    fetchInfo();
  }, []);

  const handleImageSave = () => {
    fetchInfo();
  }

  const handleSocialEdit = () => {
    displaySocials(true);;
  }

  const handleSocialSave = () => {
    displaySocials(false);
    fetchInfo();
  }

  const handleDetailsEdit = () => {
    displayDetails(true);
  }

  const handleDetailsSave = () => {
    displayDetails(false);
    fetchInfo();
  }

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
            <ProfileBox style={style} data={data} handleImageSave={handleImageSave} privilege={privilege} isAccount={isAccount}/>
            { !editSocials 
            ? <SocialMediaDisplay handleEdit={handleSocialEdit} style={style} socials={data} isAccount={isAccount}/>
            : <SocialMediaEdit handleSave={handleSocialSave} style={style}/> 
            }
          </Grid>
          <Grid item xs={8}>
            { !editDetails 
            ? <ProfileDetailsDisplay handleEdit={handleDetailsEdit} style={style} data={data} isAccount={isAccount}/> 
            : <ProfileDetailsEdit handleSave={handleDetailsSave} style={style} />             
            }
            { privilege == 1 && <CollectionCompletion style={style} /> }
          </Grid>
        </Grid>
      </Container>
    </ThemeProvider>
  );
}


export default Profile;