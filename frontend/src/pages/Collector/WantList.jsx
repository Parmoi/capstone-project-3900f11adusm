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

import CollectibleImage from '../../components/CollectibleImage';
import { apiCall } from '../../App';

// Displays collectibles in current user's wantlist
// Shows collectible name, image, associated campaign, date released and date collectible was added to user's collection
// Table sourced from https://github.com/KevinVandy/material-react-table/blob/v1/apps/material-react-table-docs/examples/custom-top-toolbar/sandbox/src/JS.js
const WantList = () => {
  const [data, setData] = React.useState([]);
  const [rowSelection, setRowSelection] = React.useState({});

  const fetchData = () => {
    // fetches all collectibles from user's wantlist
    const options = {
      method: 'GET',
      route: "/wantlist/get",
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
        accessorKey: 'id',
        header: 'id',
      },
      {
        accessorKey: 'image',
        header: 'Image',
        Cell: ({ row }) => (
          <CollectibleImage id={row.original.collectible_id} name={row.original.name} image={row.original.image} />

        ),
        enableColumnActions: false,
        enableColumnFilter: false,
        enableSorting: false,
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
      positionToolbarAlertBanner="bottom"
      initialState={{ columnVisibility: { id: false } }}
      defaultColumn={{
        minSize: 50,
        maxSize: 500,
        size: 250,
      }}
      onRowSelectionChange={setRowSelection}
      state={{ rowSelection }}

      //add custom action buttons to top-left of top toolbar
      renderBottomToolbarCustomActions={({ table }) => {
        const handleDelete = () => {
          // deletes all selected collectibles from wantlist
          table.getSelectedRowModel().flatRows.map((row) => {
            const options = {
              method: 'DELETE',
              route: "/wantlist/delete",
              body: JSON.stringify({
                'wantlist_id': row.getValue('id'),
              }),
            };

            apiCall(() => { 
              // reloads wantlist and resets selection
              fetchData();
              setRowSelection({});
             }, options);
          });
        };

        const handleMove = () => {
          // moves all selected collectibles from wantlist to collection list
          table.getSelectedRowModel().flatRows.map((row) => {
            const options = {
              method: 'POST',
              route: "/wantlist/move",
              body: JSON.stringify({
                'wantlist_id': row.getValue('id'),
              }),
            };

            apiCall(() => { 
              // reloads wantlist and resets selection
              fetchData();
              setRowSelection({});
             }, options);
          });
        };

        return (
          <Box sx={{ display: 'flex', gap: '1rem', p: '4px' }}>
            <Button
              color="secondary"
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