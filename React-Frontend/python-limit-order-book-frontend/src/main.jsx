import React from 'react';
import ReactDOM from 'react-dom/client';
import { router } from './router'
import { RouterProvider } from 'react-router-dom';
import { ThemeProvider } from '@mui/material';
import { CssBaseline } from '@mui/material';
import { globalTheme } from './globalTheme';
import { globalThemeDark } from './globalThemeDark';

//import './index.css';

// const [light, setLight] = React.useState(true);
const light = true;

ReactDOM.createRoot(document.getElementById('root')).render(

  <React.StrictMode>
    <ThemeProvider theme={light ? globalTheme : globalThemeDark}>
      <CssBaseline />
      <RouterProvider router={router} />
    </ThemeProvider>
  </React.StrictMode>
);
