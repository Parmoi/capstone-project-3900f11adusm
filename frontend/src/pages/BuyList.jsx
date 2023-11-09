import React, { useMemo, Fragment } from 'react';

import {

  MaterialReactTable,

  MRT_ToggleDensePaddingButton,

  MRT_FullScreenToggleButton,

} from 'material-react-table';

import { Box } from '@mui/material';
import { apiCall } from '../App';
import { useParams, useNavigate } from 'react-router-dom';
import Avatar from '@mui/material/Avatar';

// sourced from https://github.com/KevinVandy/material-react-table/blob/v1/apps/material-react-table-docs/examples/custom-top-toolbar/sandbox/src/JS.js
function BuyList() {
  const [data, setData] = React.useState([]);

  const navigate = useNavigate();
  const params = useParams();
  const c_id = params.id;

  const fetchData = () => {
    // call api with data
    const options = {
      method: 'GET',
      route: `/collectible/buy?collectible_id=${c_id}`,
    };

    apiCall((d) => {
      console.log(d);
      setData(d);
    }, options)
      .then((res) => {
        if (res) {
          // set error msg if api call returns error

        }
      });
  }

  React.useEffect(() => {
    fetchData();
  }, []);

  const columns = useMemo(
    //column definitions...
    () => [
      {
        accessorKey: 'collection_id',
        header: 'Collection id',
      },
      {
        accessorKey: 'image',
        header: 'Collectible Image',
        Cell: ({ row }) => (
          <Box
            sx={{
              display: 'flex',
              gap: '1rem',
            }}
          >
            <img
              alt="collectible image"
              height={60}
              src={row.original.image}
              loading="lazy"
            />
          </Box>

        ),
        enableColumnActions: false,
        enableColumnFilter: false,
        enableSorting: false,
      },
      {
        accessorKey: 'collectible_name',
        header: 'Name',
      },
      {
        accessorKey: 'trader_name',
        header: 'Traded by',
      },
      {
        accessorKey: 'trader_profile_img',
        header: 'Trader Profile',
        Cell: ({ row }) => (
          <Box
            sx={{
              display: 'flex',
              gap: '1rem',
            }}
          >
            <Avatar alt="Trader Profile" src={row.original.trader_profile_img} />
          </Box>
        ),
        enableColumnActions: false,
        enableColumnFilter: false,
      },
      {
        accessorKey: 'location',
        header: 'Location',
      },
    ],
    [],
    //end
  );

  return (
    <MaterialReactTable
      title="BuyList"
      columns={columns}
      data={data}
      positionToolbarAlertBanner="bottom" //show selected rows count on bottom toolbar
      muiTableBodyRowProps={({ row }) => ({
        onClick: () => {
          navigate(`/trade/view/${row.original.collection_id}`)
        },
        sx: { cursor: 'pointer' },
      })}
      initialState={{ columnVisibility: { collection_id: false } }}
      // changes sizing of default columns
      defaultColumn={{
        minSize: 50,
        maxSize: 500,
        size: 200, 
      }}

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


export default BuyList;