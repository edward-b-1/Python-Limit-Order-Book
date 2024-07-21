import React from 'react';
import { useState } from 'react';

// import axios from 'axios';
import { Button, Container, TextField, Typography, Paper } from '@mui/material';

// import Tabs from '@mui/material/Tabs';

import Box from '@mui/material/Box';
import Tab from '@mui/material/Tab';
import TabContext from '@mui/lab/TabContext';
import TabList from '@mui/lab/TabList';
import TabPanel from '@mui/lab/TabPanel';

//import Tab from '@mui/material/Tab';

import TabPanelOrderControlContent from '../components/tabpanel/TabPanelOrderControlContent';
import TabPanelOrderBoardContent from '../components/tabpanel/TabPanelOrderBoardContent';
import TabPanelTradeRecordsContent from '../components/tabpanel/TabPanelTradeRecordsContent';
import TabPanelOrderBookStatisticsContent from '../components/tabpanel/TabPanelOrderBookStatisticsContent';
import TabPanelServerPerformanceStatisticsContent from '../components/tabpanel/TabPanelServerPerformanceStatisticsContent';
import TabPanelAccountSettingsContent from '../components/tabpanel/TabPanelAccountSettingsContent';
import TabPanelAboutContent from '../components/tabpanel/TabPanelAboutContent';
import TabPanelHelpContent from '../components/tabpanel/TabPanelHelpContent';

export default function MainPage() {
  const [selectedTabIndex, setSelectedTabIndex] = useState('1');
  const handleChange = (event, newValue) => {
    setSelectedTabIndex(newValue);
  };

  return (
    <>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <Container
          sx={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
          }}
        >
          <Paper elevation={4} sx={{ mt: 4, backgroundColor: 'textfieldBackgroundColor' }}>
            <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
              }}
            >
              <Typography
                variant="h1"
                sx={{ p: 2, mt: 4, color: 'primary.main' }}
              >
                Limit Order Book Interface with React
              </Typography>
            </Box>
          </Paper>
          <Box sx={{ py: 2 }}></Box>

          <Box sx={{ width: '100%' }}>
            <TabContext value={selectedTabIndex}>
              <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                <TabList
                  onChange={handleChange}
                  aria-label="lab API tabs example"
                >
                  <Tab label="Order Entry" value="1" />
                  <Tab label="Order Board" value="2" />
                  <Tab label="Trade Records" value="3" />
                  <Tab label="Book Statistics" value="4" />
                  <Tab label="Server Statistics" value="5" />
                  <Tab label="Account Settings" value="6" />
                  <Tab label="About" value="7" />
                  <Tab label="Help" value="8" />
                </TabList>
              </Box>
              <TabPanel value="1">
                <TabPanelOrderControlContent></TabPanelOrderControlContent>
              </TabPanel>
              <TabPanel value="2">
                <TabPanelOrderBoardContent></TabPanelOrderBoardContent>
              </TabPanel>
              <TabPanel value="3">
                <TabPanelTradeRecordsContent></TabPanelTradeRecordsContent>
              </TabPanel>
              <TabPanel value="4">
                <TabPanelOrderBookStatisticsContent></TabPanelOrderBookStatisticsContent>
              </TabPanel>
              <TabPanel value="5">
                <TabPanelServerPerformanceStatisticsContent></TabPanelServerPerformanceStatisticsContent>
              </TabPanel>
              <TabPanel value="6">
                <TabPanelAccountSettingsContent></TabPanelAccountSettingsContent>
              </TabPanel>
              <TabPanel value="7">
                <TabPanelAboutContent></TabPanelAboutContent>
              </TabPanel>
              <TabPanel value="8">
                <TabPanelHelpContent></TabPanelHelpContent>
              </TabPanel>
            </TabContext>
          </Box>
        </Container>
      </Box>
    </>
  );
}
