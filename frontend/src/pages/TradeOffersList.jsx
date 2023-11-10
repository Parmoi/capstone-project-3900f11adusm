import React, { useMemo } from 'react';

import {
    MaterialReactTable,
    MRT_ToggleDensePaddingButton,
    MRT_FullScreenToggleButton,
} from 'material-react-table';

import { Box, Button, IconButton } from '@mui/material';
import Avatar from '@mui/material/Avatar';

//Date Picker Imports
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import moment from 'moment';
import { useParams } from 'react-router-dom';
import { apiCall } from '../App';


// sourced from https://github.com/KevinVandy/material-react-table/blob/v1/apps/material-react-table-docs/examples/custom-top-toolbar/sandbox/src/JS.js
const TradeOffersList = () => {
    const [data, setData] = React.useState([]);

    const params = useParams();
    const t_id = params.id;

    const fetchData = () => {
        // call api with data
        const options = {
            method: 'GET',
            route: `/trade/list/offers?trade_id=${t_id}`,
        };

        apiCall((d) => {
            console.log(d);
            setData(d.offers_list);
        }, options)
            .then((res) => {
                if (res) {
                    // set error msg if api call returns error

                }
            });
    }

    React.useEffect(() => {
        fetchData();
    }, []);

    const columns = useMemo(
        //column definitions...
        () => [
            {
                accessorKey: 'offer_collectible_name',
                header: 'Collectible Offered',
            },
            {
                accessorKey: 'offer_collectible_img',
                header: 'Trade Item Image',
                Cell: ({ row }) => (
                    <Box
                        sx={{
                            display: 'flex',
                            gap: '1rem',
                        }}
                    >
                        <img
                            alt="trading collectible image"
                            height={60}
                            src={row.original.offer_collectible_img}
                            loading="lazy"
                        />
                    </Box>
                ),
                enableColumnActions: false,
                enableColumnFilter: false,
                enableSorting: false,
            },
            {
                accessorKey: 'trader_profile_img',
                header: 'Trader Profile',
                Cell: ({ row }) => (
                    <Box
                        sx={{
                            display: 'flex',
                            gap: '1rem',
                        }}
                    >
                        <Avatar alt="Trader Profile" src={row.original.trader_profile_img} />
                    </Box>
                ),
                enableColumnActions: false,
                enableColumnFilter: false,
            },
            {
                accessorKey: 'offer_made_date',
                accessorFn: (row) => moment(row.offer_made_date, "DD/MM/YYYY"), //convert to Date for sorting and filtering
                id: 'dateOffer',
                header: 'Date Offer Made',
                filterFn: 'lessThanOrEqualTo',
                sortingFn: 'datetime',

                Cell: ({ cell }) => cell.getValue()?.format('DD/MM/YY'), //render Date as a string
                Header: ({ column }) => <em>{column.columnDef.header}</em>, //custom header markup

                //Custom Date Picker Filter from @mui/x-date-pickers
                Filter: ({ column }) => (
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                        <DatePicker
                            onChange={(newValue) => {
                                column.setFilterValue(newValue);
                            }}

                            slotProps={{
                                textField: {
                                    helperText: 'Filter Mode: Less Than',
                                    sx: { minWidth: '120px' },
                                    variant: 'standard',
                                },
                            }}

                            value={column.getFilterValue()}
                            format="DD-MM-YYYY"
                        />
                    </LocalizationProvider>
                )
            },
        ],
        [],
        //end
    );

    return (
        <MaterialReactTable
            title="Tradelist"
            columns={columns}
            data={data}
            enableRowSelection
            enableMultiRowSelection={false}
            positionToolbarAlertBanner="bottom" //show selected rows count on bottom toolbar
            initialState={{ columnVisibility: { id: false } }}
            // changes sizing of default columns
            defaultColumn={{
                minSize: 50,
                maxSize: 300,
                size: 250,
            }}

            //add custom action buttons to top-left of top toolbar

            renderBottomToolbarCustomActions={({ table }) => {
                const handleDecline = () => {
                    table.getSelectedRowModel().flatRows.map((row) => {
                        const options = {
                            method: 'POST',
                            route: "/exchange/decline",
                            body: JSON.stringify({
                                offer_id: row.original.offer_id,
                            })
                        };
                        console.log(options)

                        apiCall(() => { }, options)
                            .then((res) => {
                                if (res) {
                                    // set error msg if api call returns error

                                }
                            });
                    });
                };

                const handleAccept = () => {
                    table.getSelectedRowModel().flatRows.map((row) => {
                        const options = {
                            method: 'POST',
                            route: "/exchange/accept",
                            body: JSON.stringify({
                                offer_id: row.original.offer_id,
                            })
                        };

                        apiCall(() => { }, options)
                            .then((res) => {
                                if (res) {
                                    // set error msg if api call returns error

                                }
                            });
                    });
                };

                return (
                    <Box sx={{ display: 'flex', gap: '1rem', p: '4px' }}>
                        <Button
                            color="secondary"
                            disabled={(!table.getIsSomeRowsSelected() && !table.getIsAllRowsSelected())}
                            onClick={handleAccept}
                            variant="contained"
                        >
                            Accept Offer
                        </Button>

                        <Button
                            color="error"
                            disabled={!table.getIsSomeRowsSelected() && !table.getIsAllRowsSelected()}
                            onClick={handleDecline}
                            variant="contained"
                        >
                            Decline Offer
                        </Button>
                    </Box>
                );

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
};


export default TradeOffersList;