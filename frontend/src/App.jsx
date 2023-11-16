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
import AdminSignedInNav from './components/AdminSignedInNav';
import ExchangeHistory from './pages/ExchangeHistory';
import Campaign from './pages/campaign';
import ResultsPage from './pages/ResultPage';
import BuyList from './pages/BuyList';
import TradePostPage from './pages/TradePostPage';
import TradeList from './pages/TradeList';
import TradeOffersList from './pages/TradeOffersList';

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

const COLLECTOR = 1;
const MANAGER = 2;
const ADMIN = 3;

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
                {/* { (privilege === 2 || privilege === 3) && <Route path="/" element={<ManagerHomePage/>} />} */}
                { privilege === MANAGER && <Route path="/" element={<ManagerHomePage/>} />}
                { privilege === ADMIN && <Route path="/" element={<AdminHomePage/>} />}

                <Route path="/profile/:id" element={<Profile privilege={privilege} user_id={userId}/>} />
                <Route path="/wantlist" element={<WantList />} />
                <Route path="/collection" element={<CollectionList />} />
                <Route path="/exchange-history" element={<ExchangeHistory />} />
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
