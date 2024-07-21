import { Typography } from '@mui/material';
import { Box } from '@mui/material';
import TradesDisplayComponent from '../trades_tab/TradesDisplayComponent';

export default function TabPanelTradeRecordsContent() {
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
        <Typography>Trades</Typography>
      </Box>
      <TradesDisplayComponent></TradesDisplayComponent>
    </>
  );
}
