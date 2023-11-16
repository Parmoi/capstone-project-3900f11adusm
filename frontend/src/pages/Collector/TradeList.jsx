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
import { useNavigate } from 'react-router-dom';
import CollectibleImage from '../../components/CollectibleImage';

// Displays list of all items the current user has put up for trade
// Shows trade item, name, date posted and number of offers received
// Clicking on offers received takes user to trade offers list page
// Table sourced from https://github.com/KevinVandy/material-react-table/blob/v1/apps/material-react-table-docs/examples/custom-top-toolbar/sandbox/src/JS.js
const TradeList = () => {
  const [data, setData] = React.useState([]);
  const navigate = useNavigate();

  const fetchData = () => {
    // fetches all trade posts made by user 
    const options = {
      method: 'GET',
      route: "/trade/list",
    };

    apiCall((d) => {
      setData(d);
    }, options);
  }

  React.useEffect(() => {
    fetchData();
  }, []);

  function handleOffersClick(post_id) {
    navigate(`/tradelist/offers/${post_id}`)
  }

  const columns = useMemo(
    //column definitions...
    () => [
      {
        accessorKey: 'trader_collectible_img',
        header: 'Trade Item Image',
        Cell: ({ row }) => (
          <CollectibleImage id={row.original.trader_collectible_id} name={row.original.trader_collectible_name} image={row.original.trader_collectible_img} />
        ),
        enableColumnActions: false,
        enableColumnFilter: false,
        enableSorting: false,
      },
      {
        accessorKey: 'trade_post_date',
        accessorFn: (row) => moment(row.trade_post_date, "DD/MM/YYYY"), //convert to Date for sorting and filtering
        id: 'datePost',
        header: 'Date Posted',
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
        accessorKey: 'offers_received',
        header: 'Offers Received',
        Cell: ({ row }) => (
          <Button
            onClick={() => handleOffersClick(row.original.trade_post_id)}
            sx={{ 
              bgcolor: 'secondary.main',
              borderRadius: 28,
            }}
          >
            {row.original.offers_received}
          </Button> 
          
        ),
      },

    ],
    [],
  );

  return (
    <MaterialReactTable
      title="Tradelist"
      columns={columns}
      data={data}
      positionToolbarAlertBanner="bottom"
      defaultColumn={{
        minSize: 50,
        maxSize: 300,
        size: 300,
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


export default TradeList;