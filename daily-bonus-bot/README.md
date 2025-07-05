# Daily Bonus Bot

A mobile-friendly web application that automates daily login bonus claims from gambling websites. Access and control the bot directly from your iPhone with a beautiful, responsive interface.

## Features

- 📱 **Mobile-Optimized Interface**: Designed specifically for iPhone access
- 🤖 **Automated Bonus Claims**: Uses Playwright to automate browser interactions
- 🔐 **Secure Credential Storage**: Passwords are encrypted before storage
- 📅 **Scheduled Daily Claims**: Automatically runs at 9 AM UTC daily
- 📸 **Screenshot Verification**: Takes screenshots after each claim attempt
- 🍪 **Cookie Management**: Saves and reuses login sessions
- 📊 **Success Tracking**: Monitor claim history and success rates
- 🧪 **Test Mode**: Test configurations before enabling automated claims

## Prerequisites

- Python 3.8 or higher
- A computer to run the bot server
- iPhone and computer on the same network

## Quick Setup

1. Clone or download this project:
```bash
cd daily-bonus-bot
```

2. Make the setup script executable and run it:
```bash
chmod +x setup.sh
./setup.sh
```

3. Start the application:
```bash
source venv/bin/activate
python run.py
```

4. Find your computer's IP address:
   - On Mac: `ifconfig | grep "inet " | grep -v 127.0.0.1`
   - On Linux: `hostname -I`
   - On Windows: `ipconfig`

5. On your iPhone, open Safari and navigate to:
   ```
   http://YOUR_COMPUTER_IP:5000
   ```

6. Login with default credentials:
   - Username: `admin`
   - Password: `changeme123`

## Manual Setup (Alternative)

If the setup script doesn't work, follow these steps:

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

3. Create a `.env` file:
```bash
cp .env.example .env
```

4. Generate encryption keys:
```bash
python -c "from cryptography.fernet import Fernet; print('CIPHER_KEY=' + Fernet.generate_key().decode())"
```
Add the generated key to your `.env` file.

5. Create directories:
```bash
mkdir -p static/screenshots
```

6. Run the application:
```bash
python run.py
```

## Usage Guide

### Adding a Gambling Site

1. Navigate to the "Sites" page
2. Click "Add Site"
3. Fill in the required information:
   - **Site Name**: A friendly name for the site
   - **URL**: The main website URL
   - **Login Credentials**: Your username and password
   - **CSS Selectors**: Elements for automation (see below)

### Finding CSS Selectors

1. Open the gambling site in Chrome/Safari
2. Right-click on the element (username field, login button, etc.)
3. Select "Inspect" or "Inspect Element"
4. Right-click on the highlighted HTML code
5. Select "Copy" → "Copy selector"

Common selectors to find:
- Username input field
- Password input field
- Login/Submit button
- Daily bonus claim button

### Additional Navigation Steps

For sites that require navigation to reach the bonus page, use JSON format:

```json
[
  {
    "action": "click",
    "selector": ".promotions-menu",
    "wait": 2
  },
  {
    "action": "wait_for_selector",
    "selector": ".daily-bonus-button",
    "timeout": 10000
  }
]
```

Available actions:
- `click`: Click an element
- `fill`: Fill a form field
- `navigate`: Go to a URL
- `wait`: Wait for seconds
- `wait_for_selector`: Wait for element to appear

### Testing a Site Configuration

1. After adding/editing a site, click the "Test" button
2. The bot will attempt to claim the bonus
3. Check the screenshot to verify success
4. If successful, enable the site for daily claims

### Manual Claim All

From the dashboard, click "Claim All Bonuses" to manually trigger claims for all active sites.

## Security Considerations

1. **Change Default Credentials**: Update the admin username and password in `.env`
2. **Secure Your Network**: Only access the bot from trusted networks
3. **Password Encryption**: All gambling site passwords are encrypted
4. **Environment Variables**: Keep your `.env` file secure and never commit it

## Troubleshooting

### Can't access from iPhone
- Ensure both devices are on the same network
- Check firewall settings on your computer
- Try using your computer's local IP instead of hostname

### Login failures
- Verify CSS selectors are correct
- Check if the site has changed its layout
- Try the "Test" function to debug
- Review screenshots for error details

### Playwright errors
- Run `playwright install chromium` to ensure browser is installed
- Check system requirements for Playwright

## Configuration

### Environment Variables (.env)

- `SECRET_KEY`: Flask session encryption key
- `ADMIN_USERNAME`: Admin login username
- `ADMIN_PASSWORD`: Admin login password
- `CIPHER_KEY`: Key for encrypting gambling site passwords
- `DATABASE_URL`: Database connection string (SQLite by default)

### Scheduling

The bot runs daily at 9 AM UTC by default. To change:
1. Edit `app/tasks.py`
2. Modify the `hour` parameter in `schedule_daily_claims()`
3. Restart the application

## Production Deployment

For production use:

1. Use a proper web server (gunicorn):
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

2. Set up a reverse proxy (nginx)
3. Use HTTPS with SSL certificates
4. Set `debug=False` in `run.py`
5. Use a production database (PostgreSQL)
6. Set up proper logging and monitoring

## Disclaimer

This bot is for educational purposes. Ensure you comply with the terms of service of any websites you interact with. The authors are not responsible for any misuse or violations of website terms.

## License

MIT License - feel free to modify and use as needed.