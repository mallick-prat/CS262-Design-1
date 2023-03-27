import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import ChatRoom from './ChatRoom';
import ChatInput from './ChatInput';
import UserList from './UserList';
import axios from 'axios';

const Chat = ({ username, room }) => {
  const [messages, setMessages] = useState([]);
  const [users, setUsers] = useState([]);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const newSocket = io();

    setSocket(newSocket);

    newSocket.emit('join', { username, room });

    newSocket.on('message', (message) => {
      setMessages((prevMessages) => [...prevMessages, message]);
    });

    newSocket.on('users', (users) => {
      setUsers(users);
    });

    return () => {
      newSocket.emit('disconnect');
      newSocket.off();
    };
  }, [username, room]);

  const sendMessage = (message) => {
    socket.emit('chatMessage', message);
  };

  // Define a function to fetch the list of messages from the server
  const getMessageList = async () => {
    try {
      const response = await axios.get('/messages');
      return response.data;
    } catch (error) {
      console.log(error);
      return [];
    }
  };

  // Fetch the list of messages from the server when the component mounts
  useEffect(() => {
    getMessageList().then((messages) => {
      setMessages(messages);
    });
  }, []);

  return (
    <div>
      <UserList users={users} />
      <ChatRoom messages={messages} />
      <ChatInput sendMessage={sendMessage} />
    </div>
  );
};

export default Chat;
