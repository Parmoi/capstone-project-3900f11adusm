import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, useTheme, ThemeProvider } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import validator from 'validator';
import { apiCall } from '../App';
import Alert from '@mui/material/Alert';

const theme = createTheme();

function Register({ setLogin }) {
  const navigate = useNavigate();
  const [emailError, setEmailError] = React.useState(false);
  const [nameError, setNameError] = React.useState(false);
  const [pwdError, setPwdError] = React.useState(false);

  const [error, setError] = React.useState(false);
  const [errContent, setErrContent] = React.useState('');


  const validateEmail = (e) => {
    const email = e.target.value;
    setEmailError(!validator.isEmail(email));
  };

  const validateName = (e) => {
    const name = e.target.value;
    setNameError(name === '');
  };

  const validatePwd = (e) => {
    const pwd = e.target.value;
    setPwdError(pwd === '');
  };

  const register = (e) => {
    e.preventDefault();
    const data = new FormData(e.currentTarget);

    if (emailError || nameError || pwdError) {
      // if error, do nothing
      return;
    }

    // call api with data
    const options = {
      method: 'POST',
      route: '/register',
      body: JSON.stringify({
        email: data.get('email'),
        password: data.get('password'),
        name: data.get('name'),
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
          navigate('/');
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
            {/* <LockOutlinedIcon /> */}
          </Avatar>
          <Typography component="h1" variant="h5" color='primary.text'>
            Sign up
          </Typography>
          <Box component="form" onSubmit={register} noValidate sx={{ mt: 1 }}>
            <TextField
              sx={{backgroundColor:'white'}}
              margin="normal"
              required
              fullWidth
              backgroundColor='white'
              name="name"
              label="Name"
              type="name"
              id="name"
              autoComplete="name"
              onBlur={(e) => validateName(e)}
              helperText={nameError ? 'Name must not be empty' : ''}
            />
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
              onChange={(e) => validateEmail(e)}
              helperText={emailError ? 'Email must be valid' : ''}
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
              onBlur={(e) => validatePwd(e)}
              helperText={pwdError ? 'Password must not be empty' : ''}
            />
            <div>
              {error ? <Alert severity='error'>{errContent}</Alert> : <></> }
            </div>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={pwdError || nameError || emailError}
            >
              Register
            </Button>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default Register;
