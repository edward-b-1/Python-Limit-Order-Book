import React from 'react';

import { Typography, Box } from '@mui/material';
import OrderBoard from '../order_board_tab/OrderBoard';

import axios from 'axios';

export default function TabPanelOrderBoardContent() {
  return (
    <>
      <Box
        sx={{
          py: 2,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Typography variant='h3'>Order Board</Typography>
      </Box>
      <OrderBoard></OrderBoard>
    </>
  );
}
