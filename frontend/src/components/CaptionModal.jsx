import React from 'react';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import InputLabel from '@mui/material/InputLabel';
import TextField from '@mui/material/TextField';


// Component for caption modal when adding images to trade post
const CaptionModal = ({ image, setImageCaptions, open, handleClose }) => {
    const [caption, setCaption] = React.useState('');

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

    const handleChange = (e) => {
        setCaption(e.target.value);
    }

    return (
        <div>
        <Modal
            open={open}
            onClose={handleClose}
            aria-labelledby="Caption modal"
            aria-describedby="Modal for adding a caption to image"
        >
            <Box sx={style}>
                <Typography id="modal-modal-title" variant="h6" component="h2" mb='30px'>
                    Add caption to image:
                </Typography>
                <Box sx={{ 
                    display: 'flex',
                    justifyContent: 'center',
                 }}>
                    <img
                        alt="collectible image"
                        height={200}
                        src={image}
                        loading="lazy"
                    />
                </Box>
            <TextField label="Caption" onChange={handleChange} variant="standard" sx={{ mb: '30px' }} />
            <Box>
                <Button variant="contained" sx={{ float: 'right', mt: '20px' }} onClick={handleClose}>Close</Button>
                <Button variant="contained" sx={{ float: 'left', mt: '20px' }} onClick={() => {
                    setImageCaptions(caption);
                    handleClose();
                    }}>Add</Button>
            </Box>
            </Box>
        </Modal>
        </div>
    );
    }

export default CaptionModal;