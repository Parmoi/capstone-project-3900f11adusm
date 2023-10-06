import React, { useMemo, Fragment } from 'react';

import {

  MaterialReactTable,

  MRT_ToggleDensePaddingButton,

  MRT_FullScreenToggleButton,

} from 'material-react-table';

import { Box, Button, IconButton } from '@mui/material';

// stub data
const data = [
  {
    image: '',
    name: 'Homer',
    collectionName: 'Winter 2022',
    yearReleased: 1999,
    dateAdded: 1800,
  },
  {
    image: '',
    name: 'Marge',
    collectionName: 'Winter 2022',
    yearReleased: 1899,
    dateAdded: 1800,
  },
  {
    image: '',
    name: 'Bart',
    collectionName: 'Winter 2022',
    yearReleased: 1499,
    dateAdded: 1800,
  },
  {
    image: '',
    name: 'Dog',
    collectionName: 'Winter 2022',
    yearReleased: 1989,
    dateAdded: 1800,
  },
  {
    image: '',
    name: 'Lisa',
    collectionName: 'Winter 2022',
    yearReleased: 1709,
    dateAdded: 1800,
  },
  {
    image: '',
    name: 'Rando',
    collectionName: 'Winter 2022',
    yearReleased: 1909,
    dateAdded: 1801,
  },
]

// sourced from https://github.com/KevinVandy/material-react-table/blob/v1/apps/material-react-table-docs/examples/custom-top-toolbar/sandbox/src/JS.js
const WantList = () => {
  // const [data, setData] = React.useState([]);
  const columns = useMemo(
    //column definitions...
    () => [
      {
        accessorKey: 'image',
        header: 'Image Placeholder',
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

  // React.useEffect(() => {
  //   // new data acquired, refresh table
  // });


  return (
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
  );
};


export default WantList;