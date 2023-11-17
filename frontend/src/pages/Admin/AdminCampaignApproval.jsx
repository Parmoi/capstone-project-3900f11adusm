import React, { useState, useEffect } from 'react';
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

import { useTheme, ThemeProvider } from '@mui/material/styles';
import { apiCall } from '../../App';


function AdminCampaignApproval() {
  const [data, setData] = useState([]);
  const [campaign, setCampaign] = useState(0);
  const [campaignDetails, setCampaignDetails] = useState({});

  const [approval, setApproval] = useState(false);
  const [approvalStatus, setApprovalStatus] = useState('')
  const [collectibles, setCollectibles] = useState([{
    "name": "Nothing",
    "image": "https://th.bing.com/th/id/OIP.cwB1TLRCZXJwp3ngh94G2gAAAA?pid=ImgDet&rs=1",
    "caption": "No Campaign has been selected"
  }]);

  const fetchInfo = () => {
    const options = {
      method: 'GET',
      route: '/admin/get_campaigns',
    };

    apiCall((d) => {
      setData(d["campaigns"]);
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


  const handleChange = (event) => {
    setCampaign(event.target.value);
    setApproval(data.filter((x) => x.campaign_id == event.target.value)[0].approved);
    if (approval) { setApprovalStatus('Approved'); }
    else { setApprovalStatus(''); }

    setCollectibles(data.filter((x) => x.campaign_id == event.target.value)[0].collection_list);
    setCampaignDetails(data.filter((x) => x.campaign_id == event.target.value)[0]);
  }

  const handleApproval = () => {
    const options = {
      method: 'POST',
      route: "/admin/campaign/approve",
      body: JSON.stringify({
        campaign_id: Number(campaign),
      })
    };

    apiCall(() => {
    }, options)
      .then((res) => {
        if (res) {
          // set error msg if api call returns error

        }
      });
    
    fetchInfo();
    setApproval('Approved');
    
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
            <InputLabel id="Campaign">Campaign</InputLabel>
            <Select
              labelId="Campaign"
              id="campaign"
              key={campaign}
              value={campaign}
              label="Campaign"
              onChange={handleChange}
            >
              {data.map((data) => (
                <MenuItem key={data.campaign_id} value={data.campaign_id}>{data.campaign_name}</MenuItem>
              ))}
            </Select>
          </FormControl>

          </Box>
        </Paper>

      <Grid item xs={12} sx={{ height: '100px' }}></Grid>
      <Grid container spacing={12}>
        <Grid item xs={1}></Grid>
        <Grid item xs={7}>
          <ImageCarousel items={collectibles}/>
        </Grid>
        <Grid item xs={3}>
        {
          approvalStatus == ''
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
              <Typography>{approvalStatus}</Typography>
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
            alignItems: 'center',
            marginBottom: '5vh',
            }}>
              <Container sx={{ padding: '10px', }}>
                <Typography variant='h5'>{campaignDetails.campaign_name}</Typography>
                <Typography variant='h8'>Proposed Start Date: {campaignDetails.campaign_start_date}</Typography>
                <Typography>{campaignDetails.campaign_description}</Typography>
                </Container>
          </Paper>
        </Grid>
      </Grid>
      </Box>
    </ThemeProvider>
  )
}


export default AdminCampaignApproval;