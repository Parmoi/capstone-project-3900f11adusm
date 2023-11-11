import * as React from 'react';
import Box from '@mui/material/Box';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

const steps = ['Add title', 'Enter a description', 'Add images', 'Post listing'];

// Derived from https://mui.com/material-ui/react-stepper/
const CampaignStepper = ({ stepperContent }) => {
  const [activeStep, setActiveStep] = React.useState(0);

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
  };

  return (
    <Box sx={{ width: '100%', flex: 1 }}>
      <Stepper activeStep={activeStep} sx={{mt:'5vh'}}>
        {steps.map((label, index) => {
          const stepProps = {};
          const labelProps = {};
          return (
            <Step key={label} {...stepProps}>
              <StepLabel {...labelProps}>{label}</StepLabel>
            </Step>
          );
        })}
      </Stepper>
        <React.Fragment>
          <Box sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', mt: '20vh'  }}>
            {stepperContent[activeStep]}
          </Box>
          <Box>
            <Box sx={{ display: 'flex', flexDirection: 'row', pt: 2, mt: '15vh' }}>
              <Button
                color="inherit"
                disabled={activeStep === 0}
                onClick={handleBack}
                sx={{ position: 'absolute', left: 10, bottom: 10 }}
              >
                Back
              </Button>
              <Box sx={{ flex: '1 1 auto' }} />
              {activeStep !== steps.length - 1 
              ? <Button 
                  onClick={handleNext}
                  sx={{ position: 'absolute', right: 10, bottom: 10 }}
                >
                  Next
                </Button>
              : null}
            </Box>
          </Box>
        </React.Fragment>
    </Box>
  );
}

export default CampaignStepper;