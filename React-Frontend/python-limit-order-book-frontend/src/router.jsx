import React from 'react';

import { createBrowserRouter } from 'react-router-dom';

// import LoginPage from './routes/LoginPage';
import AboutPage from './routes/AboutPage';
// import OrderControlPanel from "./routes/OrderControlPanel";
import NotFoundPage from './routes/NotFoundPage';
import RootPage from './routes/RootPage';
import MainPage from './routes/MainPage';

export const router = createBrowserRouter([
  { path: '/', element: <RootPage></RootPage> },
  // { path: '/login', element: <LoginPage></LoginPage> },
  // {
  //   path: "/order-control-pannel",
  //   element: <OrderControlPanel></OrderControlPanel>,
  // },
  { path: '/mainpage', element: <MainPage></MainPage> },
  { path: '/about', element: <AboutPage></AboutPage> },
  {
    path: '*',
    element: <NotFoundPage></NotFoundPage>,
  },
]);
