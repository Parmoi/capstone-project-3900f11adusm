import React, { useMemo } from 'react';

import {
  MaterialReactTable,
  MRT_ToggleDensePaddingButton,
  MRT_FullScreenToggleButton,
} from 'material-react-table';

import { Box } from '@mui/material';

//Date Picker Imports
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import moment from 'moment';
import { apiCall } from '../App';
import { useNavigate } from 'react-router-dom';


// sourced from https://github.com/KevinVandy/material-react-table/blob/v1/apps/material-react-table-docs/examples/custom-top-toolbar/sandbox/src/JS.js
const TradeList = () => {
  const [data, setData] = React.useState([]);
  const navigate = useNavigate();

  const fetchData = () => {
    // call api with data
    const options = {
      method: 'GET',
      route: "/trade/list",
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
      },

    ],
    [],
    //end
  );

  return (
    <MaterialReactTable
      title="Tradelist"
      columns={columns}
      data={data}
      positionToolbarAlertBanner="bottom" //show selected rows count on bottom toolbar
      // changes sizing of default columns
      defaultColumn={{
        minSize: 50,
        maxSize: 300,
        size: 250,
      }}
      muiTableBodyRowProps={({ row }) => ({
        onClick: () => {
          navigate(`/tradelist/offers/${row.original.trade_post_id}`)
        },
        sx: { cursor: 'pointer' },
      })}

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