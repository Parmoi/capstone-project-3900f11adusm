import * as React from 'react';

import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

import { LineChart } from '@mui/x-charts/LineChart';

const pData = [24, 13, 98, 39, 48, 38, 43];
const xLabels = [
  '2023/10/20',
  '2023/10/21',
  '2023/10/22',
  '2023/10/23',
  '2023/10/24',
  '2023/10/25',
  '2023/10/26',
];


function ManagerAnalytics() {
  return (
    <LineChart
      width={1200}
      height={800}
      backgroundColor={'White'}
      series={[
        { data: pData, label: 'Simpsons', id: 'pvId' },
      ]}
      xAxis={[{ scaleType: 'point', data: xLabels }]}
      sx={{
        '.MuiLineElement-root, .MuiMarkElement-root': {
          strokeWidth: 1,
        },
        '.MuiLineElement-series-pvId': {
          strokeDasharray: '5 5',
        },
        '.MuiLineElement-series-uvId': {
          strokeDasharray: '3 4 5 2',
        },
        '.MuiMarkElement-root:not(.MuiMarkElement-highlighted)': {
          fill: '#fff',
        },
        '& .MuiMarkElement-highlighted': {
          stroke: 'none',
        },
      }}
    />
  );
}


export default ManagerAnalytics;