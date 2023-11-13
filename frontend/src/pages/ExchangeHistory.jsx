import React, { useMemo } from 'react';
import { Box, Typography} from '@mui/material';
import Avatar from '@mui/material/Avatar';

import { MaterialReactTable, MRT_ToggleDensePaddingButton, MRT_FullScreenToggleButton } from 'material-react-table';

import { useState, useEffect } from 'react';

import { apiCall } from '../App';
import ProfileAvatar from '../components/ProfileAvatar';

function ExchangeHistory() {
  const [data, setData] = useState([]);

  const fetchInfo = () => {
    const options = {
      method: 'GET',
      route: '/exchange/history'
    };

    apiCall((d) => {
      setData(d["exchange_history"]);
    }, options)
      .then((res) => {
        if (res) {
          // set error msg if api call returns error
        }
      });
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
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '1rem',
              flexDirection: 'column'
            }}
          >
            <Typography variant="h8">{row.original.traded_collectible_name}</Typography>
            <img
              alt="collectible image"
              height={50}
              src={row.original.traded_collectible_img}
              loading="lazy"
            />
          </Box>
        ),
        enableColumnActions: false,
        enableColumnFilter: false,
      },
      {
        accessorKey: 'accepted_collectible_img',
        header: 'Accepted Collectible',
        Cell: ({ row }) => (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '1rem',
              flexDirection: 'column'
            }}
          >
            <Typography variant="h8">{row.original.accepted_collectible_name}</Typography>
            <img
              alt="collectible image"
              height={50}
              src={row.original.accepted_collectible_img}
              loading="lazy"
            />
          </Box>
        ),
        enableColumnActions: false,
        enableColumnFilter: false,
      },
      {
        accessorKey: 'trader_profile_img',
        header: 'Trader Profile',
        Cell: ({ row }) => (
          <ProfileAvatar userId={row.original.trader_collector_id} image={row.original.trader_profile_img}/>
        ),
        enableColumnActions: false,
        enableColumnFilter: false,
      },
      {
        accessorKey: 'trader_username',
        header: 'Trade Username',
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
      // changes sizing of default columns
      defaultColumn={{
        minSize: 50,
        maxSize: 200,
        size: 170,
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