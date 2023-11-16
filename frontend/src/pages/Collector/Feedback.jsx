import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { useNavigate, useLocation } from 'react-router-dom';
import { apiCall } from '../../App';
import Paper from '@mui/material/Paper';

// Page that allows user to add feedback for any particular campaign, which is sent to the manager
function Feedback() {
    const location = useLocation();
    const navigate = useNavigate();
    const [feedbackText, setFeedbackText] = React.useState("");
    const [showPopup, setShowPopup] = React.useState(false);
    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        const options = {
            method: 'POST',
            route: '/campaign/feedback',
            body: JSON.stringify({
              campaign_id: location.state?.id,
              feedback: data.get('feedback'),
            })
          };
      
          apiCall((d) => {
          }, options)
        setShowPopup(true);
        setTimeout(() => {
          setShowPopup(false); // Hide popup
          navigate("/dashboard"); // Navigate to dashboard
        }, 2000);
      };

    return (
    
    <Box 
      sx={{ 
        width: '100%', 
        height: '90.8vh', 
        display: "flex", 
        flexDirection: "column", 
        backgroundImage: `url("https://res.cloudinary.com/ddor5nnks/image/upload/v1699602264/gradient_background_zjdl6a.webp")`, 
        backgroundRepeat: "no-repeat", 
        backgroundSize: "cover", 
        alignItems: 'center', 
        justifyContent: 'center'
        }}
    >
      {showPopup && (
        <div style={{
          position: 'fixed',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          zIndex: 1000,
          backgroundColor: '#fff',
          padding: '70px',
          borderRadius: '10px',
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
          backgroundImage: `url("https://res.cloudinary.com/ddor5nnks/image/upload/v1699602264/gradient_background_zjdl6a")`,
          width: '500px',
          height: '200px',
          fontWeight: 'bold',
          fontSize: '25px'
        }}>
          Successfully submitted!
        </div>
      )}
    <Paper 
      component="main" 
      maxWidth="xs" 
      sx={{
        // mt: '15vh',
        borderRadius: 2,
        maxWidth: '700px',
        width: '100vw',
        paddingBottom: '100px',
        // height: '50vh',
      }}
    >
      <CssBaseline />
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Avatar sx={{ m: 2, bgcolor: 'support.main' }}>
        </Avatar>
        <Typography component="h1" variant="h5" color='primary.text'>
          <strong>Feedback</strong>
        </Typography>
        <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 1 }}>
          <TextField
            id="feedback"
            name="feedback"
            autoComplete="feedback"
            margin="normal"
            type='feedback'
            required
            fullWidth
            label="Write your feedback"
            autoFocus
            multiline
            rows={6}
            inputProps={{ maxLength: 500 }}
            value={feedbackText}
            onChange={(e) => setFeedbackText(e.target.value)}
          />
          
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2, backgroundColor: 'primary', color: 'secondary.main' }}
            name="Feedback"
          >
            Submit
          </Button>
          
        </Box>
      </Box>
    </Paper>
    </Box>

    );
}


export default Feedback;
