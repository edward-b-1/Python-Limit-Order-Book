
import { useState, useEffect } from 'react';
import { Button, Box } from '@mui/material';

import TopOfBookTableContainer from './TopOfBookTableContainer';

import axios from 'axios';

export default function OrderEntryComponent() {
  const [rows, setRows] = useState([]);

  function refreshData() {
    fetchRows().then((data) => {
      setRows(data);
    });
  }

  const fetchRows = async () => {
    let rows = [];
    const responseAllTickers = await axios.post(`/api/list_all_tickers`, {});
    const allTickers = responseAllTickers.data['tickers'];
    for (const ticker of allTickers) {
      console.log(`${ticker}`);
      const responseTopOfBook = await axios.post(`/api/top_of_book`, {
        ticker: ticker,
      });
      const topOfBook = responseTopOfBook.data['top_of_book'];
      rows.push(topOfBook);
    }
    return rows;
  };

  useEffect(() => {
    fetchRows().then((data) => {
      setRows(data);
    });
  }, []);

  return (
    <>
      <Box sx={{ px: 1, py: 1 }}>
        <Button variant="contained" onClick={refreshData}>
          Refresh
        </Button>
      </Box>
      <TopOfBookTableContainer rows={rows} sx={{ px: 2, mt: 2 }}>
        table
      </TopOfBookTableContainer>
    </>
  );
}
