import React, { useState } from 'react';
import ImageCarousel from '../components/ImageCarousel';
import {
    Grid,
    Button,
    Typography,
    Box,
    Container,
    Paper,
} from '@mui/material'
import Divider from '@mui/material/Divider';
import { useParams, useNavigate } from 'react-router-dom';
import { useTheme, ThemeProvider } from '@mui/material/styles';
import { apiCall } from '../App';
import Avatar from '@mui/material/Avatar';


const CollectiblePage = () => {
  const [data, setData] = React.useState(
      {
        "post_images": []
      }
  );
  const navigate = useNavigate();
  const params = useParams();
  const tradepost_id = params.id;
  

  const fetchData = () => {
    // call api with data
    const options = {
      method: 'GET',
      route: `/trade/get?collectible_id=${tradepost_id}`,
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

  const handleOffer = () => {
    // insert offer page
  }

  return (
    <ThemeProvider theme={useTheme()}>
      <Box sx={{ width: '100%', height: '100%', flexGrow: 1, alignContent: 'center', bgcolor: '#f4f4f4' }}>
      <Grid item xs={12} sx={{ height: '100px' }}></Grid>
      <Grid container spacing={12}>
        <Grid item xs={1}></Grid>
        <Grid item xs={7}>
          <ImageCarousel items={data.post_images}/>
        </Grid>
        <Grid item xs={3}>
          <Paper elevation={3} sx={{ 
            height: '100%', 
            display: 'flex', 
            flexDirection: 'column', 
            rowGap: '50px', 
            justifyContent: 'center', 
            alignItems: 'center' 
            }}>
            <Typography variant='h5'>{data.post_trader}</Typography>
            <Typography variant='h6' color='grey'>{data.trader_location}</Typography>
            <Box component="span">
                <Avatar 
                variant="outlined"
                alt="Trader avatar"
                src={data.trader_avatar ? data.trader_avatar : ''}
                display="flex"
                sx={{ width: 150, height: 150, marginTop: "16px", fontSize: "60px"}}
                />
            </Box>
            <Button variant="contained" onClick={handleOffer}>Make offer</Button>
          </Paper>
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
                <Typography variant='h5'>{data.post_title}</Typography>
                <Typography>Added on: {data.post_created}</Typography>
                <Typography>{data.post_description}</Typography>
                </Container>
          </Paper>
        </Grid>
      </Grid>
      </Box>
    </ThemeProvider>
  )
}

export default CollectiblePage;