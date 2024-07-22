import React from 'react';

import { Typography } from '@mui/material';
import { Box } from '@mui/material';

import OrderControlPanelExampleHelp from '../order_control_tab/OrderControlPanelExampleHelp';
import OrderControlPanel from '../order_control_tab/OrderControlPanel';
import OrderEntryTopOfBookDisplayComponent from '../order_control_tab/OrderControlTopOfBookDisplayComponent';

export default function TabPanelOrderControlContent() {
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
        <Typography variant='h3' sx={{mb: 4}}>Order Control and Top Of Book Display</Typography>
      </Box>
      <OrderControlPanelExampleHelp></OrderControlPanelExampleHelp>
      <OrderControlPanel></OrderControlPanel>
      <OrderEntryTopOfBookDisplayComponent></OrderEntryTopOfBookDisplayComponent>
    </>
  );
}
