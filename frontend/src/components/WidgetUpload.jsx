import { useEffect, useRef } from "react";
import { Box, Button } from '@mui/material';

// Component for uploading images
// Takes in onSuccess and performs function if image is successfully updated
const WidgetUpload = ({ onSuccess, style, buttonName='Upload' }) => {
    const cloudinaryRef = useRef();
    const widgetRef = useRef();
    
    useEffect(() => {
        cloudinaryRef.current = window.cloudinary;
        widgetRef.current = cloudinaryRef.current.createUploadWidget({
            cloudName: 'ddor5nnks',
            uploadPreset: 'wwrzhd4r',
            max_files: '1',
        }, function(error, result) {
            if (result.event === "success") {
                onSuccess(result.info.secure_url);
            }
        });
    }, [])

    return (
        <Box sx={{ display: 'flex', justifyContent: "center" }}>
            <Button variant="contained" onClick={() => widgetRef.current.open()} sx={style}>
                {buttonName}
            </Button>
        </Box>
    )
}

export default WidgetUpload;