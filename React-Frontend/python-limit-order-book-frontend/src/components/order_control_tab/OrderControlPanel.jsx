import React from 'react';

import { useState } from 'react';

import { Button, TextField, Box } from '@mui/material';
import Grid from '@mui/material/Grid';

import axios from 'axios';


export default function OrderControlPanel() {

  const [sendOrderTicker, setSendOrderTicker] = useState(null);
  const [sendOrderOrderSide, setSendOrderOrderSide] = useState(null);
  const [sendOrderPrice, setSendOrderPrice] = useState(null);
  const [sendOrderVolume, setSendOrderVolume] = useState(null);
  const [updateOrderOrderId, setUpdateOrderOrderId] = useState(null);
  const [updateOrderPrice, setUpdateOrderPrice] = useState(null);
  const [updateOrderVolume, setUpdateOrderVolume] = useState(null);
  const [partialCancelOrderOrderId, setPartialCancelOrderOrderId] =
    useState(null);
  const [partialCancelOrderVolume, setPartialCancelOrderVolume] =
    useState(null);
  const [cancelOrderOrderId, setCancelOrderOrderId] = useState('');
  const [apiStatusMessage, setApiStatusMessage] = useState('');
  const [apiOrderId, setApiOrderId] = useState('');

  function sendOrder() {
    console.log(
      `send order: ${sendOrderTicker} ${sendOrderOrderSide} ${sendOrderPrice} ${sendOrderVolume}`
    );
    axios
      .post('/api/send_order', {
        ticker: sendOrderTicker,
        order_side: sendOrderOrderSide,
        price: sendOrderPrice,
        volume: sendOrderVolume,
      })
      .then((response) => {
        console.log(response);
        const orderId = response.data.order_id;
        setApiOrderId(orderId);
        const message = response.data.statusText;
        setApiStatusMessage(message || '');
      });
  }

  function updateOrder() {
    console.log(
      `update order: ${updateOrderOrderId} ${updateOrderPrice} ${updateOrderVolume}`
    );
    axios
      .post('/api/update_order', {
        order_id: updateOrderOrderId,
        price: updateOrderPrice,
        volume: updateOrderVolume,
      })
      .then((response) => {
        console.log(response);
        const message = response.data.statusText;
        setApiStatusMessage(message || '');
      });
  }

  function cancelOrder() {
    console.log(`cancel order: ${cancelOrderOrderId}`);
    axios
      .post('/api/cancel_order', {
        order_id: cancelOrderOrderId,
      })
      .then((response) => {
        console.log(response);
      });
  }

  function cancelOrderPartial() {
    console.log(
      `cancel order partial: ${partialCancelOrderOrderId} ${partialCancelOrderVolume}`
    );
    axios
      .post('/api/cancel_order_partial', {
        order_id: partialCancelOrderOrderId,
        volume: partialCancelOrderVolume,
      })
      .then((response) => {
        console.log(response);
      });
  }

  function onChangeOrderAddTicker(event) {
    const ticker = event.target.value;
    setSendOrderTicker(ticker);
  }

  function onChangeOrderAddOrderSide(event) {
    const orderSide = event.target.value;
    setSendOrderOrderSide(orderSide);
  }

  function onChangeOrderAddPrice(event) {
    const price = event.target.value;
    setSendOrderPrice(price);
  }

  function onChangeOrderAddVolume(event) {
    const volume = event.target.value;
    setSendOrderVolume(volume);
  }

  function onChangeOrderUpdateOrderId(event) {
    const orderId = event.target.value;
    setUpdateOrderOrderId(orderId);
  }

  function onChangeOrderUpdatePrice(event) {
    const price = event.target.value;
    setUpdateOrderPrice(price);
  }

  function onChangeOrderUpdateVolume(event) {
    const volume = event.target.value;
    setUpdateOrderVolume(volume);
  }

  function onChangeOrderCancelPartialOrderId(event) {
    const orderId = event.target.value;
    setPartialCancelOrderOrderId(orderId);
  }

  function onChangeOrderCancelPartialVolume(event) {
    const volume = event.target.value;
    setPartialCancelOrderVolume(volume);
  }

  function onChangeOrderCancelOrderId(event) {
    const orderId = event.target.value;
    setCancelOrderOrderId(orderId);
  }

  return (
    <>
      <Grid container spacing={2} columns={10} alignItems="center">
        <Grid item xs={2}>
          <TextField
            id="text-entry-order-add-ticker"
            label="TICKER"
            variant="filled"
            onChange={onChangeOrderAddTicker}
          />
        </Grid>
        <Grid item xs={2}>
          <TextField
            id="text-entry-order-add-order-side"
            label="ORDER SIDE [BUY|SELL]"
            variant="filled"
            onChange={onChangeOrderAddOrderSide}
          />
        </Grid>
        <Grid item xs={2}>
          <TextField
            id="text-entry-order-add-price"
            label="PRICE"
            variant="filled"
            onChange={onChangeOrderAddPrice}
          />
        </Grid>
        <Grid item xs={2}>
          <TextField
            id="text-entry-order-add-volume"
            label="VOLUME"
            variant="filled"
            onChange={onChangeOrderAddVolume}
          />
        </Grid>
        <Grid item xs={2}>
          <Button variant="contained" onClick={sendOrder} sx={{ width: 1 }}>
            Send order
          </Button>
        </Grid>
        <Grid item xs={2}></Grid>
        <Grid item xs={2}>
          <TextField
            id="text-entry-order-update-order-id"
            label="ORDER ID"
            variant="filled"
            onChange={onChangeOrderUpdateOrderId}
          />
        </Grid>
        <Grid item xs={2}>
          <TextField
            id="text-entry-order-update-price"
            label="PRICE"
            variant="filled"
            onChange={onChangeOrderUpdatePrice}
          />
        </Grid>
        <Grid item xs={2}>
          <TextField
            id="text-entry-order-update-volume"
            label="VOLUME"
            variant="filled"
            onChange={onChangeOrderUpdateVolume}
          />
        </Grid>
        <Grid item xs={2}>
          <Button variant="contained" onClick={updateOrder} sx={{ width: 1 }}>
            Update order
          </Button>
        </Grid>
        <Grid item xs={2}></Grid>
        <Grid item xs={2}></Grid>
        <Grid item xs={2}>
          <TextField
            id="text-entry-order-cancel-partial-order-id"
            label="ORDER ID"
            variant="filled"
            onChange={onChangeOrderCancelPartialOrderId}
          />
        </Grid>
        <Grid item xs={2}>
          <TextField
            id="text-entry-order-cancel-partial-volume"
            label="VOLUME"
            variant="filled"
            onChange={onChangeOrderCancelPartialVolume}
          />
        </Grid>
        <Grid item xs={2}>
          <Button
            variant="contained"
            onClick={cancelOrderPartial}
            sx={{ width: 1 }}
          >
            Partial cancel order
          </Button>
        </Grid>
        <Grid item xs={2}></Grid>
        <Grid item xs={2}></Grid>
        <Grid item xs={2}></Grid>
        <Grid item xs={2}>
          <TextField
            id="text-entry-order-cancel-order-id"
            label="ORDER ID"
            variant="filled"
            onChange={onChangeOrderCancelOrderId}
          />
        </Grid>
        <Grid item xs={2}>
          <Button variant="contained" onClick={cancelOrder} sx={{ width: 1 }}>
            Cancel order
          </Button>
        </Grid>
      </Grid>

      <Box
        p={2}
        sx={{
          display: 'flex',
          flexDirection: 'row',
          justifyContent: 'center',
        }}
      >
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
          }}
        >
          <Grid container spacing={2} columns={2}>
            <Grid item xs={1}>
              <TextField
                id="text-field-order-id-last"
                label="last order id"
                variant="filled"
                value={apiOrderId}
                inputProps={{ readOnly: true }}
              ></TextField>
            </Grid>
            <Grid item xs={1}>
              <TextField
                id="text-field-webapi-message-status"
                label="api status message"
                variant="filled"
                value={apiStatusMessage}
                inputProps={{ readOnly: true }}
              ></TextField>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </>
  );
}
