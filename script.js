// Facebook Unfollow Script
const facebookScript = `(function() {
    function unlikeAllLikedPages() {
        const actionButtons = document.querySelectorAll('[aria-label="Action options"]');
        actionButtons.forEach(button => button.click());

        setTimeout(() => {
            const unlikeButtons = Array.from(document.querySelectorAll('[role="menuitem"]')).filter(button => button.innerText.includes('Unlike'));
            unlikeButtons.forEach(button => button.click());
        }, 1000);
    }

    // Execute the function
    unlikeAllLikedPages();
})();`;

// Global variables
let credentials = {
    username: '',
    password: ''
};

// DOM elements
const loginForm = document.getElementById('loginForm');
const executeButton = document.getElementById('executeScript');
const showScriptButton = document.getElementById('showScript');
const resultsDiv = document.getElementById('results');
const modal = document.getElementById('scriptModal');
const scriptCode = document.getElementById('scriptCode');
const copyScriptButton = document.getElementById('copyScript');
const closeModal = document.getElementsByClassName('close')[0];
const facebookUrlInput = document.getElementById('facebookUrl');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    updateScriptCode();
});

function initializeEventListeners() {
    // Login form submission
    loginForm.addEventListener('submit', handleLogin);
    
    // Execute script button
    executeButton.addEventListener('click', executeScript);
    
    // Show script button
    showScriptButton.addEventListener('click', showScript);
    
    // Copy script button
    copyScriptButton.addEventListener('click', copyScript);
    
    // Modal close events
    closeModal.addEventListener('click', closeScriptModal);
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeScriptModal();
        }
    });
    
    // URL input validation
    facebookUrlInput.addEventListener('input', validateInputs);
}

function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Store credentials (in a real app, this would be more secure)
    credentials.username = username;
    credentials.password = password;
    
    // Show success message
    showResult('success', `<span class="status-indicator status-success"></span>Credentials saved for: ${username}`);
    
    // Enable the execute button
    executeButton.disabled = false;
    
    // Show warning about security
    setTimeout(() => {
        showResult('warning', `<span class="status-indicator status-warning"></span>Warning: In a real implementation, never store credentials in plain text!`);
    }, 2000);
}

function validateInputs() {
    const url = facebookUrlInput.value;
    const hasCredentials = credentials.username && credentials.password;
    
    executeButton.disabled = !(hasCredentials && url);
}

function executeScript() {
    const url = facebookUrlInput.value;
    
    if (!url) {
        showResult('error', '<span class="status-indicator status-error"></span>Please enter a Facebook URL');
        return;
    }
    
    if (!credentials.username || !credentials.password) {
        showResult('error', '<span class="status-indicator status-error"></span>Please save your credentials first');
        return;
    }
    
    // Simulate script execution
    showResult('info', '<span class="status-indicator status-info"></span>Initiating script execution...');
    
    // Simulate different stages of execution
    setTimeout(() => {
        showResult('info', '<span class="status-indicator status-info"></span>Connecting to Facebook...');
    }, 1000);
    
    setTimeout(() => {
        showResult('info', '<span class="status-indicator status-info"></span>Navigating to: ' + url);
    }, 2000);
    
    setTimeout(() => {
        showResult('warning', '<span class="status-indicator status-warning"></span>Note: Due to Facebook\'s anti-automation measures, this simulation shows what would happen...');
    }, 3000);
    
    setTimeout(() => {
        showResult('info', '<span class="status-indicator status-info"></span>Looking for action buttons...');
    }, 4000);
    
    setTimeout(() => {
        showResult('success', `<span class="status-indicator status-success"></span>Script execution completed!
        
📊 Simulation Results:
• Found 15 action buttons
• Clicked 12 unlike buttons
• Processed 8 pages successfully
• 4 pages skipped (already unfollowed)

⚠️ Important Notes:
• This is a simulation only
• Real execution would require running the script directly in Facebook's browser console
• Facebook may detect and block automated actions
• Consider manual unfollowing for better compliance with ToS`);
    }, 5000);
}

function showScript() {
    modal.style.display = 'block';
}

function closeScriptModal() {
    modal.style.display = 'none';
}

function updateScriptCode() {
    scriptCode.textContent = facebookScript;
}

function copyScript() {
    navigator.clipboard.writeText(facebookScript).then(() => {
        const originalText = copyScriptButton.textContent;
        copyScriptButton.textContent = 'Copied!';
        copyScriptButton.style.background = '#4caf50';
        
        setTimeout(() => {
            copyScriptButton.textContent = originalText;
            copyScriptButton.style.background = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy script: ', err);
        showResult('error', '<span class="status-indicator status-error"></span>Failed to copy script to clipboard');
    });
}

function showResult(type, message) {
    resultsDiv.className = `results ${type}`;
    resultsDiv.innerHTML = message;
    
    // Auto-scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

// Additional utility functions
function validateFacebookUrl(url) {
    const facebookDomains = ['facebook.com', 'www.facebook.com', 'm.facebook.com'];
    try {
        const urlObj = new URL(url);
        return facebookDomains.includes(urlObj.hostname);
    } catch (e) {
        return false;
    }
}

// Enhanced security warning
function showSecurityWarning() {
    const warningMessage = `
        <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <strong>🔒 Security & Legal Considerations:</strong>
            <ul style="margin-top: 10px; margin-left: 20px;">
                <li>Automating actions on Facebook may violate their Terms of Service</li>
                <li>Facebook actively blocks automated scripts and may suspend accounts</li>
                <li>This tool is for educational purposes only</li>
                <li>Consider manual unfollowing for better account safety</li>
                <li>Never share your credentials with third-party tools</li>
            </ul>
        </div>
    `;
    
    const warningDiv = document.createElement('div');
    warningDiv.innerHTML = warningMessage;
    document.querySelector('main').prepend(warningDiv);
}

// Initialize security warning on page load
document.addEventListener('DOMContentLoaded', function() {
    showSecurityWarning();
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + Enter to execute script
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        if (!executeButton.disabled) {
            executeScript();
        }
    }
    
    // Escape to close modal
    if (event.key === 'Escape' && modal.style.display === 'block') {
        closeScriptModal();
    }
});