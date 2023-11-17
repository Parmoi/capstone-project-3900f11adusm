import React, { useMemo } from 'react';

import {
  MaterialReactTable,
  MRT_ToggleDensePaddingButton,
  MRT_FullScreenToggleButton,
} from 'material-react-table';

import { Box } from '@mui/material';
import { apiCall } from '../../App';
import { useParams, useNavigate } from 'react-router-dom';
import Avatar from '@mui/material/Avatar';

// Page which display a list of trade posts trading a particular collectible
// The collectible id identifies which collectible the trade posts are trading
// Clicking on a trade post takes the user to the trade post page
// List sourced from https://github.com/KevinVandy/material-react-table/blob/v1/apps/material-react-table-docs/examples/custom-top-toolbar/sandbox/src/JS.js
function BuyList() {
  const [data, setData] = React.useState([]);

  const navigate = useNavigate();
  const params = useParams();
  const c_id = params.id;

  const fetchData = () => {
    // fetches all trade posts trading this collectible 
    const options = {
      method: 'GET',
      route: `/collectible/buy?collectible_id=${c_id}`,
    };

    apiCall((d) => {
      setData(d);
    }, options)
  }

  React.useEffect(() => {
    fetchData();
  }, []);

  const columns = useMemo(
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
  );

  return (
    <MaterialReactTable
      title="BuyList"
      columns={columns}
      data={data}
      positionToolbarAlertBanner="bottom" //show selected rows count on bottom toolbar
      muiTableBodyRowProps={({ row }) => ({
        onClick: () => {
          // navigates to trade post
          navigate(`/trade/view/${row.original.trade_post_id}`)
        },
        sx: { cursor: 'pointer' },
      })}
      initialState={{ columnVisibility: { collection_id: false } }}
      defaultColumn={{
        minSize: 50,
        maxSize: 500,
        size: 200, 
      }}

      renderToolbarInternalActions={({ table }) => (
        <Box>
          <MRT_ToggleDensePaddingButton table={table} />
          <MRT_FullScreenToggleButton table={table} />
        </Box>
      )}

    />
  );
};


export default BuyList;