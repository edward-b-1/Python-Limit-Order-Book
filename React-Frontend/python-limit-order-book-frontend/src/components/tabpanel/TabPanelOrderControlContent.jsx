import { Typography } from '@mui/material';
import { Box } from '@mui/material';

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
        <Typography variant='h3'>Order Control and Top Of Book Display</Typography>
      </Box>
      <OrderControlPanel></OrderControlPanel>
      <OrderEntryTopOfBookDisplayComponent></OrderEntryTopOfBookDisplayComponent>
    </>
  );
}
