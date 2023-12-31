import * as React from 'react';
import PostStepper from "../../components/PostStepper";
import Typography from '@mui/material/Typography';
import { Box, Button, Grid } from '@mui/material';
import TextField from '@mui/material/TextField';
import Alert from '@mui/material/Alert';

import { apiCall } from '../../App';
import WidgetUpload from '../../components/WidgetUpload';
import { useNavigate } from 'react-router-dom';
import CollectibleUploadModal from '../../components/CollectibleUploadModal';
import ImageCollectiblesList from '../../components/ImageCollectiblesList';

import dayjs from 'dayjs';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import moment from 'moment';

// stepper steps
const steps = ['Add name', 'Enter a description', 'Add start and end dates', 'Add an image', 'Add new collectibles', 'Post campaign'];

// Page for posting campaign as a manager
// Can input campaign name, description, image, start and end date, and upload new collectibles that are associated with the campaign
const ManagerPost = () => {
  const [name, setName] = React.useState('');
  const [description, setDescription] = React.useState('');
  const [startDate, setStartDate] = React.useState(dayjs());
  const [endDate, setEndDate] = React.useState(dayjs());
  const [image, setImage] = React.useState('');
  const [collectibles, setCollectibles] = React.useState([]);
  const [isNameAdded, setIsNameAdded] = React.useState(false);
  const [isDescAdded, setIsDescAdded] = React.useState(false);
  const [modalOpen, setModalOpen] = React.useState(false);
  const handleModalClose = () => setModalOpen(false);
  
  const navigate = useNavigate();

  // Component for adding campaign name
  const AddName = () => {
    const postName = (e) => {
      e.preventDefault();
      const data = new FormData(e.currentTarget);
      setIsNameAdded(true);
      setName(data.get('name'));
    }

    return (
      <Box component="form" onSubmit={postName} sx={{ height: '100%' }}>
        <Typography variant='h5' mb='50px'>Add a name for your campaign</Typography>
        <TextField id='name' name='name' label="Name" variant="standard" onChange={() => setIsNameAdded(false)} />
        <Button type="submit" variant='contained' sx={{ m: 1, ml: '10px' }}>ADD</Button>
        {isNameAdded ? <Alert severity='success'>Added name!</Alert> : ''}
      </Box>
    );
  }

  // Component for adding campaign description
  const CampaignDescription = () => {
    const postDescription = (e) => {
      e.preventDefault();
      const data = new FormData(e.currentTarget);
      setIsDescAdded(true);
      setDescription(data.get('description'));
    }

    return (
      <Box component="form" onSubmit={postDescription} sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <Typography variant='h5' mb='50px'>Add a description of your Campaign</Typography>
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

  // Component for adding start and end dates
  const AddDates = () => {
    const handleStartChange = (e) => {
      setStartDate(e.$d);
    }

    const handleEndChange = (e) => {
      setEndDate(e.$d);
    }

    return (
      <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column', rowGap: '70px' }}>
        <Typography variant='h5'>Add dates for campaign</Typography>
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <DatePicker value={dayjs(startDate)} disablePast label="Start date" format="DD/MM/YYYY" onChange={handleStartChange}/>
          <DatePicker value={dayjs(endDate)} disablePast label="End date" format="DD/MM/YYYY" onChange={handleEndChange} minDate={dayjs(startDate)}/>
        </LocalizationProvider>
      </Box>
    );
  }

  // Component for adding campaign image
  const AddImage = () => {
    const handleImageURL = (url) => {
      setImage(url);
    }

    return (
      <Box sx={{ height: '100%', display: 'flex', justifyContent: 'center', flexDirection: 'column' }}>
        <Typography variant='h5' mb='50px'>Add your campaign image:</Typography>
        { image !== '' ? <Box
          component="img"
          sx={{
              height: 350,
              width: 350,
          }}
          alt="Campaign image."
          src={image}
        /> 
        : <></>}
        <WidgetUpload onSuccess={handleImageURL} />
      </Box>
    );
  }

  // Component for uploading collectibles
  const AddCollectibles = () => {
    const handleImageURL = (url) => {
      setImage(url);
      setModalOpen(true);
    }

    return (
      <Box sx={{ height: '100%' }}>
        <CollectibleUploadModal image={image} setCollectible={(collectible) => {
          const newList = collectibles.concat(collectible);
          setCollectibles(newList);
        }} open={modalOpen} handleClose={handleModalClose}/>
        <Typography variant='h5' mb='50px'>Add new collectibles:</Typography>
        <WidgetUpload onSuccess={handleImageURL} />
      </Box>
    );
  }

  // Component for displaying post details and allow for posting campaign
  const PostCampaign = () => {
    const postData = () => {
      // api call to post new campaign
      const options = {
        method: "POST",
        route: "/campaign/register",
        body: JSON.stringify({
          name: name,
          image: image,
          desc: description,
          start: moment(startDate).format('DD/MM/YYYY'),
          end: moment(endDate).format('YY/MM/YYYY'),
          collectibles_list: collectibles,
        }),
      };

      apiCall(() => {
          navigate('/');
      }, options);
    }

    function dataError() {
      return (name === '' || image === '' || description === '' || collectibles.length === 0 );
    }

    return (
      <Box sx={{ height: '100%' }}>
        <Typography variant='h5' mb='50px'>Check new campaign post</Typography>
        <Grid container spacing={12} sx={{ display: 'flex', justifyContent: 'center' }}>
          <Grid item xs={6}>
            <Box sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
              <TextField label="Campaign Name" variant="standard" aria-disabled value={name} sx={{ mb: '50px' }} />
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
            <ImageCollectiblesList itemData={collectibles}/>
          </Grid>
          <Grid item xs={3}>
            <Button variant='contained' disabled={dataError()} onClick={postData}>POST</Button>
          </Grid>
        </Grid>
      </Box>
    );
  }

  const stepperContent = [
    <AddName />,
    <CampaignDescription />,
    <AddDates />,
    <AddImage />,
    <AddCollectibles />,
    <PostCampaign />,
  ]

  return (
    <PostStepper steps={steps} stepperContent={stepperContent} />
  );
}


export default ManagerPost;