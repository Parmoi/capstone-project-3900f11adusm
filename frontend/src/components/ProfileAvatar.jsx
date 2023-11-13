import React from 'react';

import { Box } from '@mui/material';
import Avatar from '@mui/material/Avatar';
import { useNavigate } from 'react-router-dom';


const ProfileAvatar = ({ userId, image }) => {
    const navigate = useNavigate();

    function handleClick() {
        navigate(`/profile/${userId}`);
    }

    return (
        <Box
            sx={{
                display: 'flex',
                gap: '1rem',
            }}
        >
        <Avatar sx={{ cursor: 'pointer' }} onClick={handleClick} alt="Trader Profile" src={image} />
        </Box>)
    ;
}

export default ProfileAvatar;