import * as React from 'react';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import ImageListItemBar from '@mui/material/ImageListItemBar';
import ListSubheader from '@mui/material/ListSubheader';
import IconButton from '@mui/material/IconButton';
import InfoIcon from '@mui/icons-material/Info';

// Displays collectibles as image list with name and description
// Sourced from https://mui.com/material-ui/react-image-list/
export default function ImageCollectiblesList({ itemData }) {
  return (
    <ImageList sx={{ width: 500, height: 300 }}>
      <ImageListItem key="Subheader" cols={2}>
        <ListSubheader component="div">Collectibles uploaded</ListSubheader>
      </ImageListItem>
      {itemData.map((item) => (
        <ImageListItem key={item.image}>
          <img
            srcSet={`${item.image}?w=248&fit=crop&auto=format&dpr=2 2x`}
            src={`${item.image}?w=248&fit=crop&auto=format`}
            alt={item.name}
            loading="lazy"
          />
          <ImageListItemBar
            title={item.name}
            subtitle={item.description}
            actionIcon={
              <IconButton
                sx={{ color: 'rgba(255, 255, 255, 0.54)' }}
                aria-label={`info about ${item.name}`}
              >
                <InfoIcon />
              </IconButton>
            }
          />
        </ImageListItem>
      ))}
    </ImageList>
  );
}
