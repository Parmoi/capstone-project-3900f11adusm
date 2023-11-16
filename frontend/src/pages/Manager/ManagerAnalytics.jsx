import * as React from 'react';

import { useTheme, ThemeProvider } from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';


import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';

import { LineChart } from '@mui/x-charts/LineChart';

import { apiCall } from '../../App';

import { useState, useEffect } from 'react';

// const pData = [24, 13, 98, 39, 48, 38, 43];
// const xLabels = [
//   '2023/10/20',
//   '2023/10/21',
//   '2023/10/22',
//   '2023/10/23',
//   '2023/10/24',
//   '2023/10/25',
//   '2023/10/26',
// ];

const TableColor = [
  '#4e79a7',
  '#f28e2c',
  '#e15759',
  '#76b7b2',
  '#59a14f',
  '#edc949',
  '#af7aa1',
  '#ff9da7',
  '#9c755f',
  '#bab0ab',
];


function ManagerAnalytics() {
  const [campaign, setCampaign] = React.useState('');
  const [color, setColor] = React.useState('#4e79a7');
  const [analytics, setAnaltyics] = React.useState([
      {
          "campaign_id": 5,
          "campaign_name": "Galapagos Dove",
          "exchange_dates": ['2023/04/20', '2023/04/21', '2023/04/22', '2023/04/23', '2023/04/24', '2023/04/25', '2023/04/26'],   
          "exchanges_made": [24, 13, 98, 39, 48, 38, 43]
      },
  ]);

  const [xLabels, setXLables] = React.useState([]);
  const [yData, setYData] = React.useState([]);

  const fetchInfo = () => {
    const options = {
      method: 'GET',
      route: '/manager/analytics'
    };

    apiCall((d) => {
      if (d.length != 0) {
        setAnaltyics(d);
      }
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

  const handleColorChange = (event, nextColor) => {
    setColor(nextColor);
  };

  const handleChange = (event) => {
    setCampaign(event.target.value);
    setXLables(analytics.filter((x) => x.campaign_id == event.target.value)[0].exchange_dates);
    setYData(analytics.filter((y) => y.campaign_id == event.target.value)[0].exchanges_made);

  };

  return (
    <ThemeProvider theme={useTheme()}>
      <Box 
        sx={{ 
          width: '100%', 
          height: '100%', 
          display: "flex", 
          flexDirection: "column", 
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
            padding: '20px',

          }}
        >
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
          <FormControl fullWidth>
            <InputLabel id="Select Campaign">Select Campaign</InputLabel>
            <Select
              labelId="Select Campaign"
              id="select-campaign"
              value={campaign}
              label="Campaign"
              onChange={handleChange}
            >
              {analytics.map((data) => (
                <MenuItem key={data.campaign_id} value={data.campaign_id}>{data.campaign_name}</MenuItem>
              ))}
            </Select>
          </FormControl>
              
          </Box>
        </Paper>

        <Paper
          component="main" 
          maxWidth="lg" 
          sx={{
            marginTop: '8vh',
            borderRadius: 2,
            maxWidth: '75%',
            width: '80vw',
            MarginBottom: '200px',
          }}
        >
          {
            analytics == [] || campaign == ''
            ? <Stack direction="column" spacing={2} alignItems="center" sx={{ width: '100%', padding: '25px' }}>
            <Typography>There is no Data to Display</Typography>
            </Stack>
            : <Stack direction="column" spacing={2} alignItems="center" sx={{ width: '100%', padding: '25px' }}>
            <LineChart
              width={1000}
              height={500}
              margin={{ top: 10, bottom: 20 }}
              backgroundColor={'Black'}
              series={[
                { data: yData, label: 'Exchanges', id: 'yData', color, },
              ]}
              xAxis={[{ scaleType: 'point', data: xLabels }]}
              sx={{
                '.MuiMarkElement-root:not(.MuiMarkElement-highlighted)': {
                  fill: '#fff',
                },
                '& .MuiMarkElement-highlighted': {
                  stroke: 'none',
                },
                marginBottom: '20px',
              }}
            />
            <ToggleButtonGroup
              // orientation="vertical"
              value={color}
              exclusive
              onChange={handleColorChange}
            >
              {TableColor.map((value) => (
                <ToggleButton key={value} value={value} sx={{ p: 1 }}>
                  <div
                    style={{
                      width: 15,
                      height: 15,
                      backgroundColor: value,
                      display: 'inline-block',
                    }}
                  />
                </ToggleButton>
              ))}
            </ToggleButtonGroup>
          </Stack>
          }
        </Paper>
      </Box>
    </ThemeProvider>
  );

}


export default ManagerAnalytics;