import React from 'react';

const ChatMessage = ({ message }) => {
  return (
    <div>
      <span>{message.username}: </span>
      <span>{message.text}</span>
    </div>
  );
};

export default ChatMessage;
