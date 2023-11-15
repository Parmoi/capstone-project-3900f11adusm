import React, { useState } from 'react';
import ImageCarousel from '../../components/ImageCarousel';
import {
    Grid,
    Button,
    Typography,
    Box,
    Container,
    Paper,
    InputLabel, 
    MenuItem, 
    FormControl,
    Select,
} from '@mui/material'

import { useParams, useNavigate } from 'react-router-dom';
import { useTheme, ThemeProvider } from '@mui/material/styles';
import { apiCall } from '../../App';



function AdminCampaignApproval() {
  const [data, setData] = React.useState({});
  const [approval, setApproval] = React.useState('');

  const navigate = useNavigate();
  // const params = useParams();
  const c_id = 1;
  

  const fetchData = () => {
    // call api with data
    const options = {
      method: 'GET',
      route: '/admin/get_campaigns',
    };

    apiCall((d) => {
      console.log(d);
      setData(d);
    }, options)
      .then((res) => {
        if (res) {
          // set error msg if api call returns error

        }
      });
  }

  React.useEffect(() => {
    fetchData();
  }, []);


  const handleChange = (event) => {
    setData(event.target.value);
  }

  const handleApproval = () => {
    const options = {
      method: 'POST',
      route: "/admin/campaign/approve",
      body: JSON.stringify({
        campaign_id: c_id,
      })
    };

    apiCall((d) => {
      console.log(d);
    }, options)
      .then((res) => {
        if (res) {
          // set error msg if api call returns error

        }
      });
    
    setApproval('Approved');
    
  }

  const handleDecline = () => {
    const options = {
      method: 'POST',
      route: "/admin/campaign/decline",
      body: JSON.stringify({
        campaign_id: c_id,
      })
    };

    apiCall((d) => {
      console.log(d);
    }, options)
      .then((res) => {
        if (res) {
          // set error msg if api call returns error

        }
      });

    setApproval('Declined');
  }

  return (
    <ThemeProvider theme={useTheme()}>
      <Box 
        sx={{ 
          width: '100%', 
          height: '100%',
          display: "flex", 
          flexDirection: "column",  
          flexGrow: 1, 
          alignContent: 'center', 
          justifyContent: 'flex-start', 
          alignItems: 'Center', 
          bgcolor: '#f4f4f4' 
        }}
      >
        <Paper 
          component="main" 
          maxWidth="xs" 
          sx={{
            marginTop: '8vh',
            borderRadius: 2,
            maxWidth: '600px',
            width: '50vw',
            padding: '20px',

          }}
        >
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
          <FormControl fullWidth>
            <InputLabel id="Select Campaign">Select Campaign</InputLabel>
            <Select
              labelId="Select Campaign"
              id="select-campaign"
              value={data}
              label="Campaign"
              onChange={handleChange}
            >
              <MenuItem value={1}>One</MenuItem>
              <MenuItem value={2}>Two</MenuItem>
              {/* {analytics.map((data) => (
                <MenuItem key={data.campaign_id} value={data.campaign_id}>{data.campaign_name}</MenuItem>
              ))} */}
            </Select>
          </FormControl>

          </Box>
        </Paper>

      <Grid item xs={12} sx={{ height: '100px' }}></Grid>
      <Grid container spacing={12}>
        <Grid item xs={1}></Grid>
        <Grid item xs={7}>
          <ImageCarousel items={
              [{
                "name": "collectible image",
                "image": data.collectible_image,
                "caption": '',
              }]
            }/>
        </Grid>
        <Grid item xs={3}>
        {
          approval == ''
          ? <Paper elevation={3} sx={{ 
            height: '80%', 
            display: 'flex', 
            flexDirection: 'column', 
            rowGap: '50px', 
            justifyContent: 'center', 
            alignItems: 'center',
            marginTop: '5vh'
            }}>
             <Button variant="contained" onClick={handleApproval}>Approve Campaign</Button>
              <Button variant="contained" onClick={handleDecline}>Decline Campaign</Button>
          </Paper>
          : <Paper elevation={3} sx={{ 
            height: '80%', 
            display: 'flex', 
            flexDirection: 'column', 
            rowGap: '50px', 
            justifyContent: 'center', 
            alignItems: 'center',
            marginTop: '5vh'
            }}>
              <Typography>{approval}</Typography>
            </Paper>
        }
        </Grid>
        <Grid item xs={1}></Grid>
        <Grid item xs={1}></Grid>
        <Grid item xs={7}>
        <Paper elevation={3} sx={{ 
            width: '100%', 
            display: 'flex', 
            flexDirection: 'column', 
            justifyContent: 'center', 
            alignItems: 'center' 
            }}>
              <Container sx={{ padding: '10px' }}>
                <Typography variant='h5'>{data.collectible_name}</Typography>
                <Typography variant='h8'>Added on: {data.collectible_added_date}</Typography>
                <Typography>{data.collectible_description}</Typography>
                </Container>
          </Paper>
        </Grid>
      </Grid>
      </Box>
    </ThemeProvider>
  )
}


export default AdminCampaignApproval;