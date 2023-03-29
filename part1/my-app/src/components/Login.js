import React, { useState } from 'react';
import io from "socket.io-client/dist/socket.io.js";

const socket = io("http://localhost:5000");

function Login({ setUsername, setRoom }) {
    const [usernameInput, setUsernameInput] = useState("");
    const [roomInput, setRoomInput] = useState("");
  
    const handleUsernameChange = (event) => {
      setUsernameInput(event.target.value);
    };
  
    const handleRoomChange = (event) => {
      setRoomInput(event.target.value);
    };
  
    const handleSubmit = (event) => {
      event.preventDefault();
      setUsername(usernameInput);
      setRoom(roomInput);
    };
  
    return (
      <form onSubmit={handleSubmit}>
        <h1>Join a Chat Room</h1>
        <div>
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={usernameInput}
            onChange={handleUsernameChange}
            required
          />
        </div>
        <div>
          <label htmlFor="room">Room:</label>
          <input
            type="text"
            id="room"
            value={roomInput}
            onChange={handleRoomChange}
            required
          />
        </div>
        <button type="submit">Join</button>
      </form>
    );
  }
  
export default Login;
