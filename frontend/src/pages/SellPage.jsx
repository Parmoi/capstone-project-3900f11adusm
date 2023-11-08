import * as React from 'react';
import SellStepper from "../components/Stepper";
import Typography from '@mui/material/Typography';
import { Box, Button } from '@mui/material';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import TextField from '@mui/material/TextField';
import Alert from '@mui/material/Alert';

import { apiCall } from '../App';
import { useNavigate } from 'react-router-dom';

const SellPage = () => {
    const [collectibleID, setCollectibleID] = React.useState('');
    const [collectibleName, setCollectibleName] = React.useState('');
    const [title, setTitle] = React.useState('');
    const [description, setDescription] = React.useState('');
    const [collectibles, setCollectibles] = React.useState([]);
    const [isTitleAdded, setIsTitleAdded] = React.useState(false);
    const [isDescAdded, setIsDescAdded] = React.useState(false);
    const navigate = useNavigate();

    const fetchData = () => {
        // call api with data
        const options = {
            method: 'GET',
            route: "/collection/get",
        };
    
        apiCall((d) => {
            setCollectibles(d.collection);
            console.log(collectibles);
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

    const SelectCollectible = () => {
    
        const handleChange = (id, name) => {
            setCollectibleID(id);
            setCollectibleName(name);
            console.log(id, name);
        }
    
        return (
            <Box sx={{height: '100%'}}>
                <Typography variant='h5' mb='50px'>Select collectible you would like to trade/sell</Typography>
                <FormControl fullWidth>
                <InputLabel>Collectible</InputLabel>
                <Select
                    id='tradeCollectible'
                    value={collectibleID}
                    label="Collectible"
                >
                    {/* Render menu items for each collectible name in user's collection */}
                    {collectibles.map((collectible) => { 
                        return (
                            <MenuItem 
                                value={collectible.collectible_id}
                                onClick={() => handleChange(collectible.collectible_id, collectible.name)}
                            >
                                {collectible.name}
                            </MenuItem>)
                        })
                    }
                </Select>
                </FormControl>
            </Box>
        );
    }

    const AddTitle = () => {
        const postTitle = (e) => {
            e.preventDefault();
            const data = new FormData(e.currentTarget);
            setIsTitleAdded(true);
            setTitle(data.get('title'));
        }

        return (
            <Box component="form" onSubmit={postTitle} sx={{height: '100%'}}>
                <Typography variant='h5' mb='50px'>Add a title for your post</Typography>
                <TextField id='title' name='title' label="Title" variant="standard" onChange={() => setIsTitleAdded(false)}/>
                <Button type="submit" variant='contained' sx={{ m: 1, ml: '10px' }}>ADD</Button>
                { isTitleAdded ? <Alert severity='success'>Added title!</Alert> : ''}
            </Box>
        );
    }

    const CollectibleDescription = () => {
        const postDescription = (e) => {
            e.preventDefault();
            const data = new FormData(e.currentTarget);
            setIsDescAdded(true);
            setDescription(data.get('description'));
        }

        return(
            <Box component="form" onSubmit={postDescription} sx={{height: '100%', display: 'flex', flexDirection: 'column' }}>
                <Typography variant='h5' mb='50px'>Add a description of your collectible</Typography>
                <TextField
                    name="description"
                    id="outlined-multiline-static"
                    label="Description"
                    multiline
                    placeholder='Add description here...'
                    rows={3}
                    onChange={() => setIsDescAdded(false)}
                />
                { isDescAdded ? <Alert severity='success'>Added description!</Alert> : <></>}
                <Button 
                variant='contained' 
                type="submit" 
                sx={{ mt: '10px'}}
                >
                    ADD
                </Button>
            </Box>
        );
    }

    const AddImages = () => {
        const [selectedFiles, setSelectedFiles] = React.useState([]);

        const handleChange = () => {

        }

        function handleFileUpload() {
            // apicall
        }

        // const handleUpload = () => {
        //     const files = Array.from(selectedFiles);
        
        // }

        // const selectFiles = (event) => {
        //     let images = [];
        
        //     for (let i = 0; i < event.target.files.length; i++) {
        //       images.push(URL.createObjectURL(event.target.files[i]));
        //     }
        
        //     setSelectedFiles(event.target.files);
        //   };
        return (
            <Box sx={{height: '100%'}}>
                <Typography variant='h5' mb='50px'>Add images of your collectible</Typography>
                <input type="file" multiple accept=".jpg, .jpeg, .png" onChange={handleChange}/>
                <Button>Upload</Button>
            </Box>
        );
    }

    const PostListing = () => {
        const postData = () => {
            // api call to post new trade
            const options = {
                method: "POST",
                route: "/trade/post",
                body: JSON.stringify({
                    collection_id: collectibleID,
                    post_images: [],
                    post_title: title,
                    post_description: description,
                  }),
            };
          
            apiCall(() => {
                navigate('/');
            }, options)
            .then((res) => {
                if (res) {
                // set error msg if api call returns error
        
                }
            });
        }

        function dataError () {
            return (collectibleName === '' || title === '' || description === '');
        }

        return(
            <Box sx={{height: '100%'}}>
                <Typography variant='h5' mb='50px'>Check new trade post</Typography>
                <FormControl fullWidth>
                    <TextField label="Collectible Name" variant="standard" aria-disabled value={collectibleName} sx={{mb:'30px'}}/>
                    <TextField label="Title" variant="standard" aria-disabled value={title} sx={{mb:'30px'}}/>
                    <TextField
                    id="outlined-multiline-static"
                    label="Description"
                    multiline
                    rows={3}
                    aria-disabled
                    value={description}
                    sx={{ mb: '10px' }}
                    />
                    { dataError() ? <Alert severity='error' sx={{ mb: '10px' }}>Missing some fields!</Alert> : <></>}
                    <Button variant='contained' disabled={dataError()} onClick={postData}>POST</Button>
                </FormControl>
            </Box>
        );
    }

    const stepperContent = [
        <SelectCollectible />,
        <AddTitle/>,
        <CollectibleDescription/>,
        <AddImages/>,
        <PostListing/>,
    ]

    return (
        <SellStepper stepperContent={stepperContent} />
    );
}

export default SellPage;