import React, { useState } from 'react';
import Chat from './components/Chat';
import Login from './components/Login';
import io from 'socket.io-client';

const App = () => {
  const [username, setUsername] = useState('');
  const [room, setRoom] = useState('');

  const handleLogin = (username, room) => {
    setUsername(username);
    setRoom(room);
  };

  return (
    <div>
      {username && room ? (
        <Chat username={username} room={room} />
      ) : (
        <Login handleLogin={handleLogin} />
      )}
    </div>
  );
};

export default App;
