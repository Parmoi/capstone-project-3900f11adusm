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
import { useParams, useNavigate } from 'react-router-dom';
import { useTheme, ThemeProvider } from '@mui/material/styles';
import { apiCall } from '../App';


const CollectiblePage = () => {
  const [data, setData] = React.useState(
      {
        "collectible_images": []
      }
  );
  const navigate = useNavigate();
  const params = useParams();
  const c_id = params.id;
  

  const fetchData = () => {
    // call api with data
    const options = {
      method: 'GET',
      route: `/collectible/get?collectible_id=${c_id}`,
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

  const handleBuy = () => {
    // navigates to buy list, with collectible id as param
    navigate(`/collectible/buy/${c_id}`);
  }

  const handleAddWantlist = () => {
    const options = {
      method: 'POST',
      route: "/wantlist/add",
      body: JSON.stringify({
        collectible_id: c_id,
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
  }

  const handleAddCollection = () => {
    const options = {
      method: 'POST',
      route: "/collection/add",
      body: JSON.stringify({
        collectible_id: c_id,
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
  }

  return (
    <ThemeProvider theme={useTheme()}>
      <Box sx={{ width: '100%', height: '100%', flexGrow: 1, alignContent: 'center', bgcolor: '#f4f4f4' }}>
      <Grid item xs={12} sx={{ height: '100px' }}></Grid>
      <Grid container spacing={12}>
        <Grid item xs={1}></Grid>
        <Grid item xs={7}>
          <ImageCarousel items={data.collectible_images}/>
        </Grid>
        <Grid item xs={3}>
          <Paper elevation={3} sx={{ 
            height: '100%', 
            display: 'flex', 
            flexDirection: 'column', 
            rowGap: '50px', 
            justifyContent: 'center', 
            alignItems: 'center',
            }}>
            <Button variant="contained" onClick={handleBuy}>See trade posts</Button>
            <Button variant="contained" onClick={handleAddWantlist}>Add to wantlist</Button>
            <Button variant="contained" onClick={handleAddCollection}>Add to collection</Button>
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

export default CollectiblePage;