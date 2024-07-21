
import { createTheme } from '@mui/material/styles';

export const globalTheme = createTheme({
  typography: {
    body1: {
      fontWeight: 400,
      fontSize: '1.0rem',
    },
    body2: {
      fontWeight: 500,
      fontSize: '1.0rem',
    },
    button: {
      fontWeight: 500,
      fontSize: '1.0rem',
      textTransform: '',
    },
    caption: {

    },
    overline: {

    },
    h1: {
      fontSize: '4rem',
      fontWeight: 350,
    },
    h2: {
      fontSize: '3rem',
    },
    h3: {
      fontSize: '2rem',
    },
    h4: {
      fontSize: '1.75rem',
    },
    h5: {
      fontSie: '1.5rem',
    },
    h6: {
      fontSize: '1.3rem',
    },
    subtitle1: {

    },
    subtitle2: undefined,
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(','),
  },
});
