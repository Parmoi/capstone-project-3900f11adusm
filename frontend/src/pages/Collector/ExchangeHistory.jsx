import React, { useMemo } from 'react';
import { Box } from '@mui/material';

import { MaterialReactTable, MRT_ToggleDensePaddingButton, MRT_FullScreenToggleButton } from 'material-react-table';

import { useState, useEffect } from 'react';

import { apiCall } from '../../App';
import ProfileAvatar from '../../components/ProfileAvatar';
import CollectibleImage from '../../components/CollectibleImage';

// Page that displays user's exchange/trade history using this platform
// Shows traded and accepted collectible, profile of user they traded with, date offer was sent and date it was accepted
function ExchangeHistory() {
  const [data, setData] = useState([]);

  const fetchInfo = () => {
    // gets user's exchange history information
    const options = {
      method: 'GET',
      route: '/exchange/history'
    };

    apiCall((d) => {
      setData(d);
    }, options);
  }

  useEffect(() => {
    fetchInfo();
  }, []);

  const columns = useMemo(
    () => [
      {
        accessorKey: 'traded_collectible_img',
        header: 'Traded Collectible',
        Cell: ({ row }) => (
          <CollectibleImage 
            id={row.original.traded_collectible_id} 
            name={row.original.traded_collectible_name}
            image={row.original.traded_collectible_img}
          />
        ),
        enableColumnActions: false,
        enableColumnFilter: false,
      },
      {
        accessorKey: 'accepted_collectible_img',
        header: 'Accepted Collectible',
        Cell: ({ row }) => (
          <CollectibleImage 
            id={row.original.accepted_collectible_id} 
            name={row.original.accepted_collectible_name}
            image={row.original.accepted_collectible_img}
          />
        ),
        enableColumnActions: false,
        enableColumnFilter: false,
      },
      {
        accessorKey: 'trader_profile_img',
        header: 'Trader Profile',
        Cell: ({ row }) => (
          <ProfileAvatar 
            userId={row.original.trader_collector_id} 
            image={row.original.trader_profile_img}
            name={row.original.trader_username}
          />
        ),
        enableColumnActions: false,
        enableColumnFilter: false,
      },
      {
        accessorKey: 'offer_made_date',
        header: 'Offer Date',
      },
      {
        accessorKey: 'accepted_date',
        header: 'Accepted Date',
      },

    ],
    [],
  );

  return (
    <MaterialReactTable
      title="Exchange History"
      columns={columns}
      data={data}
      defaultColumn={{
        minSize: 50,
        maxSize: 200,
        size: 200,
      }}
      useMaterialReactTable={({ table }) => (
        <Box>
          <MRT_ToggleDensePaddingButton table={table} />
          <MRT_FullScreenToggleButton table={table} />
        </Box>
      )}
    />
  );

};


export default ExchangeHistory;