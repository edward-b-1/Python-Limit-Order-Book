import reactLogo from '../../assets/react.svg';
import viteLogo from '/vite.svg';

import { Typography, Box, Link } from '@mui/material';

export default function TabPanelAboutContent() {
  return (
    <>
      <Typography variant="h3">This is the about page</Typography>
      <Typography variant="h3">The backend is built with Python</Typography>
      <Typography variant="h3">
        The frontend is built with React and Material UI
      </Typography>
      <Typography variant="h3">
        Tech stack list: Python, FastAPI, React, MUI
      </Typography>

      <Box display="flex" justifyContent="center" alignItems="center">
        <Link href="/about" variant="body2">
          about the developer
        </Link>
      </Box>

      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Made with Vite + React</h1>
    </>
  );
}
