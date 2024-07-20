
import { ThemeProvider, createTheme } from '@mui/material';


const theme = createTheme(
    {
      palette: {
        mode: 'light',
        primary: {
          main: '#3f51b5',
        },
        secondary: {
          main: '#f50057',
        },
      },
    }
  );


    //{
    // palette: {
    //   primary: {
    //     main: '#013e87',
    //   },
    //   secondary: {
    //     main: '#2e74c9',
    //   },
    //   paper: {
    //     main: '#dfdfdf',
    //   },
    //   typography: {
    //     h1: {
    //       fontSize: "3rem",
    //       fontWeight: 600,
    //     },
    //     h2: {
    //       fontSize: "1.75rem",
    //       fontWeight: 600,
    //     },
    //     h3: {
    //       fontSize: "1.5rem",
    //       fontWeight: 600,
    //     },
    //   }
    // },
    //}

  // <ThemeProvider theme={theme}>
  // <App />
  // </ThemeProvider>
