document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-btn');
    const connectionStatus = document.getElementById('connection-status');
    const spiritualQuote = document.getElementById('spiritual-quote');
    
    // Base API URL (modify this based on your environment)
    const API_BASE_URL = window.location.pathname.endsWith('/') ? '/api' : '/api';
    
    // Spiritual quotes to rotate
    const spiritualQuotes = [
        "Wherever there is Krishna, the master of all mystics, and wherever there is Arjuna, the supreme archer, there will certainly be opulence, victory, extraordinary power, and morality.",
        "You have the right to work, but never to the fruit of work. You should never engage in action for the sake of reward, nor should you long for inaction.",
        "The soul can never be cut to pieces by any weapon, nor burned by fire, nor moistened by water, nor withered by the wind.",
        "For the soul there is neither birth nor death at any time. He has not come into being, does not come into being, and will not come into being. He is unborn, eternal, ever-existing, and primeval.",
        "One who sees inaction in action, and action in inaction, is intelligent among men.",
        "The wise see that there is action in inaction and inaction in action.",
        "He who sees Me everywhere and sees everything in Me, never loses sight of Me, nor do I ever lose sight of him.",
        "Whatever you do, whatever you eat, whatever you offer in sacrifice, whatever you give, whatever you practice as austerity, do it as an offering to Me."
    ];
    
    // Rotate spiritual quotes
    let quoteIndex = 0;
    function rotateQuotes() {
        if (spiritualQuote) {
            spiritualQuote.style.opacity = 0;
            setTimeout(() => {
                quoteIndex = (quoteIndex + 1) % spiritualQuotes.length;
                spiritualQuote.textContent = spiritualQuotes[quoteIndex];
                spiritualQuote.style.opacity = 1;
            }, 500);
        }
    }
    
    // Set interval to rotate quotes (every 30 seconds)
    setInterval(rotateQuotes, 30000);
    
    console.log('GitaAI Chat initialized');

    // Update connection status with animation
    function updateConnectionStatus(status, message) {
        connectionStatus.className = '';
        connectionStatus.textContent = message;
        
        // Add a slight delay before applying the class for animation effect
        setTimeout(() => {
            connectionStatus.classList.add(status);
        }, 50);
    }

    // Initial status
    updateConnectionStatus('connecting', 'Connecting...');

    // Check server connectivity on load
    checkServerConnectivity();

    // Function to test server connectivity
    async function checkServerConnectivity() {
        try {
            updateConnectionStatus('connecting', 'Checking connection...');
            console.log('Testing server connectivity...');
            
            const response = await fetch(`${API_BASE_URL}/test`);
            if (response.ok) {
                const data = await response.json();
                console.log('Server connectivity test:', data);
                updateConnectionStatus('connected', 'Connected');
                addMessage('I am ready to answer your questions about the Bhagavad Gita and share spiritual wisdom.', 'system');
            } else {
                console.error('Server test failed:', response.status);
                updateConnectionStatus('disconnected', 'Connection failed');
                addMessage('Server connectivity issue. Please refresh the page or try again later.', 'system');
            }
        } catch (error) {
            console.error('Server connectivity error:', error);
            updateConnectionStatus('disconnected', 'Cannot connect to server');
            addMessage('Cannot connect to the server. Please check if the backend is running.', 'system');
        }
    }

    // Function to create and add a message to the chat
    function addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type);
        messageDiv.style.opacity = '0';
        messageDiv.style.transform = 'translateY(10px)';

        const avatar = document.createElement('div');
        avatar.classList.add('avatar', type === 'user' ? 'user' : 'krishna');
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        
        const paragraph = document.createElement('p');
        paragraph.textContent = text;
        
        messageContent.appendChild(paragraph);
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to the bottom of the chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Animate the message appearance
        setTimeout(() => {
            messageDiv.style.opacity = '1';
            messageDiv.style.transform = 'translateY(0)';
            messageDiv.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        }, 50);
        
        console.log(`Added ${type} message: ${text.substring(0, 50)}...`);
    }

    // Function to add a typing indicator
    function addTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'system', 'typing-message');
        typingDiv.style.opacity = '0';
        
        const avatar = document.createElement('div');
        avatar.classList.add('avatar', 'krishna');
        
        const typingContent = document.createElement('div');
        typingContent.classList.add('typing-indicator');
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            typingContent.appendChild(dot);
        }
        
        typingDiv.appendChild(avatar);
        typingDiv.appendChild(typingContent);
        
        chatMessages.appendChild(typingDiv);
        
        // Animate the typing indicator appearance
        setTimeout(() => {
            typingDiv.style.opacity = '1';
            typingDiv.style.transition = 'opacity 0.3s ease';
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 50);
        
        console.log('Added typing indicator');
        return typingDiv;
    }

    // Function to remove the typing indicator
    function removeTypingIndicator() {
        const typingMessage = document.querySelector('.typing-message');
        if (typingMessage) {
            typingMessage.style.opacity = '0';
            
            // Remove after fade out animation completes
            setTimeout(() => {
                if (typingMessage.parentNode) {
                    chatMessages.removeChild(typingMessage);
                }
                console.log('Removed typing indicator');
            }, 300);
        }
    }

    // Function to send a message to the server and get a response
    async function sendMessage(message) {
        try {
            console.log('Sending message to server:', message);
            const typingIndicator = addTypingIndicator();
            
            // Rotate spiritual quote when user sends a message
            rotateQuotes();
            
            // Create the full API URL
            const apiUrl = `${API_BASE_URL}/chat`;
            console.log('Using API URL:', apiUrl);
            
            // Prepare the request
            const requestOptions = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            };
            
            // Add minimum delay to ensure typing indicator is visible (better UX)
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            const response = await fetch(apiUrl, requestOptions);
            
            // Add slight delay before removing typing indicator
            setTimeout(() => {
                removeTypingIndicator();
            }, 300);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('Server error:', errorText);
                throw new Error(`Server responded with status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Response received');
            
            if (data.error) {
                addMessage(`Error: ${data.error}. Please try again later.`, 'system');
            } else {
                addMessage(data.message, 'system');
            }
        } catch (error) {
            removeTypingIndicator();
            addMessage(`Sorry, I encountered an error: ${error.message}. Please try again later.`, 'system');
            console.error('Error sending message:', error);
        }
    }

    // Function to handle sending a message
    function handleSendMessage() {
        const message = userInput.value.trim();
        
        if (message) {
            console.log('User submitted message:', message);
            addMessage(message, 'user');
            userInput.value = '';
            userInput.style.height = 'auto';
            sendMessage(message);
        }
    }

    // Event listeners
    sendButton.addEventListener('click', handleSendMessage);
    
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });

    // Auto-resize textarea as user types
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = (userInput.scrollHeight < 150) ? `${userInput.scrollHeight}px` : '150px';
    });
    
    // Focus input field when page loads
    setTimeout(() => {
        userInput.focus();
    }, 1000);
}); 