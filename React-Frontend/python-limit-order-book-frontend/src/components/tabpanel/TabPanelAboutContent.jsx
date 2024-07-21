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
          <Paper>
            <Typography variant="h2" sx={{ m: 3 }}>
              About
            </Typography>
          </Paper>
        </Box>
        <Box>
          <Typography>
            More detailed information about this project can be found on the
            <Link
              href="https://github.com/edward-b-1/Python-Limit-Order-Book"
              variant="body2"
              sx={{ ml: 0.5 }}
            >
              associated github page
            </Link>
            .
          </Typography>
        </Box>
        <Box sx={{ mt: 3 }}>
          <Paper>
            <Box sx={{ my: 3, mx: 2, pb: 2, pt: 1 }}>
              <Typography variant="h3" sx={{ m: 1, mb: 2 }}>
                Technology Stack
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                The backend is built with Python and FastAPI, which is a Python
                webserver framework.
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                The frontend is built with React and Material UI (MUI).
              </Typography>
            </Box>
          </Paper>
        </Box>
      </Box>

      <Box display="flex" justifyContent="center" alignItems="center" sx={{mb:2}}>
        <Link href="/about" variant="body2">
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
        <Box>
          <Link href="https://vitejs.dev" target="_blank">
            <img src={viteLogo} className="logo" alt="Vite logo" />
          </Link>
          <Link href="https://react.dev" target="_blank">
            <img src={reactLogo} className="logo react" alt="React logo"/>
          </Link>
        </Box>
        <Typography variant='h3' sx={{mt:3}}>Made with Vite + React</Typography>
      </Box>
    </>
  );
}
