import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography } from '@mui/material';

// Component for collectible image, displays the name and image
// Clicking on this component takes user to the collectible page
const CollectibleImage = ({ id, name, image }) => {
  const navigate = useNavigate();
  function handleClick() {
    navigate(`/collectible/${id}`);
  }

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '1rem',
        flexDirection: 'column',
        cursor: 'pointer'
      }}
      onClick={handleClick}
      >
      <Typography variant="h8">{name}</Typography>
      <img
        alt="collectible image"
        height={100}
        src={image}
        loading="lazy"
      />
    </Box>
  );
}

export default CollectibleImage;