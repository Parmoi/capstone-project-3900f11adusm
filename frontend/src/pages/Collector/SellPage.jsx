import * as React from 'react';
import PostStepper from "../../components/PostStepper";
import Typography from '@mui/material/Typography';
import { Box, Button, Grid } from '@mui/material';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import TextField from '@mui/material/TextField';
import Alert from '@mui/material/Alert';

import { apiCall } from '../../App';
import WidgetUpload from '../../components/WidgetUpload';
import { useNavigate } from 'react-router-dom';
import CaptionModal from '../../components/CaptionModal';
import ImageList from '../../components/ImageCaptionList';

// stepper steps
const steps = ['Select collectible', 'Add title', 'Enter a description', 'Add images', 'Post listing'];

// Displays page in which user can put up a collectible that they own, for trade
// Allows user to select collectible they want to trade from their collection list, add title, description and images (with captions) for post
// Last step shows the post listing details which they can verify before posting
const SellPage = () => {
const [collectionID, setCollectibleID] = React.useState('');
const [collectibleName, setCollectibleName] = React.useState('');
const [title, setTitle] = React.useState('');
const [description, setDescription] = React.useState('');
const [collectibles, setCollectibles] = React.useState([]);
const [images, setImages] = React.useState([]);
const [isTitleAdded, setIsTitleAdded] = React.useState(false);
const [isDescAdded, setIsDescAdded] = React.useState(false);
const [emptyCollection, setEmptyCollection] = React.useState(false);
const [offerOpen, setOfferOpen] = React.useState(false);
const handleOfferClose = () => setOfferOpen(false);

const navigate = useNavigate();

const fetchData = () => {
    // fetches all collectibles in user's collection
    const options = {
      method: 'GET',
      route: "/collection/get",
    };

    apiCall((d) => {
      setCollectibles(d.collection);
      setEmptyCollection(d.collection.length === 0);
    }, options);
}

React.useEffect(() => {
  fetchData();
}, []);

// Component for selecting collectible from user collection
const SelectCollectible = () => {

  const handleChange = (id, name) => {
    setCollectibleID(id);
    setCollectibleName(name);
  }

    return (
    <Box sx={{ height: '100%' }}>
      <Typography variant='h5' mb='50px'>Select collectible you would like to trade/sell</Typography>
      <FormControl fullWidth>
        <InputLabel>Collectible</InputLabel>
        <Select
          id='tradeCollectible'
          value={collectionID}
          label="Collectible"
        >
        {/* Render menu items for each collectible name in user's collection */}
        {collectibles.map((collectible) => {
          return (
            <MenuItem
              value={collectible.id}
              onClick={() => handleChange(collectible.id, collectible.name)}
            >
              {collectible.name}
            </MenuItem>)
          })
        }
        {emptyCollection ? <Alert severity='error'>No collectibles in collection!</Alert> : <></>}
        </Select>
      </FormControl>
    </Box>
  );
}

// Component for adding title to tradepost
const AddTitle = () => {
  const postTitle = (e) => {
    e.preventDefault();
    const data = new FormData(e.currentTarget);
    setIsTitleAdded(true);
    setTitle(data.get('title'));
  }

  return (
    <Box component="form" onSubmit={postTitle} sx={{ height: '100%' }}>
      <Typography variant='h5' mb='50px'>Add a title for your post</Typography>
      <TextField id='title' name='title' label="Title" variant="standard" onChange={() => setIsTitleAdded(false)} />
      <Button type="submit" variant='contained' sx={{ m: 1, ml: '10px' }}>ADD</Button>
      {isTitleAdded ? <Alert severity='success'>Added title!</Alert> : ''}
    </Box>
  );
}

// Component for adding description to tradepost
const CollectibleDescription = () => {
  const postDescription = (e) => {
    e.preventDefault();
    const data = new FormData(e.currentTarget);
    setIsDescAdded(true);
    setDescription(data.get('description'));
  }

  return (
    <Box component="form" onSubmit={postDescription} sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Typography variant='h5' mb='50px'>Add a description of your collectible</Typography>
      <TextField
        name="description"
        id="outlined-multiline-static"
        label="Description"
        multiline
        placeholder='Add description here...'
        rows={3}
        onChange={() => setIsDescAdded(false)}
      />
      {isDescAdded ? <Alert severity='success'>Added description!</Alert> : <></>}
      <Button
        variant='contained'
        type="submit"
        sx={{ mt: '10px' }}
      >
        ADD
      </Button>
    </Box>
  );
}

// Component for adding images of collectible to tradepost
const AddImages = () => {
  const handleImageURL = (url) => {
    const newList = images.concat({'image': url, 'caption': ''});
    setImages(newList);
    setOfferOpen(true);
  }

  return (
    <Box sx={{ height: '100%' }}>
      {/* Gets last image and adds caption */}
      <CaptionModal image={images.length === 0 ? '' : images[images.length - 1].image} setImageCaptions={(caption) => {
        images.at(-1).caption = caption;
      }} open={offerOpen} handleClose={handleOfferClose}/>
      <Typography variant='h5' mb='50px'>Add images of your collectible:</Typography>
      <WidgetUpload onSuccess={handleImageURL} />
    </Box>
  );
}

// Component for checking and posting tradepost
const PostListing = () => {
  const postData = () => {
    // api call to post new tradepost
    const options = {
      method: "POST",
      route: "/trade/post",
      body: JSON.stringify({
          collection_id: collectionID,
          post_images: images,
          post_title: title,
          post_description: description,
      }),
    };

    apiCall(() => {
      navigate('/');
    }, options);
  }

  // checks for errors in inputs given
  function dataError() {
    return (collectibleName === '' || title === '' || description === '' || images.length === 0);
  }

  return (
    <Box sx={{ height: '100%' }}>
      <Typography variant='h5' mb='20px'>Check new trade post</Typography>
        <Grid container spacing={12} sx={{ display: 'flex', justifyContent: 'center' }}>
          <Grid item xs={6}>
            <Box sx={{ display: 'flex', flexDirection: 'column' }}>
              <TextField label="Collectible Name" variant="standard" aria-disabled value={collectibleName} sx={{ mb: '50px' }} />
              <TextField label="Title" variant="standard" aria-disabled value={title} sx={{ mb: '50px' }} />
              <TextField
                id="outlined-multiline-static"
                label="Description"
                multiline
                rows={3}
                aria-disabled
                value={description}
                sx={{ mb: '10px' }}
              />
              {dataError() ? <Alert severity='error' sx={{ mb: '10px' }}>Missing some fields!</Alert> : <></>}
            </Box>
          </Grid>
          <Grid item xs={6}>
            <ImageList itemData={images}/>
          </Grid>
          <Grid item xs={3}>
            <Button variant='contained' disabled={dataError()} onClick={postData}>POST</Button>
          </Grid>
        </Grid>
    </Box>
  );
}

const stepperContent = [
  <SelectCollectible />,
  <AddTitle />,
  <CollectibleDescription />,
  <AddImages />,
  <PostListing />,
]

return (
  <PostStepper steps={steps} stepperContent={stepperContent} />
);
}

export default SellPage;