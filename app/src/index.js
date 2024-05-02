import React from 'react';
import ReactDOM from 'react-dom/client';
import './style/style.css';
import Navbar from './components/navbar'

import reportWebVitals from './reportWebVitals';
import { createBrowserRouter, BrowserRouter, Route, Routes } from 'react-router-dom';

import SignupPage from './pages/signup_page';
import RoomSelectPage from "./pages/room_selection_page"
import MainPage from "./pages/main_page"
import PlayRoomPage from './pages/play_room_page';


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <>
    <BrowserRouter>
      <Navbar/>
      <Routes>
        <Route path="/lobbies" element={<RoomSelectPage/>} />
        <Route path="/signup" element={<SignupPage/>} />
        <Route path="/room" element={<PlayRoomPage/>} />
      </Routes>
    </BrowserRouter>
  </>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
