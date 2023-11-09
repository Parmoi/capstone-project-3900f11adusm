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
const WantList = () => {
  const [data, setData] = React.useState([]);

  const fetchData = () => {
    // call api with data
    const options = {
      method: 'GET',
      route: "/wantlist/get",
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
        accessorKey: 'id',
        header: 'id',
      },
      {
        accessorKey: 'image',
        header: 'Image',
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
        accessorKey: 'name',
        header: 'Name',
      },
      {
        accessorKey: 'campaign_name',
        header: 'Campaign Name',
      },
      {
        accessorKey: 'dateReleased',
        accessorFn: (row) => moment(row.date_released, "DD/MM/YYYY"), //convert to Date for sorting and filtering
            id: 'dateReleased',
            header: 'Date Released',
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
        accessorKey: 'dateAdded',
        accessorFn: (row) => moment(row.date_added, "DD/MM/YYYY"), //convert to Date for sorting and filtering
            id: 'dateAdded',
            header: 'Date Added',
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
      title="Wantlist"
      columns={columns}
      data={data}
      enableRowSelection
      positionToolbarAlertBanner="bottom" //show selected rows count on bottom toolbar
      initialState={{ columnVisibility: { id: false } }}
      // changes sizing of default columns
      defaultColumn={{
        minSize: 50,
        maxSize: 500,
        size: 300, 
      }}

      //add custom action buttons to top-left of top toolbar

      renderBottomToolbarCustomActions={({ table }) => {
        const handleDelete= () => {
          table.getSelectedRowModel().flatRows.map((row) => {
            const options = {
              method: 'DELETE',
              route: "/wantlist/delete",
              body: {
                'wantlist_id': row.getValue('id'),
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

        const handleMove= () => {
          table.getSelectedRowModel().flatRows.map((row) => {
            const options = {
              method: 'POST',
              route: "/wantlist/move",
              body: {
                'wantlist_id': row.getValue('id'),
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
            onClick={handleMove}
            variant="contained"
          >
            Move to collections
          </Button>

          <Button
            color="error"
            disabled={!table.getIsSomeRowsSelected() && !table.getIsAllRowsSelected()}
            onClick={handleDelete}
            variant="contained"
          >
            Delete selected
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


export default WantList;