import React, { useMemo, Fragment } from 'react';
import Box from '@mui/material/Box';
import Avatar from '@mui/material/Avatar';

import { MaterialReactTable, MRT_ToggleDensePaddingButton, MRT_FullScreenToggleButton } from 'material-react-table';

import { useState, useEffect } from 'react';

import { apiCall } from '../../App';


function ManagerFeedback() {
  const [data, setData] = useState([]);

  const fetchInfo = () => {
    const options = {
      method: 'GET',
      route: '/manager/feedback'
    };

    apiCall((d) => {
      setData(d["feedback"]);
    }, options)
    .then((res) => {
      if (res) {
        // set error msg if api call returns error
      }
    });
  }

  useEffect(() => {
    fetchInfo();
  }, []);

  const columns = useMemo(
    () => [
      {
        accessorKey: 'collector_username',
        header: 'Collector Username',
      },
      {
        accessorKey: 'collector_profile_img',
        header: 'Collector Profile',
        Cell: ({ row }) => (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '1rem',
            }}
          >
            <Avatar alt="Collector Profile" src={row.original.collector_profile_img} />
          </Box>
        ),
        enableColumnActions: false,
        enableColumnFilter: false,
      },
      {
        accessorKey: 'feedback',
        header: 'Feedback',
      },
      {
        accessorKey: 'feedback_date',
        header: 'Feedback Date',
      },
      

    ],
    [],
  );

  return (
    <MaterialReactTable
      title="Feedback from Collectors"
      columns={columns}
      data={data}
      useMaterialReactTable={({ table }) => (
        <Box>
          <MRT_ToggleDensePaddingButton table={table} />
          <MRT_FullScreenToggleButton table={table} />
        </Box>
      )}
    />
  );
}


export default ManagerFeedback;