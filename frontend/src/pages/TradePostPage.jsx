import React from 'react';
import ImageCarousel from '../components/ImageCarousel';
import {
    Grid,
    Button,
    Typography,
    Box,
    Container,
    Paper,
} from '@mui/material'
import { useParams } from 'react-router-dom';
import { useTheme, ThemeProvider } from '@mui/material/styles';
import { apiCall } from '../App';
import ProfileAvatar from '../components/ProfileAvatar';
import OfferModal from '../components/OfferModal'


const TradePostPage = () => {
  const [data, setData] = React.useState(
      {
        "post_images": []
      }
  );
  const [offerOpen, setOfferOpen] = React.useState(false);
  const handleOfferClose = () => setOfferOpen(false);
    
  const params = useParams();
  const tradepost_id = params.id;
  

  const fetchData = () => {
    // call api with data
    const options = {
      method: 'GET',
      route: `/trade/view?trade_post_id=${tradepost_id}`,
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

  React.useEffect(() => {
    fetchData();
  }, []);

  const handleOffer = () => {
    setOfferOpen(true);
  }

  return (
    <ThemeProvider theme={useTheme()}>
      <Box sx={{ width: '100%', height: '100%', flexGrow: 1, alignContent: 'center', bgcolor: '#f4f4f4' }}>
      <OfferModal tradeId={tradepost_id} open={offerOpen} handleClose={handleOfferClose}/>
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
            <Typography variant='h6' color='grey'>{data.trader_location}</Typography>
            <ProfileAvatar 
              userId={data.trader_id} 
              image={data.trader_avatar} 
              name={data.trader_name}
            />
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

export default TradePostPage;