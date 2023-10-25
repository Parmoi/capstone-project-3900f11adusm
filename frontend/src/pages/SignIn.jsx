import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { useTheme, ThemeProvider } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import { apiCall } from '../App';
import Alert from '@mui/material/Alert';

function SignIn({ setLogin }) {
  const [error, setError] = React.useState(false);
  const [errContent, setErrContent] = React.useState('');
  const navigate = useNavigate();
  
  const login = (e) => {
    e.preventDefault();
    const data = new FormData(e.currentTarget);

    // call api with data
    const options = {
      method: 'POST',
      route: '/login',
      body: JSON.stringify({
        email: data.get('email'),
        password: data.get('password'),
      })
    };

    apiCall(() => {
      setLogin(true);
    }, options)
      .then((res) => {
        if (res) {
          // set error msg if api call returns error
          setErrContent(`Error: ${res.msg}`);
          setError(true);
        }
        else {
          navigate('/dashboard');
        }
      });
  }

  return (
    <ThemeProvider theme={useTheme()}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'support.main' }}>
          </Avatar>
          <Typography component="h1" variant="h5" color='primary.text'>
            Sign in
          </Typography>
          <Box component="form" onSubmit={login} noValidate sx={{ mt: 1 }}>
            <TextField
              sx={{backgroundColor:'white'}}
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
              sx={{backgroundColor:'white'}}
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
      </Container>
    </ThemeProvider>
  );
}

export default SignIn;
