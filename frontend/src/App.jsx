import './App.css';
import React, { Fragment } from 'react';
import Box from '@mui/material/Box';
import { ThemeProvider, createTheme } from "@mui/material/styles";

import SignIn from './pages/Collector/SignIn';
import Register from './pages/Collector/Register';
import Profile from './pages/Collector/Profile';
import WantList from './pages/Collector/WantList';
import CollectionList from './pages/Collector/CollectionList';
import HomePage from './pages/Collector/HomePage';
import CollectiblePage from './pages/Collector/CollectiblePage';

import OffersList from './pages/Collector/OffersList';
import SellPage from './pages/Collector/SellPage';
import LandingPage from './pages/Collector/LandingPage';
import SignedInNav from './components/SignedInNav';
import SignedOutNav from './components/SignedOutNav';
import AdminSignedInNav from './components/AdminSignedInNav';
import ExchangeHistory from './pages/Collector/ExchangeHistory';
import Campaign from './pages/Collector/Campaign';
import ResultsPage from './pages/Collector/ResultPage';
import BuyList from './pages/Collector/BuyList';
import TradePostPage from './pages/Collector/TradePostPage';
import TradeList from './pages/Collector/TradeList';
import TradeOffersList from './pages/Collector/TradeOffersList';
import Feedback from './pages/Collector/Feedback';

import ManagerHomePage from './pages/Manager/ManagerHomePage';
import ManagerAnalytics from './pages/Manager/ManagerAnalytics';
import ManagerFeedback from './pages/Manager/ManagerFeedback';
import ManagerPost from './pages/Manager/ManagerPost';
import ManagerRegister from './pages/Manager/ManagerRegister';

import AdminHomePage from './pages/Admin/AdminHomePage';
import AdminManageManagers from './pages/Admin/AdminManageManagers';
import AdminCampaignApproval from './pages/Admin/AdminCampaignApproval';
import AdminManageCollectors from './pages/Admin/AdminManageCollectors';

import { useState } from 'react';

import {
  BrowserRouter,
  Routes,
  Route,
} from 'react-router-dom';

const PORT = 5000;

// Account Privileges
const BANNED = 0
const COLLECTOR = 1;
const MANAGERPENDING = 2;
const MANAGER = 3;
const ADMIN = 4;

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
  const [privilege, setPrivilege] = useState(1);
  const [username, setUsername] = useState('');
  const [userId, setUserId] = useState(0);

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

  // Changes background to gradient image
  document.body.style.backgroundImage = `url("https://res.cloudinary.com/ddor5nnks/image/upload/v1699602264/gradient_background_zjdl6a.webp")`;
  document.body.style.backgroundSize = 'cover';
  document.body.style.backgroundRepeat = 'no-repeat';

  return (
    <Fragment>
      <ThemeProvider theme={theme}>
        <Box 
          sx={{ 
            display: 'flex', 
            flexDirection: 'column', 
            rowGap: '10ch', 
            alignItems: 'center', 
            justifyContent: 'center', 
            height: '100%',
         }}
        >
          {!loggedIn
            ? <BrowserRouter>
              <SignedOutNav />
              <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/login" element={<SignIn setUserId={setUserId} setLogin={setLoggedIn} setPrivilege={setPrivilege} setUsername={setUsername} />} />
                <Route path="/register" element={<Register setUserId={setUserId} setLogin={setLoggedIn} setUsername={setUsername} />} />
                <Route path="/manager/register" element={<ManagerRegister setLogin={setLoggedIn} setUsername={setUsername} />} />
              </Routes>
            </BrowserRouter>
            : <BrowserRouter>
              { (privilege === ADMIN || privilege === MANAGER) 
                ? <AdminSignedInNav logout={logout} username={username}/>
                : <SignedInNav userId={userId} logout={logout} username={username} />
              }
              <Routes>
                { privilege === COLLECTOR && <Route path="/" element={<HomePage/>} />}
                { (privilege === MANAGERPENDING || privilege === MANAGER) && <Route path="/" element={<ManagerHomePage/>} />}
                { privilege === ADMIN && <Route path="/" element={<AdminHomePage/>} />}

                <Route path="/profile/:id" element={<Profile privilege={privilege} user_id={userId}/>} />
                <Route path="/wantlist" element={<WantList />} />
                <Route path="/collection" element={<CollectionList />} />
                <Route path="/exchange-history" element={<ExchangeHistory />} />  
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
                <Route path="/feedback" element={<Feedback />}></Route>
                <Route path="/manager/feedback" element={<ManagerFeedback />} />
                <Route path="/manager/post" element={<ManagerPost />} />
                <Route path="/manager/analytics" element={<ManagerAnalytics />} />
                <Route path='/manage/managers' element={<AdminManageManagers/>} />
                <Route path='/campaign/approval' element={<AdminCampaignApproval/>} />
                <Route path='/manage/collectors' element={<AdminManageCollectors/>} />

              </Routes>

            </BrowserRouter>
          }
        </Box>
      </ThemeProvider>
    </Fragment>
  );
}

export default App;
