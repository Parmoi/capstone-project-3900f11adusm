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

import Switch from '@mui/material/Switch';

import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';

import { Divider } from '@mui/material';

import TwitterIcon from '@mui/icons-material/Twitter';

import { MaterialReactTable, MRT_ToggleDensePaddingButton, MRT_FullScreenToggleButton } from 'material-react-table';

import { useState, useEffect } from 'react';

import PropTypes from 'prop-types';



function AdminManageManagers() {
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
          <Box component="form"  noValidate sx={{ mt: 1 }}>
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
          maxWidth: '95vw',
          width: '80vw',
        }}
      > 
        <MaterialReactTable 
          title="Managers List"
          columns={columns}
          data={data}
          useMaterialReactTable={({ table }) => (
            <Box>
              <MRT_ToggleDensePaddingButton table={table} />
              <MRT_FullScreenToggleButton table={table} />
            </Box>
          )}
        />
      </Paper>
      </Box>
    </ThemeProvider>
  );
}


export default AdminManageManagers;