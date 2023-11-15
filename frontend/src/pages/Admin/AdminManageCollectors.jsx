import React, { useMemo } from 'react';
import Avatar from '@mui/material/Avatar';

import {
  MaterialReactTable,
  MRT_ToggleDensePaddingButton,
  MRT_FullScreenToggleButton,
} from 'material-react-table';

import { Box, Button } from '@mui/material';

import { apiCall } from '../../App';



function AdminManageCollectors() {
  const [data, setData] = React.useState([]);
  const [rowSelection, setRowSelection] = React.useState({});

  const fetchData = () => {
    console.log('fetching data');
    // call api with data
    const options = {
      method: 'GET',
      route: "/collector/getlist",
    };

    apiCall((d) => {
      setData(d["collectors"]);
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
    () => [
      {
        accessorKey: 'user_id',
        header: 'Collector ID',
      },
      {
        accessorKey: 'username',
        header: 'Collector Username',
      },
      {
        accessorKey: 'profile_img',
        header: 'Collector Profile',
        Cell: ({ row }) => (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'flex-start',
              gap: '1rem',
            }}
          >
            <Avatar alt="Collector Profile" src={row.original.profile_img} />
          </Box>
        ),
        enableColumnActions: false,
        enableColumnFilter: false,
      },
      {
        accessorKey: 'first_name',
        header: 'First Name',
      },
      {
        accessorKey: 'last_name',
        header: 'Last Name',
      },
      {
        accessorKey: 'email',
        header: 'Email',
      },
      {
        accessorKey: 'phone',
        header: 'Phone',
      },
    ],
    [],
  );

  return (
    <MaterialReactTable
      title="Collection"
      columns={columns}
      data={data}
      enableRowSelection
      positionToolbarAlertBanner="bottom" //show selected rows count on bottom toolbar
      initialState={{ columnVisibility: { user_id: false } }}
      // changes sizing of default columns
      defaultColumn={{
        minSize: 50,
        maxSize: 500,
        size: 200,
      }}
      onRowSelectionChange={setRowSelection}
      state={{ rowSelection }}

      //add custom action buttons to top-left of top toolbar

      renderBottomToolbarCustomActions={({ table }) => {
        const handleDelete = () => {
          table.getSelectedRowModel().flatRows.map((row) => {
            const options = {
              method: 'POST',
              route: "/collector/ban",
              body: JSON.stringify({
                'collector_id': row.getValue('user_id'),
              })
            };
            console.log(row.getValue('user_id'));

            apiCall(() => { 
              fetchData();
              setRowSelection({});
             }, options)
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
              color="error"
              // For some reason, button is disabled when all rows selected
              // TODO: find fix
              disabled={!table.getIsSomeRowsSelected() && !table.getIsAllRowsSelected()}
              onClick={() => {
                // api call to backend
                // setData to new data
                handleDelete();
              }}
              variant="contained"
            >
              Ban Collectors
            </Button>
          </Box>
        );

      }}

      //customize built-in buttons in the top-right of top toolbar

      renderToolbarInternalActions={({ table }) => (

        <Box>
          {/* add custom button to print table  */}
          <MRT_ToggleDensePaddingButton table={table} />
          <MRT_FullScreenToggleButton table={table} />
        </Box>
      )}

    />
  );
}


export default AdminManageCollectors;