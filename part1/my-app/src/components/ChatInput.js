import React, { useState } from 'react';

const ChatInput = ({ sendMessage }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    sendMessage(message);
    setMessage('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={message}
        onChange={(event) => setMessage(event.target.value)}
      />
      <button type="submit">Send</button>
    </form>
  );
};

export default ChatInput;
