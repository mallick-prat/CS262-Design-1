import React from 'react';
import ChatMessage from './ChatMessage';

const ChatRoom = ({ messages }) => {
  return (
    <div>
      {messages.map((message, index) => (
        <ChatMessage key={index} message={message} />
      ))}
    </div>
  );
};

export default ChatRoom;
