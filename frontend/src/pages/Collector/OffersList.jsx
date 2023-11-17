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

import { apiCall } from '../../App';
import ProfileAvatar from '../../components/ProfileAvatar';
import CollectibleImage from '../../components/CollectibleImage';

// changes colour of status icon based on status
const getBackgroundColor = (status) => {
  return status ? 'secondary.main' : 'ACCEPTED' ? 'primary.light' : 'error.main';
}

// Displays all offers sent by user and the offer status
// Table sourced from https://github.com/KevinVandy/material-react-table/blob/v1/apps/material-react-table-docs/examples/custom-top-toolbar/sandbox/src/JS.js
const OffersList = () => {
  const [data, setData] = React.useState([]);

  const fetchData = () => {
    // fetches data on all offers sent by current user
    const options = {
      method: 'GET',
      route: "/offers/get",
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
        accessorKey: 'offer_id',
        header: 'id',
      },
      {
        accessorKey: 'collectible_s_img',
        header: 'Collectible Offered',
        Cell: ({ row }) => (
          <CollectibleImage 
            id={row.original.collectible_s_id} 
            name={row.original.collectible_s_name}
            image={row.original.collectible_s_img}
          />

        ),
        enableColumnActions: false,
        enableColumnFilter: false,
        enableSorting: false,
      },
      {
        accessorKey: 'collectible_r_img',
        header: 'Collectible to be Received',
        Cell: ({ row }) => (
          <CollectibleImage 
            id={row.original.collectible_r_id} 
            name={row.original.collectible_r_name}
            image={row.original.collectible_r_img}
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
              userId={row.original.trader_collector_id} 
              image={row.original.trader_profile_img}
              name={row.original.trader_name}
            />
        ),
        enableColumnActions: false,
        enableColumnFilter: false,
    },
      {
        accessorKey: 'offer_status',
        header: 'Offer Status',
        Cell: ({ cell }) => (
        <Button
          sx={{ 
            bgcolor: `${getBackgroundColor(cell.getValue())}`,
            borderRadius: 28,
            cursor: "default",
          }}
        >
          {cell.getValue()}
        </Button>
        ),
      },
      {
        accessorKey: 'date_offer_sent',
        accessorFn: (row) => moment(row.date_offer_sent, "DD/MM/YYYY"), //convert to Date for sorting and filtering
            id: 'dateOffer',
            header: 'Date Offer Sent',
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
      {
        accessorKey: 'dateUpdated',
        accessorFn: (row) => moment(row.date_updated, "DD/MM/YYYY"), //convert to Date for sorting and filtering
            id: 'dateUpdated',
            header: 'Date Updated',
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
      title="Offerlist"
      columns={columns}
      data={data}
      positionToolbarAlertBanner="bottom" 
      initialState={{ columnVisibility: { offer_id: false } }}
      defaultColumn={{
        minSize: 50,
        maxSize: 500,
        size: 150, 
      }}

      // buttons for toggling padding and full screen
      renderToolbarInternalActions={({ table }) => (
        <Box>
          <MRT_ToggleDensePaddingButton table={table} />
          <MRT_FullScreenToggleButton table={table} />
        </Box>
      )}

    />
  );
};


export default OffersList;