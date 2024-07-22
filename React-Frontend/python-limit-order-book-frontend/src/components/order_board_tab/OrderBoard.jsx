import React from 'react';
import { useState, useEffect } from 'react';

import { Box } from '@mui/material';

import OrderBoardTableContainer from './OrderBoardTableContainer';

import axios from 'axios';

export default function OrderBoard() {
  const [rows, setRows] = useState([]);

  const fetchRows = async () => {
    let rows = [];
    const responseAllTickers = await axios.get(`/api/order_board`, {});
    const allOrders = responseAllTickers.data['orders'];
    for (const order of allOrders) {
      rows.push(order);
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
      <OrderBoardTableContainer
        rows={rows}
        sx={{ px: 2, mt: 2, backgroundColor: 'background.whitesmoke' }}
      >
        table
      </OrderBoardTableContainer>
    </>
  );
}
