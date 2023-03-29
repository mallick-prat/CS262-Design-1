const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const messagesContainer = document.getElementById('messages');

sendButton.addEventListener('click', (event) => {
  event.preventDefault();

  const message = messageInput.value;

  // Make an AJAX request to send the message to the server
  // You can use fetch, axios or any other library of your choice
  fetch('/send_message', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message })
  })
  .then(response => response.json())
  .then(data => {
    // Display the new message in the chat interface
    const newMessage = document.createElement('div');
    newMessage.textContent = data.message;
    messagesContainer.appendChild(newMessage);

    // Clear the input field
    messageInput.value = '';
  })
  .catch(error => {
    console.error('Error sending message:', error);
  });
});
