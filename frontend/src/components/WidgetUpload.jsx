import { useEffect, useRef } from "react";
import { Box, Button } from '@mui/material';

const WidgetUpload = ({ onSuccess }) => {
    const cloudinaryRef = useRef();
    const widgetRef = useRef();
    
    useEffect(() => {
        cloudinaryRef.current = window.cloudinary;
        widgetRef.current = cloudinaryRef.current.createUploadWidget({
            cloudName: 'ddor5nnks',
            uploadPreset: 'wwrzhd4r'
        }, function(error, result) {
            if (result.event === "success") {
                console.log(result);
                // console.log('The url to the image');
                // console.log(result.info.secure_url); // The URL to the image.
                onSuccess(result.info.secure_url);
                // widgetRef.current.close(); This immedietely closes the widget.
            }
        });
    }, [])

    return (
        <Box sx={{ display: 'flex', justifyContent: "center" }}>
            <Button onClick={() => widgetRef.current.open()}>
                Upload
            </Button>
        </Box>
    )
}

export default WidgetUpload;