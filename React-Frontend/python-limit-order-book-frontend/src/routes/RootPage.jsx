import React from 'react';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import { Typography } from '@mui/material';

export default function RootPage() {
  const navigate = useNavigate();

  const gotoLandingPage = () => {
    navigate('/mainpage');
  };

  useEffect(() => {
    gotoLandingPage();
  }, []);

  return (
    <>
      <Typography>Root page</Typography>
    </>
  );
}
