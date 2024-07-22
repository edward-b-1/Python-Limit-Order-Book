import React from 'react';

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

export default function TopOfBookTableContainer({rows, sx}) {
  return (
    <TableContainer component={Paper} sx={sx}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Ticker</TableCell>
            <TableCell align="right">Price BUY</TableCell>
            <TableCell align="right">Volume BUY</TableCell>
            <TableCell align="right">Price SELL</TableCell>
            <TableCell align="right">Volume SELL</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={row.ticker}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {row.ticker}
              </TableCell>
              <TableCell align="right">{row.price_buy}</TableCell>
              <TableCell align="right">{row.volume_buy}</TableCell>
              <TableCell align="right">{row.price_sell}</TableCell>
              <TableCell align="right">{row.volume_sell}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}