import React from 'react';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { apiCall } from '../App';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import TextField from '@mui/material/TextField';




// Component for offer modal
const OfferModal = ({ tradeId, open, handleClose }) => {
    const [offerTitle, setOfferTitle] = React.useState('');
    const [collectibleID, setCollectibleID] = React.useState(0);
    const [description, setDescription] = React.useState('');
    const [image, setImage] = React.useState('');
    const [collectibles, setCollectibles] = React.useState([]);

    const fetchData = () => {
        // call api with data
        const options = {
        method: 'GET',
        route: "/collection/get",
        };

        apiCall((d) => {
        setCollectibles(d.collection);
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

    const style = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 400,
        bgcolor: 'background.paper',
        border: '2px solid #000',
        boxShadow: 24,
        p: 4,
    };

    const handleMakeOffer = () => {
      // call api with data
      // const options = {
      //   method: 'POST',
      //   route: "/exchange/makeoffer",
      //   body: JSON.stringify({
      //     "trade_id": tradeId,
      //     "offer_img": image,
      //     "offer_title": offerTitle,
      //     "collectible_id": collectibleID,
      //     "description": description,
      //   })
      // };

      // console.log(options.body);

      // apiCall((d) => {}, options)
      // .then((res) => {
      //     if (res) {
      //     // set error msg if api call returns error

      //     }
      // });
      handleClose();
  }

    const renderMenuItems = (collectibles) => {
        return collectibles.map((collectible) => { 
            <MenuItem 
                value={collectible['id']}
                onClick={() => handleIdChange(collectible['id'])}
            >
                {collectible["name"]}
            </MenuItem>
        }
        );
    }

    const handleTitleChange = (title) => {
        setOfferTitle(title);
    }

    const handleIdChange = (id) => {
      setCollectibleID(id);
    }

    const handleDescChange = (desc) => {
      setDescription(desc);
    }

    const handleImageChange = (image) => {
      setImage(image);
    }
  
    return (
      <div>
        <Modal
          open={open}
          onClose={handleClose}
          aria-labelledby="Offer modal"
          aria-describedby="Modal for making an offer"
        >
          <Box sx={style}>
            <Typography id="modal-modal-title" variant="h6" component="h2" mb='30px'>
                Make an offer:
            </Typography>
            <FormControl fullWidth>
            <InputLabel>Collectible</InputLabel>
            <Select
                id='tradeCollectible'
                value={collectibleID}
                label="Collectible"
            >
                {renderMenuItems(collectibles)}
            </Select>
            <TextField label="Title" onBlur={handleTitleChange} variant="standard" sx={{mb: '30px'}}/>
            <TextField
              id="outlined-multiline-static"
              label="Description"
              multiline
              placeholder='Add description here...'
              rows={3}
              onBlur={handleDescChange}
              sx={{mb: '30px'}}
              />
            <Box sx={{}}>
              <input type="file" multiple accept=".jpg, .jpeg, .png" onChange={handleImageChange}/>
              <Button>Upload</Button>
            </Box>
            </FormControl>
            <Button variant="contained" sx={{ float: 'right', mt: '20px' }} onClick={handleClose}>Close</Button>
            <Button variant="contained" sx={{ float: 'left', mt: '20px' }} onClick={handleMakeOffer}>Trade</Button>
          </Box>
        </Modal>
      </div>
    );
  }
  
  export default OfferModal;