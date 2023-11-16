import React from 'react';
import ImageCarousel from '../../components/ImageCarousel';
import {
    Grid,
    Button,
    Typography,
    Box,
    Container,
    Paper,
    Divider,
    ListItem,
    List,
} from '@mui/material'

import { useParams, useNavigate } from 'react-router-dom';
import { useTheme, ThemeProvider } from '@mui/material/styles';
import { apiCall } from '../../App';

// Page which displays information about collectible including name, image, add date and description
// Contains buttons which allow users to see trade posts, add collectible to wantlist and collection
const CollectiblePage = () => {
  const [data, setData] = React.useState({});
  const navigate = useNavigate();
  const params = useParams();
  const c_id = params.id;
  
  const fetchData = () => {
    // fetches collectible information to be displayed
    const options = {
      method: 'GET',
      route: `/collectible/get?collectible_id=${c_id}`,
    };

    apiCall((d) => {
      setData(d);
    }, options);
  }

  React.useEffect(() => {
    fetchData();
  }, []);

  const handleBuy = () => {
    // navigates to buy list, with collectible id as param
    navigate(`/collectible/buy/${c_id}`);
  }

  const handleAddWantlist = () => {
    // api call to add collectible to wantlist
    const options = {
      method: 'POST',
      route: "/wantlist/add",
      body: JSON.stringify({
        collectible_id: c_id,
      })
    };

    apiCall(() => {
    }, options);
  }

  const handleAddCollection = () => {
    // api call to add collectible to collection list
    const options = {
      method: 'POST',
      route: "/collection/add",
      body: JSON.stringify({
        collectible_id: c_id,
      })
    };

    apiCall(() => {
    }, options);
  }

  return (
    <ThemeProvider theme={useTheme()}>
      <Box sx={{ width: '100%', height: '100%', flexGrow: 1 }}>
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
        <Paper elevation={3} 
          sx={{ 
              width: '100%', 
              display: 'flex', 
              flexDirection: 'column', 
              justifyContent: 'center', 
              alignItems: 'center' 
          }}
        >
        <List sx={{ display: 'flex', flexDirection: 'column', alignContent: 'flex-start', width: '100%' }}>
          <ListItem>
            <Typography variant='h5'>{data.collectible_name}</Typography>
          </ListItem>
          <ListItem>
            <Typography variant='h8'>Added on: {data.collectible_added_date}</Typography>
          </ListItem>
          <Divider variant="middle"/>
          <ListItem>
            <Typography>{data.collectible_description}</Typography>
          </ListItem>
        </List>
        </Paper>
        </Grid>
      </Grid>
      </Box>
    </ThemeProvider>
  )
}

export default CollectiblePage;