import { useState, useEffect } from 'react';

import { Box } from '@mui/material';

import TradesTableContainer from './TradesTableContainer';

import axios from 'axios';

export default function TradesDisplayComponent() {
  const [rows, setRows] = useState([]);

  const fetchRows = async () => {
    let rows = [];
    const responseAllTrades = await axios.get(`/api/trades`, {});
    const allTrades = responseAllTrades.data['trades'];
    console.log(allTrades);
    for (const trade of allTrades) {
      console.log(`Trade: ${trade}`);
      rows.push(trade);
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
      <TradesTableContainer
        rows={rows}
        sx={{ px: 2, mt: 2, backgroundColor: 'background.whitesmoke' }}
      ></TradesTableContainer>
    </>
  );
}
