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


// stub data
const stubData = [
  {
    image: 'https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg',
    name: 'Homer',
    collectionName: 'Winter 2022',
    dateReleased: '23/5/2014',
    dateAdded: '3/3/2014',
  },
  {
    image: 'https://tse4.mm.bing.net/th?id=OIP.e4tAXeZ6G0YL4OE5M8KTwAHaMq&pid=Api',
    name: 'Marge',
    collectionName: 'Winter 2022',
    dateReleased: '3/2/2014',
    dateAdded: '3/1/2014',
  },
  {
    image: 'https://tse2.mm.bing.net/th?id=OIP.j7EknM6CUuEct_kx7o-dNQHaMN&pid=Api',
    name: 'Bart',
    collectionName: 'Winter 2022',
    dateReleased: '4/2/2014',
    dateAdded: '3/12/2014',
  },
  {
    image: 'https://tse3.mm.bing.net/th?id=OIP.6761X25CX3UUjklkDCnjSwHaHa&pid=Api',
    name: 'Dog',
    collectionName: 'Winter 2022',
    dateReleased: '3/4/2014',
    dateAdded: '3/6/2014',
  },
  {
    image: 'https://tse3.mm.bing.net/th?id=OIP.JqWjPHsW5aJIZDnPYMGovQHaJQ&pid=Api',
    name: 'Lisa',
    collectionName: 'Winter 2022',
    dateReleased: '3/7/2014',
    dateAdded: '3/8/2014',
  },
  {
    image: 'https://tse1.mm.bing.net/th?id=OIP.qVV8kcLdcLysZ5OOCzhKLAHaF7&pid=Api',
    name: 'Rando',
    collectionName: 'Winter 2022',
    dateReleased: '3/10/2014',
    dateAdded: '3/2/2014',
  },
]

// sourced from https://github.com/KevinVandy/material-react-table/blob/v1/apps/material-react-table-docs/examples/custom-top-toolbar/sandbox/src/JS.js
const WantList = () => {
  const [data, setData] = React.useState(stubData);

  const columns = useMemo(
    //column definitions...
    () => [
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
        accessorKey: 'collectionName',
        header: 'Collection Name',
      },
      {
        accessorKey: 'dateReleased',
        accessorFn: (row) => moment(row.dateReleased, "DD/MM/YYYY"), //convert to Date for sorting and filtering
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
        accessorFn: (row) => moment(row.dateAdded, "DD/MM/YYYY"), //convert to Date for sorting and filtering
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

      //add custom action buttons to top-left of top toolbar

      renderBottomToolbarCustomActions={({ table }) => {
        const handleDelete= () => {
          table.getSelectedRowModel().flatRows.map((row) => {
            alert('deleting ' + row.getValue('name'));
          });
        };

        const handleMove= () => {
          table.getSelectedRowModel().flatRows.map((row) => {
            alert('moving ' + row.getValue('name'));
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