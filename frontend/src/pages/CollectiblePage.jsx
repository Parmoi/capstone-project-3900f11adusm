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
import { useTheme, ThemeProvider } from '@mui/material/styles';
import { apiCall } from '../App';

// stub images
// const images = [
//   {
//       name: "Lego",
//       caption: "Random lego.",
//       image: "https://tse3.mm.bing.net/th?id=OIP.SwCSPpmwihkM2SUqh7wKXwHaFG&pid=Api"
//   },
//   {
//     name: "More legos",
//     caption: "More lego.",
//     image: "https://content.api.news/v3/images/bin/f82665f51acc50360bbc70901f3563a1"
//   },
//   {
//     name: "Collectibles",
//     caption: "Random collectibles.",
//     image: "https://tse1.mm.bing.net/th?id=OIP.Cs29HRbrYZhSfWdUdgRgMAHaEK&pid=Api"
//   },
// ]

const CollectiblePage = () => {
  const [data, setData] = React.useState([]);

  const fetchData = () => {
    // call api with data
    const options = {
      method: 'GET',
      route: "/collectible/get",
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
            alignItems: 'center' 
            }}>
            <Button variant="contained">Buy item</Button>
            <Button variant="contained">Add to wantlist</Button>
            <Button variant="contained">Add to collection</Button>
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