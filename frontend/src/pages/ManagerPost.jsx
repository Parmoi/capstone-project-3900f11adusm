import * as React from 'react';
import CampaignStepper from "../components/CampaignStepper";
import Typography from '@mui/material/Typography';
import { Box, Button } from '@mui/material';
import FormControl from '@mui/material/FormControl';
import TextField from '@mui/material/TextField';

import { apiCall } from '../App';
import { useNavigate } from 'react-router-dom';

const ManagerPost = () => {
    const [collectibleName, setCollectibleName] = React.useState('');
    const [title, setTitle] = React.useState('');
    const [description, setDescription] = React.useState('');
    const [collectibles, setCollectibles] = React.useState([]);
    const navigate = useNavigate();

    const fetchData = () => {
        // call api with data
        const options = {
            method: 'GET',
            route: "/collection/get",
        };
    
        apiCall((d) => {
            console.log(d);
            setCollectibles(d.collection);
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

    const AddTitle = () => {
        const handleChange = (e) => {
            setTitle(e.target.value);
        }

        return (
            <Box sx={{height: '100%'}}>
                <Typography variant='h5' mb='50px'>Give a name for your campaign</Typography>
                <FormControl fullWidth>
                <TextField label="Title" onBlur={handleChange} variant="standard"/>
                </FormControl>
            </Box>
        );
    }

    const CollectibleDescription = () => {
        const handleChange = (e) => {
            setDescription(e.target.value);
        }
        return(
            <Box sx={{height: '100%'}}>
                <Typography variant='h5' mb='50px'>Add a description of your campaign</Typography>
                <FormControl fullWidth>
                    <TextField
                    id="outlined-multiline-static"
                    label="Description"
                    multiline
                    placeholder='Add description here...'
                    rows={3}
                    onBlur={handleChange}
                    />
                </FormControl>
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
                    placeholder='Add description here...'
                    rows={3}
                    sx={{mb:'30px'}}
                    aria-disabled
                    value={description}
                    />
                    <Button variant='contained' onClick={postData}>POST</Button>
                </FormControl>
            </Box>
        );
    }

    const stepperContent = [
        <AddTitle/>,
        <CollectibleDescription/>,
        <AddImages/>,
        <PostListing/>,
    ]

    return (
        <CampaignStepper stepperContent={stepperContent} />
    );
}


export default ManagerPost;