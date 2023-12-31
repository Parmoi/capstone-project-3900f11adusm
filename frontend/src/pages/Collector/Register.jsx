import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import { useTheme, ThemeProvider } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import validator from 'validator';
import { apiCall } from '../../App';
import Alert from '@mui/material/Alert';

// Displays page for user to register
// Accepts name, email address and password as inputs
// Has validation for all fields, shows relevant helper text
function Register({ setUserId, setLogin, setUsername }) {
  const navigate = useNavigate();
  const [emailError, setEmailError] = React.useState(false);
  const [nameError, setNameError] = React.useState(false);
  const [pwdError, setPwdError] = React.useState(false);

  const [error, setError] = React.useState(false);
  const [errContent, setErrContent] = React.useState('');

  const validateEmail = (e) => {
    const email = e.target.value;
    // error when email is not valid format
    setEmailError(!validator.isEmail(email));
  };

  const validateName = (e) => {
    const name = e.target.value;
    // error when name is empty string
    setNameError(name === '');
  };

  const validatePwd = (e) => {
    const pwd = e.target.value;
    // error when password is empty string
    setPwdError(pwd === '');
  };

  const register = (e) => {
    e.preventDefault();
    const data = new FormData(e.currentTarget);

    if (emailError || nameError || pwdError) {
      // if error, do nothing
      return;
    }

    const options = {
      method: 'POST',
      route: '/register',
      body: JSON.stringify({
        email: data.get('email'),
        password: data.get('password'),
        username: data.get('name'),
      })
    };

    // call api with register inputs
    apiCall((d) => {
      setLogin(true);
      setUsername(data.get('name'));
      setUserId(d.user_id);
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
          paddingLeft: '50px',
          paddingRight: '50px',
          borderRadius: 2,
          maxWidth: '700px',
          width: '50vw',
          paddingBottom: '50px',
          mt: '15vh',
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
          <Avatar sx={{ m: 1, bgcolor: 'support.main' }}>
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
      </Paper>
      </Box>
    </ThemeProvider>
  );
}

export default Register;
