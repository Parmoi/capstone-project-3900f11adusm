import * as React from 'react';
import PropTypes from 'prop-types';
import LinearProgress from '@mui/material/LinearProgress';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import List from '@mui/material/List';

import { Divider } from '@mui/material';

function LinearProgressWithLabel(props) {
  return (
    <Box sx={{ display: 'flex', alignItems: 'center' }}>
      <Box sx={{ width: '100%', mr: 1 }}>
        <LinearProgress variant="determinate" sx={{margin: "8px", height: 10, borderRadius: 5}} {...props} />
      </Box>
      <Box sx={{ minWidth: 35 }}>
        <Typography variant="body2" color="text.secondary">{`${Math.round(
        props.value,
        )}%`}</Typography>
      </Box>
    </Box>
  );
}

LinearProgressWithLabel.propTypes = {
  value: PropTypes.number.isRequired,
};


const CollectionCompletion = ({style}) => {
  return (
    <Box sx={style} p="8px">
      <Typography variant="h5" sx={{margin: "8px"}}>Collection Completion</Typography>
      <List sx={{alignItems: "center"}} p={8}>
        <Typography sx={{margin: "8px"}}>Campaign Name</Typography>
        <LinearProgressWithLabel value={50} />
        <Divider sx={{margin: "8px"}}/>
        <Typography sx={{margin: "8px"}}>Campaign Name</Typography>
        <LinearProgressWithLabel value={50} />
        <Divider sx={{margin: "8px"}}/>
        <Typography sx={{margin: "8px"}}>Campaign Name</Typography>
        <LinearProgressWithLabel value={50} />
      </List> 
    </Box>
  );
};

export default CollectionCompletion;