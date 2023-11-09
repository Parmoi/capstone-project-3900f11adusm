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

const getBackgroundColor = (status) => {
  return 'SENT' ? 'secondary.main' : 'ACCEPTED' ? 'primary.light' : 'error.main';
}

// sourced from https://github.com/KevinVandy/material-react-table/blob/v1/apps/material-react-table-docs/examples/custom-top-toolbar/sandbox/src/JS.js
const OffersList = () => {
  const [data, setData] = React.useState([]);

  const fetchData = () => {
    // call api with data
    const options = {
      method: 'GET',
      route: "/offers/get",
    };

    apiCall((d) => {
      console.log(d);
      setData(d.offers_list);
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
        accessorKey: 'offer_id',
        header: 'id',
      },
      {
        accessorKey: 'collectible_name',
        header: 'Collectible Name',
      },
      {
        accessorKey: 'offer_status',
        header: 'Offer Status',
        Cell: ({ cell }) => (
        <Button
          sx={{ 
            bgcolor: `${getBackgroundColor(cell.getValue())}`,
            borderRadius: 28
          }}
        >
          {cell.getValue()}
        </Button>
        ),
      },
      {
        accessorKey: 'trader_name',
        header: 'Traded By',
      },
      {
        accessorKey: 'date_offer_sent',
        accessorFn: (row) => moment(row.date_offer, "DD/MM/YYYY"), //convert to Date for sorting and filtering
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
    //end
  );

  return (
    <MaterialReactTable
      title="Offerlist"
      columns={columns}
      data={data}
      positionToolbarAlertBanner="bottom" //show selected rows count on bottom toolbar
      initialState={{ columnVisibility: { offer_id: false } }}
      // changes sizing of default columns
      defaultColumn={{
        minSize: 50,
        maxSize: 500,
        size: 300, 
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


export default OffersList;