import React from 'react';

import { Box, Typography } from '@mui/material';
import Avatar from '@mui/material/Avatar';
import { useNavigate } from 'react-router-dom';


const ProfileAvatar = ({ image }) => {
    const navigate = useNavigate();
    
    function handleClick() {
        
    }

    return (
        <Box
            sx={{
                display: 'flex',
                gap: '1rem',
            }}
        >
        <Avatar onClick={handleClick} alt="Trader Profile" src={image} />
        </Box>)
    ;
}

export default ProfileAvatar;