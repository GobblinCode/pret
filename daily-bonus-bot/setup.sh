#!/bin/bash

echo "Daily Bonus Bot Setup"
echo "===================="

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    
    # Generate cipher key
    CIPHER_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
    
    # Update .env file based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/your-cipher-key-here/$CIPHER_KEY/" .env
        sed -i '' "s/your-secret-key-here-change-in-production/$(openssl rand -hex 32)/" .env
    else
        # Linux
        sed -i "s/your-cipher-key-here/$CIPHER_KEY/" .env
        sed -i "s/your-secret-key-here-change-in-production/$(openssl rand -hex 32)/" .env
    fi
    
    echo "Generated encryption keys in .env file"
fi

# Create screenshots directory
echo "Creating screenshots directory..."
mkdir -p static/screenshots

echo ""
echo "Setup complete!"
echo ""
echo "To start the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the application: python run.py"
echo ""
echo "Default login credentials:"
echo "Username: admin"
echo "Password: changeme123"
echo ""
echo "Access the application from your iPhone at: http://YOUR_COMPUTER_IP:5000"
echo "Make sure your iPhone and computer are on the same network."