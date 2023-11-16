import React, { useMemo, Fragment } from 'react';
import Avatar from '@mui/material/Avatar';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { useTheme, ThemeProvider } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import { apiCall } from '../../App';
import Alert from '@mui/material/Alert';
import Paper from '@mui/material/Paper';
import FormControlLabel from '@mui/material/FormControlLabel';

import Switch from '@mui/material/Switch';


import { MaterialReactTable, MRT_ToggleDensePaddingButton, MRT_FullScreenToggleButton } from 'material-react-table';

import { useState, useEffect } from 'react';

function AdminManageManagers() {
  const [data, setData] = useState([]);
  const [sent, setSent] = useState(false);

  const changePermission = (manager_id) => {
    const options = {
      method: 'POST',
      route: '/manager/publish',
      body: JSON.stringify({
        manager_id: manager_id,
      })
    };

    apiCall(() => {}, options)
      .then((res) => {
        if (res) {
          // set error msg if api call returns error
        }
      })
    ;

  }

  const sendInvite = (e) => {
    e.preventDefault();
    const data = new FormData(e.currentTarget);

    // call api with data
    const options = {
      method: 'POST',
      route: '/manager/invite',
      body: JSON.stringify({
        email: data.get('email'),
      })
    };

    apiCall(() => {}, options)
      .then((res) => {
        if (res) {
          // set error msg if api call returns error
        }
        else { setSent(true); }
      })
    ;
  }

  const fetchInfo = () => {
    const options = {
      method: 'GET',
      route: '/manager/getlist'
    };

    apiCall((d) => {
      setData(d["managers"]);
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
        accessorKey: 'username',
        header: 'Manager Username',
      },
      {
        accessorKey: 'profile_img',
        header: 'Manager Profile',
        Cell: ({ row }) => (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'flex-start',
              gap: '1rem',
            }}
          >
            <Avatar alt="Manager Profile" src={row.original.profile_img} />
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
      { 
        accessorKey: 'can_publish',
        header: 'can_publish', 
        Cell: ({ row }) => (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '1rem',
            }}
          >
            <Switch 
              checked={row.original.privelage == 3} 
              onChange={changePermission(row.original.user_id)} 
              name="Can Publish" color="primary"
            />
          </Box>
        ),
      },
    ],
    [],
  );


  return (
    <ThemeProvider theme={useTheme()}>
      <Box 
        sx={{ 
          width: '100%', 
          height: '90.8vh', 
          display: "flex", 
          flexDirection: "column", 
          backgroundImage: `url("https://res.cloudinary.com/ddor5nnks/image/upload/v1699602264/gradient_background_zjdl6a.webp")`, 
          backgroundRepeat: "no-repeat", 
          backgroundSize: "cover", 
          alignItems: 'center', 
          justifyContent: 'flex-start',
          }}
      >
      <Paper 
        component="main" 
        maxWidth="xs" 
        sx={{
          marginTop: '8vh',
          borderRadius: 2,
          maxWidth: '600px',
          width: '50vw',
          paddingBottom: '50px',
        }}
      >
        <CssBaseline />
        <Box
          sx={{
            marginTop: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >

          <Typography component="h1" variant="h5" color='primary.text'>
            Invite New Managers
          </Typography>
          <Box component="form" onSubmit={sendInvite}  noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              autoFocus
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, backgroundColor: 'primary', color: 'secondary.main' }}
              name="sign in"
            >
              Send Invite
            </Button>
            
          </Box>
        </Box>
      </Paper>

      <Paper 
        component="main" 
        maxWidth="xs" 
        sx={{
          mt: '5vh',
          borderRadius: 2,
          maxWidth: '100vw',
          width: '95vw',
        }}
      > 
        <MaterialReactTable 
          title="Managers List"
          columns={columns}
          data={data}
          positionToolbarAlertBanner="bottom" //show selected rows count on bottom toolbar
          // changes sizing of default columns
          defaultColumn={{
            minSize: 50,
            maxSize: 300,
            size: 250,
          }}

          //customize built-in buttons in the top-right of top toolbar
          renderToolbarInternalActions={({ table }) => (

            <Box>
              <MRT_ToggleDensePaddingButton table={table} />
              <MRT_FullScreenToggleButton table={table} />
            </Box>
          )}
        />
      </Paper>

      <Paper 
        maxWidth="xs" 
        sx={{
          mt: '5vh',
          borderRadius: 2,
          maxWidth: '20vw',
          width: '20vw',
        }}
      >
        <Box>
          {sent 
          ? <Alert 
              onClose={() => { setSent(false); }}
              fullWidth
              variant="outlined"
            >
              Invite Sent
            </Alert>
          : <></> }
        </Box>
      </Paper>

      </Box>
    </ThemeProvider>
  );
}


export default AdminManageManagers;