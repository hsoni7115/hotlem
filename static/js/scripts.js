async function sendMessage() {
    let userMessage = document.getElementById('user-input').value;
    let receiverEmail = document.getElementById('receiver-email').value;  // Get receiver's email
    if (userMessage.trim() === "") return;

    // Display the user's message in the chat box
    appendMessage('user', userMessage);
    document.getElementById('user-input').value = "";  // Clear input field

    // Check if receiver email is provided
    if (!receiverEmail.trim()) {
        appendMessage('assistant', "Please provide a receiver's email.");
        return;
    }

    // Prepare data to send to the Flask backend
    const data = {
        message: userMessage,
        receiver_email: receiverEmail, // Include receiver email in the data
    };

    // Send the message to the Flask backend
    try {
        const response = await fetch('http://127.0.0.1:5000/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();

        // Display the assistant's response in the chat box
        appendMessage('assistant', result.reply || "Sorry, I didn't get that.");
    } catch (error) {
        console.error('Error:', error);
        appendMessage('assistant', "There was an error. Please try again later.");
    }
}

function appendMessage(sender, message) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', `${sender}-message`);
    
    const messageText = document.createElement('p');
    messageText.textContent = message;
    messageElement.appendChild(messageText);

    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the bottom
}
