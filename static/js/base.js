function hideSystemMessage() {
    let systemMessage = document.getElementById('system-message');
    if (systemMessage) {
        if (systemMessage.style.display !== 'none') {
            systemMessage.animate([
                { opacity: 1 },
                { opacity: 0 }
            ], {
                duration: 500,
                easing: 'ease-out',
                fill: 'forwards'
            });
            setTimeout(() => {
                systemMessage.style.display = 'none';
            }, 500);
        }
    }
}

function showSystemMessage(message, type) {
    let systemMessage = document.getElementById('system-message');
    if (systemMessage) {
        if (systemMessage.style.display !== 'none') {
            hideSystemMessage();
            setTimeout(() => {
                showSystemMessage(message, type);
            }, 500);
            return;
        }
        let systemMessageText = document.getElementById('system-message-text');
        if (systemMessageText) {
            systemMessageText.innerText = message;
            let systemMessageContainer = document.getElementById('system-message-container');
            if (systemMessageContainer) {
                systemMessageContainer.classList.remove('info', 'success', 'warning', 'error');
                if (['info', 'success', 'warning', 'error'].includes(type)) {
                    systemMessageContainer.classList.add(type);
                }
                else {
                    systemMessageContainer.classList.add('info');
                }
            }
            else {
                console.error('Unable to display system message: system-message-container not found');
            }

        }
        else {
            console.error('Unable to display system message: system-message-text not found');
        }
        systemMessage.style.display = 'flex';
        systemMessage.style.opacity = 0;
        systemMessage.animate([
            { opacity: 0 },
            { opacity: 1 }
        ], {
            duration: 500,
            easing: 'ease-in',
            fill: 'forwards'
        });
    }
    else {
        console.error('Unable to display system message: system-message not found');
    }
}

function getCSRFToken() {
    let cookieParts = document.cookie.split(';');
    for (let i = 0; i < cookieParts.length; i++) {
        let cookiePart = cookieParts[i].trim();
        if (cookiePart.startsWith('user_session_csrf_token=')) {
            return cookiePart.split('=')[1];
        }
    }
    return null;
}