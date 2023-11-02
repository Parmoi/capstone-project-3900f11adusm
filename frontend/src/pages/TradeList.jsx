import React, { useMemo } from 'react';

import {
  MaterialReactTable,
  MRT_ToggleDensePaddingButton,
  MRT_FullScreenToggleButton,
} from 'material-react-table';

import { Box, Button, IconButton } from '@mui/material';

//Date Picker Imports
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import moment from 'moment';

import { apiCall } from '../App';


// sourced from https://github.com/KevinVandy/material-react-table/blob/v1/apps/material-react-table-docs/examples/custom-top-toolbar/sandbox/src/JS.js
const TradeList = () => {
  const [data, setData] = React.useState([]);

  const fetchData = () => {
    // call api with data
    const options = {
      method: 'GET',
      route: "/trade/list",
    };

    apiCall((d) => {
      console.log(d);
      setData(d["trades_list"]);
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
        accessorKey: 'trader_collectible_name',
        header: 'Collectible on Trade',
      },
      {
        accessorKey: 'trader_collectible_img',
        header: 'Trade Item Image',
        Cell: ({ row }) => (
          <Box
            sx={{
              display: 'flex',
              gap: '1rem',
            }}
          >
            <img
              alt="trading collectible image"
              height={60}
              src={row.original.trader_collectible_img}
              loading="lazy"
            />
          </Box>

        ),
        enableColumnActions: false,
        enableColumnFilter: false,
        enableSorting: false,
      },
      {
        accessorKey: 'offer_collectible_name',
        header: 'Offer Collectible',
      },
      {
        accessorKey: 'offer_collectible_img',
        header: 'Offer Item Image',
        Cell: ({ row }) => (
          <Box
            sx={{
              display: 'flex',
              gap: '1rem',
            }}
          >
            <img
              alt="offer collectible image"
              height={60}
              src={row.original.offer_collectible_img}
              loading="lazy"
            />
          </Box>

        ),
        enableColumnActions: false,
        enableColumnFilter: false,
        enableSorting: false,
      },
      {
        accessorKey: 'offer_name',
        header: 'Collector Name'
      },
      {
        accessorKey: 'offer_profile_img',
        header: 'Collector Profile',
        Cell: ({ row }) => (
          <Box
            sx={{
              display: 'flex',
              gap: '1rem',
            }}
          >
            <img
              alt="collector profile"
              height={60}
              src={row.original.offer_profile_img}
              loading="lazy"
            />
          </Box>

        ),
        enableColumnActions: false,
        enableColumnFilter: false,
        enableSorting: false,
      },
      {
        accessorKey: 'offer_made_date',
        header: 'Offer Received'
      }


    ],
    [],
    //end
  );

  return (
    <MaterialReactTable
      title="Wantlist"
      columns={columns}
      data={data}
      enableRowSelection
      positionToolbarAlertBanner="bottom" //show selected rows count on bottom toolbar
      initialState={{ columnVisibility: { id: false } }}

      //add custom action buttons to top-left of top toolbar

      renderBottomToolbarCustomActions={({ table }) => {
        const handleDecline= () => {
          table.getSelectedRowModel().flatRows.map((row) => {
            const options = {
              method: 'DELETE',
              route: "/exchange/decline",
              body: {
                'offer_id': row.getValue('offer_id'),
              }
            };
            console.log(row.getValue('offer_id'));

            apiCall(() => { }, options)
              .then((res) => {
                if (res) {
                  // set error msg if api call returns error

                }
              });
          });
        };

        const handleAccept= () => {
          table.getSelectedRowModel().flatRows.map((row) => {
            const options = {
              method: 'POST',
              route: "/exchange/accept",
              body: {
                'offer_id': row.getValue('offer_id'),
              }
            };
            console.log(row.getValue('id'));

            apiCall(() => { }, options)
              .then((res) => {
                if (res) {
                  // set error msg if api call returns error

                }
              });
          });
        };

        return (
        <Box sx={{ display: 'flex', gap: '1rem', p: '4px' }}>
          <Button
            color="secondary"
            // For some reason, button is disabled when all rows selected
            // TODO: find fix
            disabled={!table.getIsSomeRowsSelected() && !table.getIsAllRowsSelected()}
            onClick={handleAccept}
            variant="contained"
          >
            Accept Offer
          </Button>

          <Button
            color="error"
            disabled={!table.getIsSomeRowsSelected() && !table.getIsAllRowsSelected()}
            onClick={handleDecline}
            variant="contained"
          >
            Decline Offer
          </Button>
        </Box>
        );

      }}

      //customize built-in buttons in the top-right of top toolbar
      renderToolbarInternalActions={({ table }) => (

        <Box>
          <MRT_ToggleDensePaddingButton table={table} />
          <MRT_FullScreenToggleButton table={table} />
        </Box>
      )}

    />
  );
};


export default TradeList;