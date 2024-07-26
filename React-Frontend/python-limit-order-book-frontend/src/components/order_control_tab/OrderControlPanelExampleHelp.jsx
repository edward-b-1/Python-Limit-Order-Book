import React from 'react';

import { Typography, Box } from '@mui/material';
import Accordion from '@mui/material/Accordion';
import AccordionActions from '@mui/material/AccordionActions';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Button from '@mui/material/Button';

function OrderControlPanelExampleHelp() {
  return (
    <>
      <Accordion disableGutters={true} sx={{ mb: 4, mt: 0, ml: 2, mr: 2 }}>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1-content"
          id="panel1-header"
        >
          Send Order Example
        </AccordionSummary>
        <AccordionDetails>
          <Typography sx={{ mb: 2 }}>
            The first row is used to enter details for an Order. For example,
            you could enter an order:
          </Typography>
          <Typography
            sx={{ fontFamily: 'Monospace', fontWeight: 'bold', ml: 4, mb: 2 }}
          >
            TSLA BUY 200 20
          </Typography>
          <Typography sx={{ mb: 2 }}>followed by another order</Typography>
          <Typography
            sx={{ fontFamily: 'Monospace', fontWeight: 'bold', ml: 4, mb: 2 }}
          >
            TSLA SELL 190 10
          </Typography>
          <Typography>
            and inspect the Order Board and Trade Records tabs to see the
            results.
          </Typography>
        </AccordionDetails>
      </Accordion>
      {/* <Typography>OrderControlPanelExampleHelp</Typography> */}
    </>
  );
}

export default OrderControlPanelExampleHelp;
