import { useEffect, useRef } from "react";

const WidgetUpload = () => {
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
                console.log('The url to the image');
                console.log(result.info.secure_url); // The URL to the image.

                // widgetRef.current.close(); This immedietely closes the widget.
            }
        });
    }, [])

    return (
        <button onClick={() => widgetRef.current.open()}>
            Upload
        </button>
    )
}

export default WidgetUpload;