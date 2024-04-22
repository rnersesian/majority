import React from 'react';
import ReactDOM from 'react-dom/client';
import './style/style.css';
import MainPage from "./pages/main_page"
import Navbar from './components/navbar'

import reportWebVitals from './reportWebVitals';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import SignupPage from './pages/signup_page';
import MultiPlayerQuizzPage from "./pages/multi_quizz_page"

const router = createBrowserRouter([
  {
    path: "/solo",
    element: <MainPage />,
  },
  {
    path: "/signup",
    element: <SignupPage/>
  },
  {
    path: "/multi",
    element: <MultiPlayerQuizzPage/>
  }
]);



const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <>
    <Navbar/>
    
    <RouterProvider router={router}/>
  </>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
