import React, { useState } from 'react';

const Login = ({ setUsername, setRoom }) => {
  const [usernameInput, setUsernameInput] = useState('');
  const [roomInput, setRoomInput] = useState('');

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
    <div>
      <form onSubmit={handleSubmit}>
        <label htmlFor="username">Username:</label>
        <input
          type="text"
          id="username"
          value={usernameInput}
          onChange={handleUsernameChange}
        />
        <label htmlFor="room">Room:</label>
        <input
          type="text"
          id="room"
          value={roomInput}
          onChange={handleRoomChange}
        />
        <button type="submit">Join Chat</button>
      </form>
    </div>
  );
};

export default Login;
