import * as React from 'react';
import SellStepper from "../components/Stepper";
import Typography from '@mui/material/Typography';

const SelectCollectible = () => {
    return (
        <Typography variant='h5'>Select collectible you would like to trade/sell</Typography>
    );
}

const stepperContent = [
    <SelectCollectible />,

]

const SellPage = () => {

    return (
        <SellStepper stepperContent={stepperContent} />
    );
}

export default SellPage;