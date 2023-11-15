// import * as React from 'react';
// import Rating from '@mui/material/Rating';
// import StarIcon from '@mui/icons-material/Star';
// import Avatar from '@mui/material/Avatar';
// import Button from '@mui/material/Button';
// import CssBaseline from '@mui/material/CssBaseline';
// import TextField from '@mui/material/TextField';
// import Box from '@mui/material/Box';
// import Typography from '@mui/material/Typography';
// import { useTheme, ThemeProvider } from '@mui/material/styles';
// import { useNavigate } from 'react-router-dom';
// import { apiCall } from '../App';
// import Alert from '@mui/material/Alert';
// import Paper from '@mui/material/Paper';

// const labels = {
//     0.5: 'Useless',
//     1: 'Useless+',
//     1.5: 'Poor',
//     2: 'Poor+',
//     2.5: 'Ok',
//     3: 'Ok+',
//     3.5: 'Good',
//     4: 'Good+',
//     4.5: 'Excellent',
//     5: 'Excellent+',
//     };

// function getLabelText(value) {
//     return `${value} Star${value !== 1 ? 's' : ''}, ${labels[value]}`;
// }

// function Feedback() {
//     const [value, setValue] = React.useState(2);
//     const [hover, setHover] = React.useState(-1);

//     return (
//     // <Box
//     //     sx={{
//     //     width: 200,
//     //     display: 'flex',
//     //     alignItems: 'center',
//     //     }}
//     // >
//     //     <Rating
//     //     name="hover-feedback"
//     //     value={value}
//     //     precision={0.5}
//     //     getLabelText={getLabelText}
//     //     onChange={(event, newValue) => {
//     //         setValue(newValue);
//     //     }}
//     //     onChangeActive={(event, newHover) => {
//     //         setHover(newHover);
//     //     }}
//     //     emptyIcon={<StarIcon style={{ opacity: 0.55 }} fontSize="inherit" />}
//     //     />
//     //     {value !== null && (
//     //     <Box sx={{ ml: 2 }}>{labels[hover !== -1 ? hover : value]}</Box>
//     //     )}
//     // </Box>
//     <ThemeProvider theme={useTheme()}>
//     <Box 
//       sx={{ 
//         width: '100%', 
//         height: '90.8vh', 
//         display: "flex", 
//         flexDirection: "column", 
//         backgroundImage: `url("https://res.cloudinary.com/ddor5nnks/image/upload/v1699602264/gradient_background_zjdl6a.webp")`, 
//         backgroundRepeat: "no-repeat", 
//         backgroundSize: "cover", 
//         alignItems: 'center', 
//         justifyContent: 'center'
//         }}
//     >
//     <Paper 
//       component="main" 
//       maxWidth="xs" 
//       sx={{
//         // mt: '15vh',
//         borderRadius: 2,
//         maxWidth: '700px',
//         width: '50vw',
//         paddingBottom: '50px',
//         // height: '50vh',
//       }}
//     >
//       <CssBaseline />
//       <Box
//         sx={{
//           marginTop: 8,
//           display: 'flex',
//           flexDirection: 'column',
//           alignItems: 'center',
//         }}
//       >
//         <Avatar sx={{ m: 2, bgcolor: 'support.main' }}>
//         </Avatar>
//         <Typography component="h1" variant="h5" color='primary.text'>
//           Sign in
//         </Typography>
//         <Box component="form" onSubmit={login} noValidate sx={{ mt: 1 }}>
//           <TextField
//             margin="normal"
//             required
//             fullWidth
//             id="email"
//             label="Email Address"
//             name="email"
//             autoComplete="email"
//             autoFocus
//           />
//           <TextField
//             margin="normal"
//             required
//             fullWidth
//             name="password"
//             label="Password"
//             type="text"
//             id="password"
//             autoComplete="current-password"
//           />
//           <div>
//             {error ? <Alert severity='error'>{errContent}</Alert> : <></> }
//           </div>
//           <Button
//             type="submit"
//             fullWidth
//             variant="contained"
//             sx={{ mt: 3, mb: 2, backgroundColor: 'primary', color: 'secondary.main' }}
//             name="sign in"
//           >
//             Sign In
//           </Button>
          
//         </Box>
//       </Box>
//     </Paper>
//     </Box>
//   </ThemeProvider>

//     );
// }


// export default Feedback;
