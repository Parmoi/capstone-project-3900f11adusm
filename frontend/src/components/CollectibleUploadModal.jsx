import React from 'react';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';


// Component for uploading collectible details modal
// Can add name and description to accompany collectible image
const CollectibleUploadModal = ({ image, setCollectible, open, handleClose }) => {
  const [name, setName] = React.useState('');
  const [description, setDescription] = React.useState('');

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
    display: 'flex',
    flexDirection: 'column',
  };

  const handleNameChange = (e) => {
    setName(e.target.value);
  }

  const handleDescriptionChange = (e) => {
    setDescription(e.target.value);
  }

  return (
    <div>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="Collectible modal"
        aria-describedby="Modal for adding collectible info"
      >
        <Box sx={style}>
          <Box 
            sx={{ 
              display: 'flex',
              justifyContent: 'center',
            }}
          >
            <img
              alt="collectible image"
              height={200}
              src={image}
              loading="lazy"
            />
          </Box>
          <Typography id="modal-modal-title" variant="h6" component="h2" mt='30px' mb='30px'>
            Add collectible details:
          </Typography>
          <TextField label="Name" onChange={handleNameChange} variant="standard" sx={{ mb: '30px' }} />
          <TextField label="Description" onChange={handleDescriptionChange} variant="standard" sx={{ mb: '30px' }} />
          <Box>
            <Button variant="contained" sx={{ float: 'right', mt: '20px' }} onClick={handleClose}>Close</Button>
            <Button variant="contained" sx={{ float: 'left', mt: '20px' }} onClick={() => {
              setCollectible({
                'image': image,
                'name': name,
                'description': description
              });
              handleClose();
              }}
            >
              Add
            </Button>
          </Box>
        </Box>
      </Modal>
    </div>
  );
  }

export default CollectibleUploadModal;