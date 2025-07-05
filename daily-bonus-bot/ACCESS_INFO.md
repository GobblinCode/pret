# Daily Bonus Bot - Access Information

## ✅ Application Status: RUNNING

The Daily Bonus Bot is now successfully running on your server!

## 📱 Access from iPhone

1. Make sure your iPhone is connected to the same network as this server
2. Open Safari on your iPhone
3. Navigate to: **http://172.17.0.2:5000**

## 🔐 Login Credentials

- **Username:** admin
- **Password:** changeme123

## 🚀 Features Currently Available

- ✅ Mobile-optimized interface
- ✅ User authentication
- ✅ Site management (add/edit/delete gambling sites)
- ✅ Mock automation for testing (80% success rate simulation)
- ✅ Claim history tracking
- ✅ Dashboard with statistics
- ✅ Scheduled daily claims (9 AM UTC)

## ⚠️ Important Notes

1. **Mock Mode**: The application is currently running with mock automation to demonstrate functionality without requiring Playwright. The bot simulates claiming bonuses with an 80% success rate.

2. **Real Automation**: To enable real browser automation:
   - Install Playwright: `pip3 install playwright==1.48.0`
   - Install browsers: `playwright install chromium`
   - The application will automatically use the real automation module

3. **Security**: 
   - Change the default admin credentials immediately
   - Use HTTPS in production
   - Keep the .env file secure

## 🛠️ Managing the Application

**Stop the application:**
```bash
pkill -f "python3 run.py"
```

**Restart the application:**
```bash
cd /workspace/daily-bonus-bot
python3 run.py
```

**Run in production mode:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 📊 Current Configuration

- Database: SQLite (bonus_bot.db)
- Screenshots: /workspace/daily-bonus-bot/static/screenshots/
- Scheduler: Running (daily claims at 9 AM UTC)
- Encryption: Enabled for password storage

## 🎯 Next Steps

1. Access the application from your iPhone
2. Add your gambling sites with proper CSS selectors
3. Test each site configuration
4. Monitor the claim history
5. Install Playwright for real automation when ready

Enjoy your automated daily bonus claims!