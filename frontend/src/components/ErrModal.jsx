import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';

// Component for error modal
const ErrModal = ({ errMsg, open, handleClose }) => {
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
  
    return (
      <div>
        <Modal
          open={open}
          onClose={handleClose}
          aria-labelledby="Error modal"
          aria-describedby="An error has occurred"
        >
          <Box sx={style}>
            <Typography id="modal-modal-title" variant="h6" component="h2">
              An error has occurred
            </Typography>
            <Typography id="modal-modal-description" sx={{ mt: 2 }}>
              {errMsg}
            </Typography>
            <Button variant="contained" sx={{ float: 'right' }} onClick={handleClose}>Close</Button>
          </Box>
        </Modal>
      </div>
    );
  }

  export default ErrModal;