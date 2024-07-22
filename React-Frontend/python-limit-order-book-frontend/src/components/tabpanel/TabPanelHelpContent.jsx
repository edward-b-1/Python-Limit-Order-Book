import React from 'react';

import { Typography, Box, Link, Paper } from '@mui/material';

export default function TabPanelHelpContent() {
  return (
    <>
      <Box>
        <Box
          sx={{
            py: 2,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Paper sx={{backgroundColor: 'background.whitesmoke', px: 10 }}>
            <Typography variant="h2" sx={{ m: 3 }}>
              Help Page and User Instructions
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
          <Paper sx={{backgroundColor: 'background.whitesmoke'}}>
            <Box sx={{ my: 3, mx: 2, pb: 2, pt: 1 }}>
              <Typography variant="h3" sx={{ m: 1, mb: 2 }}>
                What is a Limit Order Book?
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                A Limit Order Book is a core piece of infastructure in financial
                exchanges across the world. It is used to match client buy and
                sell orders for different instruments across varrying price
                levels.
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                This website hosts a Limit Order Book. There are a number of
                different tabs which are accessible from this page. You are
                currently on the "Help" tab.
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                The "Order Entry" tab is where you can enter buy and sell
                orders. The top half of this page contains the Order Controls.
                The bottom half contains the Top Of Book display screen. The Top
                Of Book display screen simply displays the current best bid and
                ask prices for all available instruments. The instrument name,
                also known as a "Ticker" is shown in the leftmost column. The
                following columns show the best bid (buy) price available, with
                its associated volume, followed by the best ask (sell) price
                with an associated volume.
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                Click the "Refresh" button to refresh the live Top Of Book
                information.
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                A new order can be entered using the first line of controls,
                adjacent to the "Send Order" button. The Ticker can be any
                string, however it will make sense to use a well known stock
                ticker such as NVDA (Nvidia) or AAPL (Apple). The Order Side
                must be either "BUY" or "SELL". No other values are permitted.
                The price and volume can be any positive integer. Click "Send
                Order" to send the order. When the order has been sent, the
                "last order id" field will be populated. This Order Id is
                required to modify or cancel the order.
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                The next row of controls can be used to modify the price or
                volume of an existing order, using the Order Id.
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                The penultimate row can be used to partially cancel an order.
                The volume field must be less than or equal to the quantity
                remaining.
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                The final row can be used to completely cancel any remaining
                amount of an order.
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                The "Order Board" tab displays information about currently
                active orders, including the remaining volume.
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                The "Trade Records" tab displays a record of all previous
                trades.
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                The following 3 tabs, "Book Statistics", "Server Statistics" and
                "Account Settings", are not implemented yet. There is no login
                page, and there are no user accounts at present. Any user of
                this site can modify orders of any other user. (I have not had
                time to implement user account functionality, yet.)
              </Typography>
              <Typography variant="body1" sx={{ mb: 1 }}>
                Finally, the "About" tab provides information about the
                developer of this website as well as the technology stack used
                to build it.
              </Typography>
            </Box>
          </Paper>
        </Box>
      </Box>
    </>
  );
}
