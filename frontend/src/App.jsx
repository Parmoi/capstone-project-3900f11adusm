import './App.css';
import React, { Fragment } from 'react';
import Box from '@mui/material/Box';
import { ThemeProvider, createTheme } from "@mui/material/styles";

import SignIn from './pages/SignIn';
import Register from './pages/Register';
import Profile from './pages/Profile';
import WantList from './pages/WantList';
import CollectionList from './pages/CollectionList';
import HomePage from './pages/homePage';
import SignedInNav from './components/SignedInNav';
import SignedOutNav from './components/SignedOutNav';
import ErrModal from './components/ErrModal';

import { useState } from 'react';

import {
  BrowserRouter,
  Routes,
  Route,
} from 'react-router-dom';
import { Helmet } from 'react-helmet';

const PORT = 5000;

export async function apiCall(onSuccess, options, ...optional) {
  const url = `http://localhost:${PORT}${options.route}`;
  const params = {
    method: options.method,
    headers: {
      'Content-type': 'application/json',
    },
    body: options.body
  }

  const response = await fetch(url, params);
  const data = await response.json();
  if (data.status !== 200) {
    console.log('there is an error');
    console.log(data);
    return data;
  } else {
    console.log(data);
    return onSuccess(data, ...optional);
  }
}

const theme = createTheme({
  palette: {
    primary: {
      main: "#216869",
      light: "#BFCC94",
      text: "#1F2421",
    },
    secondary: {
      main: "#F0F4EF",
    },
    support: {
      main: "#B4CDED",
    },
  }
});

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [errOpen, setErrOpen] = React.useState(false);
  const handleErrClose = () => setErrOpen(false);
  const [errMsg, setErrMsg] = React.useState('');
  const [token, setToken] = React.useState('');

  function logout () {
    const options = {
      method: 'POST',
      route: '/logout',
    };
    apiCall(() => 
    {
      setLoggedIn(false);
      setToken('');
    }
    , options);
  }


  return (
    <Fragment>
      <ThemeProvider theme={theme}>
        <Helmet bodyAttributes={{ style: 'background-color : white' }} />
        <ErrModal errMsg={errMsg} open={errOpen} handleClose={handleErrClose}/>
        <Box sx={{ display: 'flex', flexDirection: 'column', rowGap: '10ch', alignItems: 'center', justifyContent: 'center' }}>
          { !loggedIn
           ?  <BrowserRouter>
              <SignedOutNav />
              <Routes>
                <Route path="/" element={<HomePage/>} />
                <Route path="/login" element={<SignIn setLogin={setLoggedIn} setToken={setToken}/>} />
                <Route path="/register" element={<Register setLogin={setLoggedIn} setToken={setToken}/>} />
              </Routes>
              </BrowserRouter>
          : <BrowserRouter>
            <SignedInNav logout={logout}/>
            <Routes>
              <Route path="/profile" element={<Profile />} />
              <Route path="/wantlist" element={<WantList />} />
              <Route path="/collection" element={<CollectionList />} />
              <Route path="/dashboard" element={<span>Dashboard</span>} />
            </Routes>
          </BrowserRouter>
          } 
        </Box>
      </ThemeProvider>
    </Fragment>
  );
}

export default App;
