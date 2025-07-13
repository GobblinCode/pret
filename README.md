# Facebook Unfollow Tool

A web interface for demonstrating how to execute a script that unfollows/unlikes pages on Facebook.

## ⚠️ Important Disclaimers

- **Educational Purpose Only**: This tool is designed for educational purposes and demonstration of web automation concepts
- **Terms of Service**: Automating actions on Facebook may violate their Terms of Service
- **Account Safety**: Facebook actively detects and blocks automated scripts, which may result in account suspension
- **Security Risk**: Never share your Facebook credentials with third-party tools
- **Manual Alternative**: Consider manual unfollowing for better account safety and ToS compliance

## Features

- 🔐 Secure credential handling (local storage only)
- 🎯 Script execution simulation
- 📋 Copy-to-clipboard functionality for manual script execution
- 📱 Responsive design for all devices
- 🛡️ Built-in security warnings and best practices
- ⌨️ Keyboard shortcuts for better UX

## How to Use

### Option 1: Direct Script Execution (Recommended)

1. Navigate to your Facebook liked pages: `https://www.facebook.com/pages/feed/`
2. Open your browser's Developer Console (F12)
3. Copy and paste the script from the "Show Script Code" button
4. Press Enter to execute

### Option 2: Using the Web Interface

1. Open `index.html` in your web browser
2. Enter your Facebook credentials in Step 1
3. Provide the Facebook page URL in Step 2
4. Click "Execute Unfollow Script"
5. View the simulation results in Step 3

## The Script

The core JavaScript script that performs the unfollowing action:

```javascript
(function() {
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
})();
```

## How It Works

1. **Find Action Buttons**: Searches for all buttons with `aria-label="Action options"`
2. **Click Actions**: Clicks each action button to open the options menu
3. **Wait for Menus**: Uses a 1-second delay to allow menus to appear
4. **Find Unlike Options**: Searches for menu items containing "Unlike"
5. **Execute Unlike**: Clicks all found unlike buttons

## Limitations

- **Rate Limiting**: Facebook may rate limit or block rapid actions
- **Dynamic Content**: Facebook's interface changes frequently, which may break the script
- **Account Restrictions**: Automated actions may result in temporary or permanent account restrictions
- **Browser Compatibility**: Script may not work in all browsers or with all Facebook interface versions

## Security Considerations

- **Local Storage**: Credentials are stored locally in your browser only
- **No Third-Party Servers**: No data is sent to external servers
- **Clear Data**: Clear your browser data after use
- **Use at Your Own Risk**: The developers are not responsible for any account issues

## File Structure

```
facebook-unfollow-tool/
├── index.html          # Main HTML interface
├── styles.css          # Styling and responsive design
├── script.js           # JavaScript functionality
└── README.md          # This documentation
```

## Browser Compatibility

- ✅ Chrome 70+
- ✅ Firefox 65+
- ✅ Safari 12+
- ✅ Edge 79+

## Development

To run the application locally:

1. Clone or download the files
2. Open `index.html` in your web browser
3. No additional setup required (pure HTML/CSS/JavaScript)

## Keyboard Shortcuts

- `Ctrl/Cmd + Enter`: Execute script (when enabled)
- `Escape`: Close modal dialogs

## Contributing

This is an educational project. If you find issues or have suggestions for improvement, please ensure any changes maintain the educational focus and security warnings.

## Legal Notice

This tool is provided as-is for educational purposes. Users are responsible for ensuring their use complies with Facebook's Terms of Service and applicable laws. The developers assume no responsibility for any consequences resulting from the use of this tool.

## Alternative Methods

Instead of using automation, consider these safer alternatives:

1. **Manual Unfollowing**: Manually unlike pages through Facebook's interface
2. **Facebook Settings**: Use Facebook's built-in settings to manage your likes
3. **Browser Extensions**: Use official browser extensions that comply with Facebook's policies

## Support

For questions or issues:
- Check Facebook's Help Center for official guidance
- Review Facebook's Terms of Service
- Consider contacting Facebook Support for account-related issues

---

**Remember**: The safest approach is always manual interaction with Facebook's interface using their provided tools and settings.
