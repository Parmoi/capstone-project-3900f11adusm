import './App.css';
import React, { Fragment } from 'react';
import Box from '@mui/material/Box';
import { ThemeProvider, createTheme } from "@mui/material/styles";

import SignIn from './pages/SignIn';
import Register from './pages/Register';
import Profile from './pages/Profile';
import WantList from './pages/WantList';
import CollectionList from './pages/CollectionList';
import OffersList from './pages/OffersList';
import HomePage from './pages/homePage';
import SellPage from './pages/SellPage';

import SignedInNav from './components/SignedInNav';
import SignedOutNav from './components/SignedOutNav';

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
    credentials: 'include',
    body: options.body
  }

  const response = await fetch(url, params);
  const data = await response.json();
  if (response.status !== 200) {
    return data;
  } else {
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
    error : {
      main: "#F46786",
    }
  }
});

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  function logout () {
    const options = {
      method: 'POST',
      route: '/logout',
    };
    apiCall(() => 
    {
      setLoggedIn(false);
    }
    , options);
  }


  return (
    <Fragment>
      <ThemeProvider theme={theme}>
        <Helmet bodyAttributes={{ style: 'background-color : #cccccc' }} />
        {/* <ErrModal errMsg={errMsg} open={errOpen} handleClose={handleErrClose}/> */}
        <Box sx={{ display: 'flex', flexDirection: 'column', rowGap: '10ch', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
          { !loggedIn
           ?  <BrowserRouter>
              <SignedOutNav />
              <Routes>
                <Route path="/" element={<HomePage/>} />
                <Route path="/login" element={<SignIn setLogin={setLoggedIn}/>} />
                <Route path="/register" element={<Register setLogin={setLoggedIn}/>} />
              </Routes>
              </BrowserRouter>
          : <BrowserRouter>
            <SignedInNav logout={logout}/>
            <Routes>
              <Route path="/profile" element={<Profile />} />
              <Route path="/wantlist" element={<WantList />} />
              <Route path="/collection" element={<CollectionList />} />
              <Route path="/dashboard" element={<span>Dashboard</span>} />
              <Route path="/offers" element={<OffersList/>} />
              <Route path="/trade" element={<SellPage/>} />
            </Routes>
          </BrowserRouter>
          } 
        </Box>
      </ThemeProvider>
    </Fragment>
  );
}

export default App;
