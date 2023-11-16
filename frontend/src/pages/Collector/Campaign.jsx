import React, { useMemo, useEffect } from 'react';

import {

  MaterialReactTable,

  MRT_ToggleDensePaddingButton,

  MRT_FullScreenToggleButton,

} from 'material-react-table';

import { Box, Button,Typography} from '@mui/material';
import { useLocation } from 'react-router-dom';
import Timer from '../../components/Timer'

// sourced from https://github.com/KevinVandy/material-react-table/blob/v1/apps/material-react-table-docs/examples/custom-top-toolbar/sandbox/src/JS.js
const Campaign = () => {
  const location = useLocation();
  const [data, setData] = React.useState([]);
  const campaignId = location.state?.id;

  const fetchData = () => {

    const options = {
      method: "GET",
      route: `/campaign/get_collectibles?campaign_id=${campaignId}`,
      
    };
    apiCall((d) => {
        console.log(d["collectibles"]);
        setData(d["collectibles"]);
    }, options)
    ;
  }
  
  
  useEffect(() => {
    fetchData();
  }, []);


  const columns = useMemo(    
    //column definitions...
    () => [
      {
        accessorKey: 'image',
        header: 'Collectible Image',
        Cell: ({ row }) => (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '1rem',
              minWidth: '500px'
            }}
          >
            <img
              alt="collectible image"
              height={50}
              src={row.original.image}
              loading="lazy"
            />
          </Box>

        ),
        enableColumnActions: false,
        enableColumnFilter: false,
      },
      {
        accessorKey: 'name',
        header: 'Collectible Name',
      },
      {
        accessorKey: 'description',
        header: 'Description',
      },
    ],
    [],
    //end
  );

  
  // const query = location.state?.
  const navigate = useNavigate();  
  const goFeedback = () => {
    navigate("/feedback", {state: {name: location.state?.name, id:location.state?.id}});
  }
  console.log(data)

  return (
    <>
      <Box sx={{ my: 0, }}>
        <Typography variant="h2" align="center" color="#2c3e50" gutterBottom>
          {location.state?.name}
        </Typography>
        <Timer startDate={location.state?.start_date} endDate={location.state?.end_date}></Timer>
      </Box>
      <MaterialReactTable
        title="Collectibles"
        columns={columns}
        data={data}
        enableRowSelection
        positionToolbarAlertBanner="bottom" //show selected rows count on bottom toolbar
        style={{minWidth: '1000px'}}
        muiTableBodyRowProps={({ row }) => ({
          onClick: () => {
            navigate(`/collectible/${row.original.id}`)
          },
          sx: { cursor: 'pointer' },
        })}
        //add custom action buttons to top-left of top toolbar

        renderBottomToolbarCustomActions={({ table }) => (

          <Box sx={{ display: 'flex', gap: '1rem', p: '4px' }}>
            <Button
              backgroundColor = 'primary'
              onClick={(goFeedback)}
              variant="contained"
            >
              Give Your Feedback
            </Button>
          </Box>

        )}

        //customize built-in buttons in the top-right of top toolbar

        renderToolbarInternalActions={({ table }) => (

          <Box>
            {/* add custom button to print table  */}
            <MRT_ToggleDensePaddingButton table={table} />
            <MRT_FullScreenToggleButton table={table} />
          </Box>
        )}

      />
    </>
  );
};


export default Campaign;