import React from 'react';
import ReactDOM from 'react-dom/client';
import { router } from './router'
import { RouterProvider } from 'react-router-dom';
import { ThemeProvider } from '@mui/material';
import { globalTheme } from './globalTheme';

//import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ThemeProvider theme={globalTheme}>
      <RouterProvider router={router} />
    </ThemeProvider>
  </React.StrictMode>
);
