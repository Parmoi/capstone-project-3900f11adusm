import React from 'react';

import { Box, Typography } from '@mui/material';
import Avatar from '@mui/material/Avatar';
import { useNavigate } from 'react-router-dom';


const ProfileAvatar = ({ userId, image, name }) => {
    const navigate = useNavigate();

    function handleClick() {
        navigate(`/profile/${userId}`);
    }

    return (
        <Box
            onClick={handleClick}
            sx={{
                display: 'flex',
                gap: '1rem',
                alignItems: 'center',
                cursor: 'pointer',
            }}
        >
            <Avatar alt="Trader Profile" src={image} />
            <Typography variant="h8">{name}</Typography>
        </Box>)
    ;
}

export default ProfileAvatar;