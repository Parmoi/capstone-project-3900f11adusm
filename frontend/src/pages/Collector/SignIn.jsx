import * as React from 'react';
import Avatar from '@mui/material/Avatar';
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

// gets username from profile api call
const getUsername = (userId, setUsername) => {
  const options = {
    method: 'GET',
    route: `/profile?id=${userId}`,
  };

  apiCall((d) => {
    setUsername(d.username);
  }, options);
}

// Displays page for user to sign in 
// Inputs are email address and password
// After sign in, takes user to the home page
function SignIn({ setUserId, setLogin, setPrivilege, setUsername }) {
  const [error, setError] = React.useState(false);
  const [errContent, setErrContent] = React.useState('');
  const navigate = useNavigate();

  const login = (e) => {
    e.preventDefault();
    const data = new FormData(e.currentTarget);

    const options = {
      method: 'POST',
      route: '/login',
      body: JSON.stringify({
        email: data.get('email'),
        password: data.get('password'),
      })
    };

    // calls api with login data
    apiCall((d) => {
      setLogin(true);
      setUserId(d.userId);
      getUsername(d.userId, setUsername);
      setPrivilege(parseInt(d.privelage));
    }, options)
      .then((res) => {
        if (res) {
          // set error msg if api call returns error
          setErrContent(`Error: ${res.msg}`);
          setError(true);
        }
        else {
          navigate('/');
        }
      });
  }

  return (
    <ThemeProvider theme={useTheme()}>
      <Box 
        sx={{ 
          width: '100%', 
          display: "flex", 
          flexDirection: "column", 
          alignItems: 'center', 
          justifyContent: 'center'
          }}
      >
      <Paper 
        component="main" 
        maxWidth="xs" 
        sx={{
          mt: '15vh',
          borderRadius: 2,
          maxWidth: '700px',
          width: '50vw',
          paddingBottom: '50px',
        }}
      >
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 2, bgcolor: 'support.main' }}>
          </Avatar>
          <Typography component="h1" variant="h5" color='primary.text'>
            Sign in
          </Typography>
          <Box component="form" onSubmit={login} noValidate sx={{ mt: 1 }}>
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
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="text"
              id="password"
              autoComplete="current-password"
            />
            <div>
              {error ? <Alert severity='error'>{errContent}</Alert> : <></> }
            </div>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2, backgroundColor: 'primary', color: 'secondary.main' }}
              name="sign in"
            >
              Sign In
            </Button>
            
          </Box>
        </Box>
      </Paper>
      </Box>
    </ThemeProvider>
  );
}

export default SignIn;
