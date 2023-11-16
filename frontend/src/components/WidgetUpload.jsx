import { useEffect, useRef } from "react";
import { Box, Button } from '@mui/material';

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
            <Button variant="contained" onClick={() => widgetRef.current.open()} sx={style}>
                {buttonName}
            </Button>
        </Box>
    )
}

export default WidgetUpload;