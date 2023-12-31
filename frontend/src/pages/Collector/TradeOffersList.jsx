import React, { useMemo } from 'react';

import {
    MaterialReactTable,
    MRT_ToggleDensePaddingButton,
    MRT_FullScreenToggleButton,
} from 'material-react-table';

import { Box, Button } from '@mui/material';

//Date Picker Imports
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import moment from 'moment';
import { useParams } from 'react-router-dom';
import { apiCall } from '../../App';
import ProfileAvatar from '../../components/ProfileAvatar';
import CollectibleImage from '../../components/CollectibleImage';

// Displays all offers made for a particular trade
// Shows offer collectible image, trader profile, offer message and date offer was made
// Table sourced from https://github.com/KevinVandy/material-react-table/blob/v1/apps/material-react-table-docs/examples/custom-top-toolbar/sandbox/src/JS.js
const TradeOffersList = () => {
  const [data, setData] = React.useState([]);

  const params = useParams();
  const t_id = params.id;

  const fetchData = () => {
    // fetches all offers for a particular trade
    const options = {
      method: 'GET',
      route: `/trade/list/offers?trade_id=${t_id}`,
    };

    apiCall((d) => {
      setData(d);
    }, options);
  }

  React.useEffect(() => {
    fetchData();
  }, []);

  const columns = useMemo(
    () => [
      {
        accessorKey: 'offer_collectible_img',
        header: 'Trade Item Image',
        Cell: ({ row }) => (
          <CollectibleImage 
            id={row.original.collectible_id} 
            name={row.original.offer_collectible_name} 
            image={row.original.offer_collectible_img}
          />
        ),
        enableColumnActions: false,
        enableColumnFilter: false,
        enableSorting: false,
      },
      {
        accessorKey: 'trader_profile_img',
        header: 'Trader Profile',
        Cell: ({ row }) => (
          <ProfileAvatar 
            userId={row.original.trader_id} 
            image={row.original.trader_profile_img} 
            name={row.original.trader_name}
          />
        ),
        enableColumnActions: false,
        enableColumnFilter: false,
      },
      {
        accessorKey: 'offer_message',
        header: 'Offer Message',
      },
      {
        accessorKey: 'offer_made_date',
        accessorFn: (row) => moment(row.offer_made_date, "DD/MM/YYYY"), //convert to Date for sorting and filtering
        id: 'dateOffer',
        header: 'Date Offer Made',
        filterFn: 'lessThanOrEqualTo',
        sortingFn: 'datetime',

        Cell: ({ cell }) => cell.getValue()?.format('DD/MM/YY'), //render Date as a string
        Header: ({ column }) => <em>{column.columnDef.header}</em>, //custom header markup

        //Custom Date Picker Filter from @mui/x-date-pickers
        Filter: ({ column }) => (
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DatePicker
              onChange={(newValue) => {
                column.setFilterValue(newValue);
              }}

              slotProps={{
                textField: {
                    helperText: 'Filter Mode: Less Than',
                    sx: { minWidth: '120px' },
                    variant: 'standard',
                },
              }}

              value={column.getFilterValue()}
              format="DD-MM-YYYY"
            />
          </LocalizationProvider>
        )
      },
    ],
  [],
  );

  return (
    <MaterialReactTable
      title="Tradelist"
      columns={columns}
      data={data}
      enableRowSelection
      enableMultiRowSelection={false}
      positionToolbarAlertBanner="bottom" //show selected rows count on bottom toolbar
      initialState={{ columnVisibility: { id: false } }}
      // changes sizing of default columns
      defaultColumn={{
        minSize: 50,
        maxSize: 300,
        size: 150,
      }}

      //add custom action buttons to top-left of top toolbar

      renderBottomToolbarCustomActions={({ table }) => {
        // declines all selected offers
        const handleDecline = () => {
          table.getSelectedRowModel().flatRows.map((row) => {
            const options = {
              method: 'POST',
              route: "/exchange/decline",
              body: JSON.stringify({
                offer_id: row.original.offer_id,
              })
            };

            apiCall(() => { 
              fetchData();
            }, options);
          });
        };

        // accepts all selected offers
        const handleAccept = () => {
          table.getSelectedRowModel().flatRows.map((row) => {
            const options = {
              method: 'POST',
              route: "/exchange/accept",
              body: JSON.stringify({
                offer_id: row.original.offer_id,
              })
            };

            apiCall(() => {
              fetchData();
              }, options);
          });
        };

        return (
          <Box sx={{ display: 'flex', gap: '1rem', p: '4px' }}>
            <Button
              color="secondary"
              disabled={(!table.getIsSomeRowsSelected() && !table.getIsAllRowsSelected())}
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

      renderToolbarInternalActions={({ table }) => (
        <Box>
          <MRT_ToggleDensePaddingButton table={table} />
          <MRT_FullScreenToggleButton table={table} />
        </Box>
      )}
    />
  );
};


export default TradeOffersList;