import React from 'react';

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

export default function OrderBoardTableContainer({rows, sx}) {
  return (
    <TableContainer component={Paper} sx={sx}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Order Id</TableCell>
            <TableCell>Created Datetime</TableCell>
            <TableCell>Ticker</TableCell>
            <TableCell>Order Side</TableCell>
            <TableCell align="right">Price</TableCell>
            <TableCell align="right">Volume (remaining)</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={row.order_id}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {row.order_id}
              </TableCell>
              <TableCell>{row.timestamp}</TableCell>
              <TableCell>{row.ticker}</TableCell>
              <TableCell>{row.order_side}</TableCell>
              <TableCell align="right">{row.price}</TableCell>
              <TableCell align="right">{row.volume}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}