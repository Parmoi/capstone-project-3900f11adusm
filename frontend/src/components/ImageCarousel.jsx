import Carousel from 'react-material-ui-carousel';
import {
    CardContent,
    CardMedia,
    Card,
    Typography,
    Box,
} from '@mui/material'

const settings = {
    autoPlay: false,
    animation: "fade",
    indicators: true,
    duration: 500,
    navButtonsAlwaysVisible: false,
    navButtonsAlwaysInvisible: false,
    cycleNavigation: true,
    fullHeightHover: true,
    swipe: true
}

// Image carousel item
function CarouselItem(props)
{
  return (
    <Card>
      <CardMedia
        component="img"
        image={props.item.image}
        height='500'
        width='200'
      />
      <CardContent>
        <Typography variant="body2" color="text.secondary">
          {props.item.caption}
        </Typography>
      </CardContent>
    </Card>
  );
}

// Component for image carousel, displaying multiple images with included captions
const ImageCarousel = ( { items } ) => {
    return (
      <Box sx={{ height:'100%', width: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <br/>
          <Carousel
            {...settings}
          >
              {
                  items.map( (item, i) => <CarouselItem key={i} item={item} /> )
              }
          </Carousel>
          <br/>
      </Box>
    )
}

export default ImageCarousel;