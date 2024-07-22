import React from 'react';

import reactLogo from '../../assets/react.svg';
import viteLogo from '/vite.svg';

import { Typography, Box, Link, Paper } from '@mui/material';

export default function TabPanelAboutContent() {
  return (
    <>
      <Box>
        <Box
          sx={{
            py: 2,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            width: 1,
          }}
        >
          <Paper sx={{ backgroundColor: 'background.whitesmoke' }}>
            <Typography variant="h2" sx={{ m: 3, px: 20 }}>
              About
            </Typography>
          </Paper>
        </Box>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Typography variant="body2">
            More detailed information about this project can be found on the
            <Link
              href="https://github.com/edward-b-1/Python-Limit-Order-Book"
              variant="body2"
              underline="hover"
              sx={{ ml: 0.5 }}
            >
              associated github page
            </Link>
            .
          </Typography>
        </Box>
        <Box sx={{ mt: 3 }}>
          <Paper sx={{ backgroundColor: 'background.whitesmoke' }}>
            <Box sx={{ my: 3, mx: 2, pb: 2, pt: 1 }}>
              <Typography variant="h3" sx={{ m: 1, mb: 2 }}>
                Technology Stack
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                The backend is built with Python and FastAPI, which is a Python
                webserver framework.
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                The frontend is built with React, Vite and Material UI (MUI).
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                The whole system is deployed to the cloud using a Linode server.
                <Link href="https://www.linode.com/choosing-linode/"></Link>
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                The Python code is Dockerized, meaning that a Docker container
                is used to deploy all of the Python code which is part of the
                backend server. The frontend is a static site, which is hosted
                using Nginx. Nginx is configured to act as a reverse-proxy for
                calls to the backend API.
              </Typography>
            </Box>
          </Paper>
        </Box>
      </Box>

      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        sx={{ mt: 4, mb: 4 }}
      >
        <Link href="/about" variant="body2" underline="hover" fontSize={'1.1rem'}>
          about the developer
        </Link>
      </Box>

      <Box
        sx={{
          py: 2,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          width: 1,
        }}
      >
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'row',
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          <Box sx={{ mr: 2 }}>
            <Link href="https://vitejs.dev" target="_blank">
              <img
                src={viteLogo}
                className="logo"
                width={100}
                alt="Vite logo"
              />
            </Link>
          </Box>
          <Box sx={{ ml: 2 }}>
            <Link href="https://react.dev" target="_blank">
              <img
                src={reactLogo}
                className="logo react"
                width={100}
                alt="React logo"
              />
            </Link>
          </Box>
        </Box>
        <Typography variant="h4" fontStyle={'italic'} sx={{ mt: 3 }}>
          Made with Vite + React
        </Typography>
      </Box>
    </>
  );
}
