import React, { useState, useEffect, useMemo  } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Link,
  useNavigate,
  useParams,
} from "react-router-dom";

import {

  MaterialReactTable,

  MRT_ToggleDensePaddingButton,

  MRT_FullScreenToggleButton,

} from 'material-react-table';

import { Box, Button, IconButton } from '@mui/material';
import { apiCall } from "../App";

function ResultsPage() {
    const { query } = useParams();
    const [results, setResults] = useState([]);

    // const fetchData = () => {
    //   const options = {
    //     method: 'GET',
    //     route: '/search/:query'
    //   };
    //   apiCall((d) => {
    //     setResults(d["collectibles"]);
    //   }, options)
    //   ;
    // }
      const storedData =  [
        {
            campaign_name: "random",
            collectible_description: "hahahahahah!",
            collectible_image: "https://tse1.mm.bing.net/th?id=OIP.qVV8kcLdcLysZ5OOCzhKLAHaF7&pid=Api",
            collectible_name: "new_collectible!",
            date_released: "30/12/2020"
        },
        {
          campaign_name: "random",
          collectible_description: "hahahahahah!",
          collectible_image: "https://tse3.mm.bing.net/th?id=OIP.JqWjPHsW5aJIZDnPYMGovQHaJQ&pid=Api",
          collectible_name: "banana",
          date_released: "30/12/2020"
        },
        {
          campaign_name: "random",
          collectible_description: "hahahahahah!",
          collectible_image: "https://tse3.mm.bing.net/th?id=OIP.6761X25CX3UUjklkDCnjSwHaHa&pid=Api",
          collectible_name: "apple",
          date_released: "30/12/2020"
        },
      ]
    
    
    useEffect(() => {
      const searchKey = storedData.map(item => item.collectible_name)
      const searchResults = searchKey.filter((str) =>
        str.toLowerCase().includes(query.toLowerCase())
      );
      setResults(searchResults);
    }, [query]);

    const filteredData = storedData.filter(item => results.includes(item.collectible_name));


    const navigate = useNavigate();

    const columns = useMemo(
        //column definitions...
        () => [
          {
            accessorKey: 'collectible_image',
            header: 'Image Placeholder',
            Cell: ({ row }) => (
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '1rem',
                }}
              >
                <img
                  alt="collectible image"
                  height={50}
                  src={row.original.collectible_image}
                  loading="lazy"
                />
              </Box>
    
            ),
            enableColumnActions: false,
            enableColumnFilter: false,
          },
          {
            accessorKey: 'collectible_name',
            header: 'Name',
          },
          {
            accessorKey: 'campaign_name',
            header: 'Campaign Name',
          },
          {
            accessorKey: 'date_released',
            header: 'Date Added',
          },
          {
            accessorKey: 'collectible_description',
            header: 'Description',
          },
        ],
        [],
        //end
      );
  
    return (
    //   <div style={{textAlign: 'left'}}>
    //     <h1 >Results for "{query}"</h1>
    //   </div>
    <MaterialReactTable
    title="Wantlist"
    columns={columns}
    data={filteredData}
    enableRowSelection
    positionToolbarAlertBanner="bottom" //show selected rows count on bottom toolbar
    muiTableBodyRowProps={({ row }) => ({
      onClick: () => {
        navigate(`/collectible/${row.id}`)
      },
      sx: { cursor: 'pointer' },
    })}

    //add custom action buttons to top-left of top toolbar

    renderBottomToolbarCustomActions={({ table }) => (

      <Box sx={{ display: 'flex', gap: '1rem', p: '4px' }}>
        
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
    );
}

export default ResultsPage;