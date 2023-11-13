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
import CollectiblePage from './pages/CollectiblePage';

import OffersList from './pages/OffersList';
import SellPage from './pages/SellPage';
import LandingPage from './pages/landingPage';
import SignedInNav from './components/SignedInNav';
import SignedOutNav from './components/SignedOutNav';
import ExchangeHistory from './pages/ExchangeHistory';
import Campaign from './pages/campaign';
import ResultsPage from './pages/ResultPage';
import BuyList from './pages/BuyList';
import TradePostPage from './pages/TradePostPage';
import TradeList from './pages/TradeList';
import TradeOffersList from './pages/TradeOffersList';

import ManagerHomePage from './pages/ManagerHomePage';
import ManagerAnalytics from './pages/ManagerAnalytics';
import ManagerFeedback from './pages/ManagerFeedback';
import ManagerPost from './pages/ManagerPost';

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
    error: {
      main: "#F46786",
    }
  }
});

function App() {
  const [loggedIn, setLoggedIn] = React.useState(false);
  const [privelage, setPrivelage] = useState(1);
  const [username, setUsername] = useState('');

  function logout() {
    const options = {
      method: 'POST',
      route: '/logout',
    };
    apiCall(() => {
      setLoggedIn(false);
    }
      , options);
  }

  return (
    <Fragment>
      <ThemeProvider theme={theme}>
        <Helmet bodyAttributes={{ style: 'background-color : #cccccc' }} />
        <Box sx={{ display: 'flex', flexDirection: 'column', rowGap: '10ch', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
          {!loggedIn
            ? <BrowserRouter>
              <SignedOutNav />
              <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/login" element={<SignIn setLogin={setLoggedIn} setPrivelage={setPrivelage} setUsername={setUsername} />} />
                <Route path="/register" element={<Register setLogin={setLoggedIn} setUsername={setUsername} />} />
              </Routes>
            </BrowserRouter>
            : <BrowserRouter>
              <SignedInNav logout={logout} username={username} />
              <Routes>
                {privelage === 1
                  ? <Route path="/" element={<HomePage />} />
                  : <Route path="/" element={<ManagerHomePage />} />
                }

                {/* <Route path="/" element={<ManagerHomePage/>} /> */}

                <Route path="/profile/:id" element={<Profile />} />
                <Route path="/wantlist" element={<WantList />} />
                <Route path="/collection" element={<CollectionList />} />
                <Route path="/exchange-history" element={<ExchangeHistory />} />
                <Route path="/dashboard" element={<span>Dashboard</span>} />
                <Route path="/dashboard" element={<HomePage />} />
                <Route path="/offers" element={<OffersList />} />
                <Route path="/trade" element={<SellPage />} />
                <Route path="/tradelist" element={<TradeList />} />
                <Route path="/tradelist/offers/:id" element={<TradeOffersList />} />
                <Route path='/campaign' element={<Campaign />} />
                <Route path='/search/:query' element={<ResultsPage />} />
                <Route path='search/' element={<ResultsPage/>} />
                <Route path="/collectible/:id" element={<CollectiblePage />} />
                <Route path="/collectible/buy/:id" element={<BuyList />} />
                <Route path="/trade/view/:id" element={<TradePostPage />} />

                <Route path="/manager/feedback" element={<ManagerFeedback />} />
                <Route path="/manager/post" element={<ManagerPost />} />
                <Route path="/manager/analytics" element={<ManagerAnalytics />} />

              </Routes>

            </BrowserRouter>
          }
        </Box>
      </ThemeProvider>
    </Fragment>
  );
}

export default App;
