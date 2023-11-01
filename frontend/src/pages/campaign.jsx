import React, { useMemo } from 'react';

import {

  MaterialReactTable,

  MRT_ToggleDensePaddingButton,

  MRT_FullScreenToggleButton,

} from 'material-react-table';

import { Box, Button,Typography} from '@mui/material';
import { useLocation } from 'react-router-dom';
import Timer from '../components/Timer'

// stub data
const data = [
  {
    image: 'https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg',
    name: 'Homer',
    collectionName: 'Winter 2022',
    yearReleased: 1999,
    dateAdded: 1800,
  },
  {
    image: 'https://tse4.mm.bing.net/th?id=OIP.e4tAXeZ6G0YL4OE5M8KTwAHaMq&pid=Api',
    name: 'Marge',
    collectionName: 'Winter 2022',
    yearReleased: 1899,
    dateAdded: 1800,
  },
  {
    image: 'https://tse2.mm.bing.net/th?id=OIP.j7EknM6CUuEct_kx7o-dNQHaMN&pid=Api',
    name: 'Bart',
    collectionName: 'Winter 2022',
    yearReleased: 1499,
    dateAdded: 1800,
  },
  {
    image: 'https://tse3.mm.bing.net/th?id=OIP.6761X25CX3UUjklkDCnjSwHaHa&pid=Api',
    name: 'Dog',
    collectionName: 'Winter 2022',
    yearReleased: 1989,
    dateAdded: 1800,
  },
  {
    image: 'https://tse3.mm.bing.net/th?id=OIP.JqWjPHsW5aJIZDnPYMGovQHaJQ&pid=Api',
    name: 'Lisa',
    collectionName: 'Winter 2022',
    yearReleased: 1709,
    dateAdded: 1800,
  },
  {
    image: 'https://tse1.mm.bing.net/th?id=OIP.qVV8kcLdcLysZ5OOCzhKLAHaF7&pid=Api',
    name: 'Rando',
    collectionName: 'Winter 2022',
    yearReleased: 1909,
    dateAdded: 1801,
  },
]

// sourced from https://github.com/KevinVandy/material-react-table/blob/v1/apps/material-react-table-docs/examples/custom-top-toolbar/sandbox/src/JS.js
const Campaign = () => {
  // const [data, setData] = React.useState([]);
  const columns = useMemo(
    //column definitions...
    () => [
      {
        accessorKey: 'image',
        header: 'Image Placeholder',
        Cell: ({ row }) => (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '1rem',
            }}
          >
            <img
              alt="collectible image"
              height={50}
              src={row.original.image}
              loading="lazy"
            />
          </Box>

        ),
        enableColumnActions: false,
        enableColumnFilter: false,
      },
      {
        accessorKey: 'name',
        header: 'Name',
      },
      {
        accessorKey: 'collectionName',
        header: 'Collection Name',
      },
      {
        accessorKey: 'yearReleased',
        header: 'Year',
      },
      {
        accessorKey: 'dateAdded',
        header: 'Date Added',
      },
    ],
    [],
    //end
  );

  const location = useLocation();
  // const query = location.state?.



  return (
    <>
      <Box sx={{ my: 0, }}>
        <Typography variant="h2" align="center" color="#2c3e50" gutterBottom>
          {location.state?.campaign_name}
        </Typography>
        <Timer startDate={location.state?.start_date} endDate={location.state?.end_date}></Timer>
      </Box>
      <MaterialReactTable
        title="Wantlist"
        columns={columns}
        data={data}
        enableRowSelection
        positionToolbarAlertBanner="bottom" //show selected rows count on bottom toolbar

        //add custom action buttons to top-left of top toolbar

        renderBottomToolbarCustomActions={({ table }) => (

          <Box sx={{ display: 'flex', gap: '1rem', p: '4px' }}>
            <Button
              color="secondary"
              disabled={!table.getIsSomeRowsSelected()}
              onClick={() => {
                // api call to backend
                // setData to new data
                alert('Move to collections');
              }}
              variant="contained"
            >
              Move to collections
            </Button>

            <Button
              color="error"
              disabled={!table.getIsSomeRowsSelected()}
              onClick={() => {
                // api call to backend
                // setData to new data
                alert('Delete selected collectibles');
              }}
              variant="contained"
            >
              Delete selected
            </Button>
          </Box>

        )}

        //customize built-in buttons in the top-right of top toolbar

        renderToolbarInternalActions={({ table }) => (

          <Box>
            {/* add custom button to print table  */}
            <MRT_ToggleDensePaddingButton table={table} />
            <MRT_FullScreenToggleButton table={table} />
          </Box>
        )}

      />
    </>
  );
};


export default Campaign;