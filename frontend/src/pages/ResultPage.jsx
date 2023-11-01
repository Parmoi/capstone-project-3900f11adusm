import React, { useState, useEffect, useMemo  } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Link,
  useNavigate,
  useParams
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
  
    // Dummy data for demonstration
    const storedData = [
        {
          image: 'https://ilarge.lisimg.com/image/8825948/980full-homer-simpson.jpg',
          name: 'Homer',
          collectionName: 'Winter 2022',
          yearReleased: 1999,
          dateAdded: 1800,
        },
        {
          image: 'https://tse4.mm.bing.net/th?id=OIP.e4tAXeZ6G0YL4OE5M8KTwAHaMq&pid=Api',
          name: 'Marge',
          collectionName: 'Winter 2022',
          yearReleased: 1899,
          dateAdded: 1800,
        },
        {
          image: 'https://tse2.mm.bing.net/th?id=OIP.j7EknM6CUuEct_kx7o-dNQHaMN&pid=Api',
          name: 'Bart',
          collectionName: 'Winter 2022',
          yearReleased: 1499,
          dateAdded: 1800,
        },
        {
          image: 'https://tse3.mm.bing.net/th?id=OIP.6761X25CX3UUjklkDCnjSwHaHa&pid=Api',
          name: 'Dog',
          collectionName: 'Winter 2022',
          yearReleased: 1989,
          dateAdded: 1800,
        },
        {
          image: 'https://tse3.mm.bing.net/th?id=OIP.JqWjPHsW5aJIZDnPYMGovQHaJQ&pid=Api',
          name: 'Lisa',
          collectionName: 'Winter 2022',
          yearReleased: 1709,
          dateAdded: 1800,
        },
        {
          image: 'https://tse1.mm.bing.net/th?id=OIP.qVV8kcLdcLysZ5OOCzhKLAHaF7&pid=Api',
          name: 'Rando',
          collectionName: 'Winter 2022',
          yearReleased: 1909,
          dateAdded: 1801,
        },
      ];

    const searchKey = storedData.map(item => item.name)

    useEffect(() => {
      const searchResults = searchKey.filter((str) =>
        str.toLowerCase().includes(query.toLowerCase())
      );
      setResults(searchResults);
    }, [query]);

    const filteredData = storedData.filter(item => results.includes(item.name));

    const columns = useMemo(
        //column definitions...
        () => [
          {
            accessorKey: 'image',
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
            header: 'Name',
          },
          {
            accessorKey: 'collectionName',
            header: 'Collection Name',
          },
          {
            accessorKey: 'yearReleased',
            header: 'Year',
          },
          {
            accessorKey: 'dateAdded',
            header: 'Date Added',
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

    //add custom action buttons to top-left of top toolbar

    renderBottomToolbarCustomActions={({ table }) => (

      <Box sx={{ display: 'flex', gap: '1rem', p: '4px' }}>
        <Button
          color="secondary"
          disabled={!table.getIsSomeRowsSelected()}
          onClick={() => {
            // api call to backend
            // setData to new data
            alert('Move to collections');
          }}
          variant="contained"
        >
          Move to collections
        </Button>

        <Button
          color="error"
          disabled={!table.getIsSomeRowsSelected()}
          onClick={() => {
            // api call to backend
            // setData to new data
            alert('Delete selected collectibles');
          }}
          variant="contained"
        >
          Delete selected
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
    );
}

export default ResultsPage;