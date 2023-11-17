import React, { useState, useEffect, useMemo } from "react";
import {
  useNavigate,
  useParams,
} from "react-router-dom";

import {
  MaterialReactTable,
  MRT_ToggleDensePaddingButton,
  MRT_FullScreenToggleButton,
} from 'material-react-table';

import { Box } from '@mui/material';
import { apiCall } from "../../App";

// Displays list of collectibles that matches the search query
// Clicking on a result takes the user to the collectible page
// Table sourced from https://github.com/KevinVandy/material-react-table/blob/v1/apps/material-react-table-docs/examples/custom-top-toolbar/sandbox/src/JS.js
function ResultsPage() {
  const { query } = useParams();
  const [results, setResults] = useState([]);

  const fetchData = (query_str) => {
    const options = {
      method: "GET",
      route: "/search"
    };
    apiCall((d) => {
      if (query_str === undefined) {
        setResults(d.collectibles);
      }
      else {
        const searchKey = d.collectibles.map(item => item.collectible_name);
        const searchResults = searchKey.filter(str =>
          str.toLowerCase().includes(query_str.toString().toLowerCase())
        );

        const filteredData = d.collectibles.filter(item => searchResults.includes(item.collectible_name));

        setResults(filteredData);
      }

    }, options);
  }


  useEffect(() => {
    fetchData(query);
  }, [query]);

  const navigate = useNavigate();

  const columns = useMemo(
    () => [
      {
        accessorKey: 'collectible_image',
        header: 'Collectible Image',
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
              height={100}
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
        header: 'Collectible Name',
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
  );

  return (
    <MaterialReactTable
      title="ResultsList"
      columns={columns}
      data={results}
      positionToolbarAlertBanner="bottom" //show selected rows count on bottom toolbar
      muiTableBodyRowProps={({ row }) => ({
        onClick: () => {
          navigate(`/collectible/${row.original.id}`)
        },
        sx: { cursor: 'pointer' },
      })}
      initialState={{ columnVisibility: { id: false } }}
      // changes sizing of default columns
      defaultColumn={{
        minSize: 50,
        maxSize: 500,
        size: 250,
      }}

      //customize built-in buttons in the top-right of top toolbar
      renderToolbarInternalActions={({ table }) => (

        <Box>
          <MRT_ToggleDensePaddingButton table={table} />
          <MRT_FullScreenToggleButton table={table} />
        </Box>
      )}

    />
  );
}

export default ResultsPage;